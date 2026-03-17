"""Google text-embedding-004 via REST API — no heavy SDK needed."""

import logging
import time

import requests

from .config import GOOGLE_API_KEY, EMBEDDING_MODEL

log = logging.getLogger("rag.embeddings")

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
BATCH_SIZE = 100  # Google allows up to 100 per batch request


def embed_one(text: str) -> list[float]:
    """Embed a single text string."""
    resp = requests.post(
        f"{API_BASE}/{EMBEDDING_MODEL}:embedContent",
        params={"key": GOOGLE_API_KEY},
        json={
            "model": f"models/{EMBEDDING_MODEL}",
            "content": {"parts": [{"text": text}]},
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]["values"]


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts using the batch API. Handles chunking for large batches."""
    if not texts:
        return []

    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        body = {
            "requests": [
                {
                    "model": f"models/{EMBEDDING_MODEL}",
                    "content": {"parts": [{"text": t}]},
                }
                for t in batch
            ]
        }

        resp = requests.post(
            f"{API_BASE}/{EMBEDDING_MODEL}:batchEmbedContents",
            params={"key": GOOGLE_API_KEY},
            json=body,
            timeout=60,
        )

        if resp.status_code == 429:
            # Rate limited — back off and retry once
            retry_after = int(resp.headers.get("Retry-After", 5))
            log.warning(f"Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = requests.post(
                f"{API_BASE}/{EMBEDDING_MODEL}:batchEmbedContents",
                params={"key": GOOGLE_API_KEY},
                json=body,
                timeout=60,
            )

        resp.raise_for_status()
        embeddings = [e["values"] for e in resp.json()["embeddings"]]
        all_embeddings.extend(embeddings)

        if i + BATCH_SIZE < len(texts):
            time.sleep(0.2)  # gentle pacing between batches

    return all_embeddings
