"""RAG HTTP API — runs as sidecar alongside OpenClaw gateway."""

import logging
import traceback
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import db, embeddings, sync as sync_module
from .config import DEFAULT_TOP_K, MAX_TOP_K

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger("rag.server")

app = FastAPI(title="RevX RAG", version="1.0.0", docs_url="/rag/docs")


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=DEFAULT_TOP_K, ge=1, le=MAX_TOP_K)
    category: Optional[str] = None


class SearchResult(BaseModel):
    content: str
    section_title: str
    source_path: str
    document_title: str
    category: str
    similarity: float
    source_type: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    count: int


class AddDocumentRequest(BaseModel):
    title: str
    content: str
    category: str = "dynamic"
    source_id: Optional[str] = None
    metadata: Optional[dict] = None


class SyncRequest(BaseModel):
    force: bool = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_db():
    """Raise 503 if the database isn't ready."""
    if not db.is_ready():
        raise HTTPException(
            status_code=503,
            detail="RAG database not initialized. Check DATABASE_URL and pgvector extension."
        )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/rag/health")
def health():
    return {
        "status": "ok",
        "service": "revx-rag",
        "db_ready": db.is_ready(),
    }


@app.post("/rag/search", response_model=SearchResponse)
def search(req: SearchRequest):
    """Semantic search across the knowledge base."""
    _check_db()
    try:
        query_embedding = embeddings.embed_one(req.query)
    except Exception as e:
        log.error(f"Embedding failed: {e}")
        raise HTTPException(status_code=502, detail=f"Embedding failed: {e}")

    try:
        results = db.search(
            query_embedding=query_embedding,
            top_k=req.top_k,
            category=req.category,
        )
    except Exception as e:
        log.error(f"Search query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    return SearchResponse(
        query=req.query,
        results=[
            SearchResult(
                content=r["content"],
                section_title=r["section_title"] or "",
                source_path=r["source_path"],
                document_title=r["title"] or "",
                category=r["category"] or "",
                similarity=round(float(r["similarity"]), 4),
                source_type=r["source_type"],
            )
            for r in results
        ],
        count=len(results),
    )


@app.post("/rag/sync")
def sync_knowledge(req: SyncRequest = SyncRequest()):
    """Sync markdown knowledge files from disk into the database."""
    _check_db()
    try:
        result = sync_module.sync_knowledge(force=req.force)
        return result
    except Exception as e:
        log.error(f"Sync failed: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {e}")


@app.post("/rag/documents")
def add_document(req: AddDocumentRequest):
    """Add a dynamic document (runtime knowledge, not from a file)."""
    _check_db()
    try:
        result = sync_module.add_dynamic_document(
            title=req.title,
            content=req.content,
            category=req.category,
            source_id=req.source_id,
            metadata=req.metadata,
        )
        return result
    except Exception as e:
        log.error(f"Add document failed: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Add document failed: {e}")


@app.delete("/rag/documents/{doc_id}")
def delete_document(doc_id: int):
    """Delete a document and all its chunks."""
    _check_db()
    try:
        db.delete_document(doc_id)
        return {"deleted": doc_id}
    except Exception as e:
        log.error(f"Delete failed: {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {e}")


@app.get("/rag/documents")
def list_documents(category: Optional[str] = None):
    """List all documents in the knowledge base."""
    _check_db()
    try:
        docs = db.list_documents(category=category)
        for d in docs:
            for key in ("created_at", "updated_at"):
                if d.get(key):
                    d[key] = str(d[key])
        return {"documents": docs, "count": len(docs)}
    except Exception as e:
        log.error(f"List documents failed: {e}")
        raise HTTPException(status_code=500, detail=f"List documents failed: {e}")


@app.get("/rag/stats")
def stats():
    """Knowledge base statistics."""
    _check_db()
    try:
        return db.get_stats()
    except Exception as e:
        log.error(f"Stats failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats failed: {e}")


@app.get("/rag/debug")
def debug():
    """Debug endpoint — test DB connection and report errors."""
    info = {
        "db_ready": db.is_ready(),
        "db_url_set": bool(db._connection_url),
        "db_url_preview": db._connection_url[:30] + "..." if db._connection_url else None,
    }

    # Test raw connection
    try:
        conn = db.get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            info["pg_version"] = cur.fetchone()[0]
            cur.execute("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector'")
            row = cur.fetchone()
            info["pgvector_installed"] = row is not None
            info["pgvector_version"] = row[1] if row else None
            cur.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name LIKE 'rag_%'
            """)
            info["rag_tables"] = [r[0] for r in cur.fetchall()]
        conn.close()
        info["connection"] = "ok"
    except Exception as e:
        info["connection"] = "failed"
        info["error"] = str(e)

    return info


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    log.info("Initializing RAG database schema...")
    try:
        db.init_schema()
        log.info("RAG database ready")
    except Exception as e:
        log.error(f"Failed to initialize RAG database: {e}")
        log.error(f"Detail: {traceback.format_exc()}")
        log.error("RAG search will not be available until database issue is resolved.")
        log.error("Use GET /rag/debug to diagnose.")
