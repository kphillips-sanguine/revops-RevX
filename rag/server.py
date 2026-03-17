"""RAG HTTP API — runs as sidecar alongside OpenClaw gateway."""

import logging
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
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/rag/health")
def health():
    return {"status": "ok", "service": "revx-rag"}


@app.post("/rag/search", response_model=SearchResponse)
def search(req: SearchRequest):
    """Semantic search across the knowledge base."""
    try:
        query_embedding = embeddings.embed_one(req.query)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding failed: {e}")

    results = db.search(
        query_embedding=query_embedding,
        top_k=req.top_k,
        category=req.category,
    )

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
    result = sync_module.sync_knowledge(force=req.force)
    return result


@app.post("/rag/documents")
def add_document(req: AddDocumentRequest):
    """Add a dynamic document (runtime knowledge, not from a file)."""
    result = sync_module.add_dynamic_document(
        title=req.title,
        content=req.content,
        category=req.category,
        source_id=req.source_id,
        metadata=req.metadata,
    )
    return result


@app.delete("/rag/documents/{doc_id}")
def delete_document(doc_id: int):
    """Delete a document and all its chunks."""
    db.delete_document(doc_id)
    return {"deleted": doc_id}


@app.get("/rag/documents")
def list_documents(category: Optional[str] = None):
    """List all documents in the knowledge base."""
    docs = db.list_documents(category=category)
    # Convert datetime objects to strings for JSON serialization
    for d in docs:
        for key in ("created_at", "updated_at"):
            if d.get(key):
                d[key] = str(d[key])
    return {"documents": docs, "count": len(docs)}


@app.get("/rag/stats")
def stats():
    """Knowledge base statistics."""
    return db.get_stats()


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
        log.error("RAG search will not be available until database is configured")
