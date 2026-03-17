"""RAG service configuration."""

import os

# Database
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Google Embeddings
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMS = 768

# Server
RAG_PORT = int(os.environ.get("RAG_PORT", "8081"))

# Chunking
CHUNK_MAX_CHARS = 1500
CHUNK_MIN_CHARS = 80
CHUNK_OVERLAP_CHARS = 200

# Knowledge directory (baked into container)
KNOWLEDGE_DIR = os.environ.get(
    "KNOWLEDGE_DIR", "/home/node/.openclaw/workspace/knowledge"
)

# Search defaults
DEFAULT_TOP_K = 5
MAX_TOP_K = 20
