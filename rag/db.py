"""Database operations for RAG — PostgreSQL + pgvector."""

import hashlib
import json
import logging
from datetime import datetime, timezone

import psycopg2
import psycopg2.extras

from .config import DATABASE_URL, EMBEDDING_DIMS

log = logging.getLogger("rag.db")

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

_connection_url = DATABASE_URL
_schema_ready = False
_working_url = None  # resolved after first successful connection


def _try_connect(url: str):
    """Attempt a connection, return the connection or raise."""
    conn = psycopg2.connect(url, connect_timeout=10)
    # Test the connection is actually alive
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
    return conn


def _resolve_connection():
    """Try the DATABASE_URL as-is, then with sslmode variants."""
    global _working_url
    if _working_url:
        return _working_url

    url = _connection_url
    if not url:
        raise RuntimeError("DATABASE_URL is not configured")

    # If user already specified sslmode, use as-is
    if "sslmode=" in url:
        _working_url = url
        return url

    separator = "&" if "?" in url else "?"

    # Try in order: as-is, sslmode=require, sslmode=disable
    attempts = [
        ("as-is", url),
        ("sslmode=require", f"{url}{separator}sslmode=require"),
        ("sslmode=disable", f"{url}{separator}sslmode=disable"),
    ]

    last_error = None
    for label, attempt_url in attempts:
        try:
            conn = _try_connect(attempt_url)
            conn.close()
            _working_url = attempt_url
            log.info(f"Database connection successful ({label})")
            return attempt_url
        except Exception as e:
            last_error = e
            log.warning(f"Connection attempt ({label}) failed: {e}")

    raise RuntimeError(f"All connection attempts failed. Last error: {last_error}")


def get_conn():
    """Get a new database connection."""
    url = _resolve_connection()
    return psycopg2.connect(url, connect_timeout=10)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = f"""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rag_documents (
    id              SERIAL PRIMARY KEY,
    source_path     TEXT NOT NULL,
    source_type     TEXT NOT NULL DEFAULT 'file',
    title           TEXT,
    category        TEXT,
    content_hash    TEXT,
    metadata        JSONB DEFAULT '{{}}'::jsonb,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_path, source_type)
);

CREATE TABLE IF NOT EXISTS rag_chunks (
    id              SERIAL PRIMARY KEY,
    document_id     INTEGER NOT NULL REFERENCES rag_documents(id) ON DELETE CASCADE,
    chunk_index     INTEGER NOT NULL,
    content         TEXT NOT NULL,
    section_title   TEXT,
    embedding       vector({EMBEDDING_DIMS}),
    metadata        JSONB DEFAULT '{{}}'::jsonb,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_rag_chunks_embedding
    ON rag_chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_rag_chunks_document_id
    ON rag_chunks(document_id);

CREATE INDEX IF NOT EXISTS idx_rag_documents_category
    ON rag_documents(category);
"""


def _check_embedding_dims(conn):
    """Check if existing embedding column matches configured dims. Migrate if needed."""
    try:
        with conn.cursor() as cur:
            # Check if rag_chunks table exists
            cur.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'rag_chunks' AND column_name = 'embedding'
            """)
            if not cur.fetchone():
                return  # Table doesn't exist yet, schema init will create it

            # Check current vector dimensions
            cur.execute("""
                SELECT atttypmod FROM pg_attribute
                WHERE attrelid = 'rag_chunks'::regclass AND attname = 'embedding'
            """)
            row = cur.fetchone()
            if row and row[0] > 0 and row[0] != EMBEDDING_DIMS:
                old_dims = row[0]
                log.warning(f"Embedding dimensions changed ({old_dims} → {EMBEDDING_DIMS}). Migrating...")
                # Drop chunks and index, recreate with new dimensions
                cur.execute("DROP INDEX IF EXISTS idx_rag_chunks_embedding")
                cur.execute("DROP TABLE IF EXISTS rag_chunks CASCADE")
                # Also clear document hashes so they get re-embedded on next sync
                cur.execute("UPDATE rag_documents SET content_hash = NULL")
                conn.commit()
                log.info(f"Migration complete. Chunks cleared — run 'rag sync --force' to re-embed.")
    except Exception as e:
        log.warning(f"Embedding dims check failed (non-fatal): {e}")


def init_schema():
    """Create tables and extensions if they don't exist."""
    global _schema_ready
    conn = get_conn()
    try:
        _check_embedding_dims(conn)
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
        conn.commit()
        _schema_ready = True
        log.info("RAG schema initialized successfully")
    except Exception as e:
        log.error(f"Schema init failed: {e}")
        # Try without the HNSW index (pgvector might be an older version)
        try:
            fallback_sql = SCHEMA_SQL.replace(
                f"CREATE INDEX IF NOT EXISTS idx_rag_chunks_embedding\n"
                f"    ON rag_chunks USING hnsw (embedding vector_cosine_ops)\n"
                f"    WITH (m = 16, ef_construction = 64);",
                "-- HNSW index skipped (not supported on this pgvector version)"
            )
            conn2 = get_conn()
            with conn2.cursor() as cur:
                cur.execute(fallback_sql)
            conn2.commit()
            conn2.close()
            _schema_ready = True
            log.warning("Schema initialized WITHOUT HNSW index (pgvector may be older)")
        except Exception as e2:
            log.error(f"Fallback schema init also failed: {e2}")
            raise e2
    finally:
        conn.close()


def is_ready() -> bool:
    """Check if the schema has been initialized."""
    return _schema_ready


# ---------------------------------------------------------------------------
# Document CRUD
# ---------------------------------------------------------------------------

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def get_document(source_path: str, source_type: str = "file"):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM rag_documents WHERE source_path = %s AND source_type = %s",
                (source_path, source_type),
            )
            return cur.fetchone()
    finally:
        conn.close()


def upsert_document(source_path: str, title: str, category: str,
                    content: str, source_type: str = "file",
                    metadata: dict = None) -> int:
    """Insert or update a document, returns document ID."""
    c_hash = content_hash(content)
    meta_json = json.dumps(metadata or {})
    now = datetime.now(timezone.utc)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO rag_documents (source_path, source_type, title, category, content_hash, metadata, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)
                ON CONFLICT (source_path, source_type)
                DO UPDATE SET title = EXCLUDED.title, category = EXCLUDED.category,
                              content_hash = EXCLUDED.content_hash, metadata = EXCLUDED.metadata,
                              updated_at = EXCLUDED.updated_at
                RETURNING id
            """, (source_path, source_type, title, category, c_hash, meta_json, now, now))
            doc_id = cur.fetchone()[0]
        conn.commit()
        return doc_id
    finally:
        conn.close()


def delete_document(doc_id: int):
    """Delete a document and its chunks (CASCADE)."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM rag_documents WHERE id = %s", (doc_id,))
        conn.commit()
    finally:
        conn.close()


def delete_chunks_for_document(doc_id: int):
    """Remove all chunks for a document (before re-embedding)."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM rag_chunks WHERE document_id = %s", (doc_id,))
        conn.commit()
    finally:
        conn.close()


def insert_chunks(doc_id: int, chunks: list[dict]):
    """Bulk insert chunks with embeddings."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            for i, chunk in enumerate(chunks):
                embedding_str = "[" + ",".join(str(v) for v in chunk["embedding"]) + "]"
                cur.execute("""
                    INSERT INTO rag_chunks (document_id, chunk_index, content, section_title, embedding, metadata)
                    VALUES (%s, %s, %s, %s, %s::vector, %s::jsonb)
                """, (
                    doc_id, i, chunk["content"], chunk.get("section_title", ""),
                    embedding_str, json.dumps(chunk.get("metadata", {}))
                ))
        conn.commit()
        log.info(f"Inserted {len(chunks)} chunks for document {doc_id}")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search(query_embedding: list[float], top_k: int = 5,
           category: str = None) -> list[dict]:
    """Semantic search — returns top-k most similar chunks."""
    embedding_str = "[" + ",".join(str(v) for v in query_embedding) + "]"

    where_clause = ""
    params = [embedding_str, embedding_str, top_k]
    if category:
        where_clause = "AND d.category = %s"
        params = [embedding_str, embedding_str, category, top_k]

    query = f"""
        SELECT
            c.id, c.content, c.section_title, c.chunk_index,
            d.source_path, d.title, d.category, d.source_type,
            1 - (c.embedding <=> %s::vector) AS similarity
        FROM rag_chunks c
        JOIN rag_documents d ON c.document_id = d.id
        WHERE c.embedding IS NOT NULL {where_clause}
        ORDER BY c.embedding <=> %s::vector
        LIMIT %s
    """

    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Stats / Listing
# ---------------------------------------------------------------------------

def list_documents(category: str = None) -> list[dict]:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if category:
                cur.execute("""
                    SELECT d.*, COUNT(c.id) as chunk_count
                    FROM rag_documents d LEFT JOIN rag_chunks c ON c.document_id = d.id
                    WHERE d.category = %s GROUP BY d.id ORDER BY d.updated_at DESC
                """, (category,))
            else:
                cur.execute("""
                    SELECT d.*, COUNT(c.id) as chunk_count
                    FROM rag_documents d LEFT JOIN rag_chunks c ON c.document_id = d.id
                    GROUP BY d.id ORDER BY d.updated_at DESC
                """)
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def get_stats() -> dict:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) as count FROM rag_documents")
            doc_count = cur.fetchone()["count"]
            cur.execute("SELECT COUNT(*) as count FROM rag_chunks")
            chunk_count = cur.fetchone()["count"]
            cur.execute("""
                SELECT category, COUNT(*) as count
                FROM rag_documents GROUP BY category ORDER BY count DESC
            """)
            categories = [dict(row) for row in cur.fetchall()]
            return {
                "documents": doc_count,
                "chunks": chunk_count,
                "categories": categories,
            }
    finally:
        conn.close()


def remove_stale_file_documents(active_paths: set[str]):
    """Remove file-sourced documents that no longer exist on disk."""
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT id, source_path FROM rag_documents WHERE source_type = 'file'"
            )
            rows = cur.fetchall()
        removed = 0
        for row in rows:
            if row["source_path"] not in active_paths:
                delete_document(row["id"])
                log.info(f"Removed stale document: {row['source_path']}")
                removed += 1
        return removed
    finally:
        conn.close()
