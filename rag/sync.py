"""Sync markdown knowledge files → PostgreSQL + embeddings."""

import logging
import os

from . import db, embeddings, chunker
from .config import KNOWLEDGE_DIR

log = logging.getLogger("rag.sync")


def sync_knowledge(knowledge_dir: str = None, force: bool = False) -> dict:
    """Sync all markdown files from knowledge_dir into the database.
    
    - New files: chunk → embed → insert
    - Changed files (hash mismatch): re-chunk → re-embed → replace
    - Deleted files: remove from DB
    - Unchanged files: skip (unless force=True)
    
    Returns summary dict.
    """
    knowledge_dir = knowledge_dir or KNOWLEDGE_DIR
    
    if not os.path.isdir(knowledge_dir):
        log.warning(f"Knowledge directory not found: {knowledge_dir}")
        return {"error": f"Directory not found: {knowledge_dir}"}
    
    files = chunker.discover_markdown_files(knowledge_dir)
    log.info(f"Found {len(files)} markdown files in {knowledge_dir}")
    
    results = {"added": 0, "updated": 0, "unchanged": 0, "removed": 0, "errors": []}
    active_paths = set()
    
    for file_path in files:
        rel_path = os.path.relpath(file_path, knowledge_dir)
        active_paths.add(rel_path)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check if document exists and is unchanged
            existing = db.get_document(rel_path, source_type="file")
            new_hash = db.content_hash(content)
            
            if existing and existing["content_hash"] == new_hash and not force:
                results["unchanged"] += 1
                log.debug(f"Unchanged: {rel_path}")
                continue
            
            action = "updated" if existing else "added"
            
            # Extract metadata
            title = chunker.extract_title(content) or os.path.splitext(os.path.basename(file_path))[0]
            category = chunker.extract_category(file_path, knowledge_dir)
            
            # Upsert document record
            doc_id = db.upsert_document(
                source_path=rel_path,
                title=title,
                category=category,
                content=content,
                source_type="file",
                metadata={"file_path": file_path},
            )
            
            # Remove old chunks
            db.delete_chunks_for_document(doc_id)
            
            # Chunk the content
            chunks = chunker.chunk_markdown(content, source_path=rel_path)
            
            if not chunks:
                log.warning(f"No chunks produced for {rel_path}")
                results[action] += 1
                continue
            
            # Embed all chunks in one batch call
            texts = [c["content"] for c in chunks]
            chunk_embeddings = embeddings.embed_batch(texts)
            
            # Attach embeddings to chunks
            for chunk, emb in zip(chunks, chunk_embeddings):
                chunk["embedding"] = emb
            
            # Store chunks
            db.insert_chunks(doc_id, chunks)
            
            results[action] += 1
            log.info(f"{action.capitalize()}: {rel_path} ({len(chunks)} chunks)")
            
        except Exception as e:
            log.error(f"Error processing {rel_path}: {e}")
            results["errors"].append({"file": rel_path, "error": str(e)})
    
    # Remove documents for files that no longer exist
    removed = db.remove_stale_file_documents(active_paths)
    results["removed"] = removed
    
    log.info(
        f"Sync complete: {results['added']} added, {results['updated']} updated, "
        f"{results['unchanged']} unchanged, {results['removed']} removed, "
        f"{len(results['errors'])} errors"
    )
    
    return results


def add_dynamic_document(title: str, content: str, category: str = "dynamic",
                         source_id: str = None, metadata: dict = None) -> dict:
    """Add a document dynamically (not from a file).
    
    Used by RevX to store knowledge learned at runtime.
    """
    source_path = source_id or f"dynamic/{title.lower().replace(' ', '-')}"
    
    doc_id = db.upsert_document(
        source_path=source_path,
        title=title,
        category=category,
        content=content,
        source_type="dynamic",
        metadata=metadata or {},
    )
    
    # Remove old chunks and re-embed
    db.delete_chunks_for_document(doc_id)
    
    chunks = chunker.chunk_markdown(content, source_path=source_path)
    if chunks:
        texts = [c["content"] for c in chunks]
        chunk_embeddings = embeddings.embed_batch(texts)
        for chunk, emb in zip(chunks, chunk_embeddings):
            chunk["embedding"] = emb
        db.insert_chunks(doc_id, chunks)
    
    return {"document_id": doc_id, "chunks": len(chunks), "source_path": source_path}
