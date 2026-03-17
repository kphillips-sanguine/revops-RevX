"""Markdown document chunker for RAG ingestion."""

import os
import re
from pathlib import Path

from .config import CHUNK_MAX_CHARS, CHUNK_MIN_CHARS


def extract_title(content: str) -> str:
    """Extract the first H1 title from markdown, or return empty string."""
    match = re.match(r"^#\s+(.+)", content.strip())
    return match.group(1).strip() if match else ""


def extract_category(file_path: str, knowledge_dir: str) -> str:
    """Derive category from the subdirectory name.
    
    knowledge/salesforce/objects.md → "salesforce"
    knowledge/business/overview.md → "business"
    knowledge/standalone.md → "general"
    """
    rel = os.path.relpath(file_path, knowledge_dir)
    parts = Path(rel).parts
    if len(parts) > 1:
        return parts[0]
    return "general"


def chunk_markdown(content: str, source_path: str = "") -> list[dict]:
    """Split markdown content into chunks by headers.
    
    Returns list of {content, section_title, metadata}.
    Large sections are further split by paragraphs.
    """
    chunks = []
    
    # Split by ## and ### headers
    # Keep track of header hierarchy for context
    sections = _split_by_headers(content)
    
    for section in sections:
        section_text = section["content"].strip()
        if len(section_text) < CHUNK_MIN_CHARS:
            continue
        
        if len(section_text) <= CHUNK_MAX_CHARS:
            chunks.append({
                "content": _add_header_context(section_text, section["headers"]),
                "section_title": section["title"],
                "metadata": {"headers": section["headers"], "source": source_path},
            })
        else:
            # Split large sections by paragraphs
            sub_chunks = _split_by_paragraphs(section_text, CHUNK_MAX_CHARS)
            for j, sub in enumerate(sub_chunks):
                if len(sub.strip()) < CHUNK_MIN_CHARS:
                    continue
                chunks.append({
                    "content": _add_header_context(sub.strip(), section["headers"]),
                    "section_title": f"{section['title']} (part {j+1})",
                    "metadata": {
                        "headers": section["headers"],
                        "source": source_path,
                        "part": j + 1,
                    },
                })
    
    return chunks


def _split_by_headers(content: str) -> list[dict]:
    """Split markdown into sections based on ## and ### headers."""
    lines = content.split("\n")
    sections = []
    current_h1 = ""
    current_h2 = ""
    current_title = ""
    current_lines = []
    
    for line in lines:
        h1_match = re.match(r"^#\s+(.+)", line)
        h2_match = re.match(r"^##\s+(.+)", line)
        h3_match = re.match(r"^###\s+(.+)", line)
        
        if h2_match or h3_match:
            # Flush current section
            if current_lines:
                sections.append({
                    "title": current_title or current_h2 or current_h1 or "Introduction",
                    "headers": [h for h in [current_h1, current_h2] if h],
                    "content": "\n".join(current_lines),
                })
                current_lines = []
            
            if h2_match:
                current_h2 = h2_match.group(1).strip()
                current_title = current_h2
            elif h3_match:
                current_title = h3_match.group(1).strip()
        elif h1_match:
            # Flush
            if current_lines:
                sections.append({
                    "title": current_title or current_h1 or "Introduction",
                    "headers": [h for h in [current_h1] if h],
                    "content": "\n".join(current_lines),
                })
                current_lines = []
            current_h1 = h1_match.group(1).strip()
            current_h2 = ""
            current_title = current_h1
        
        current_lines.append(line)
    
    # Flush remaining
    if current_lines:
        sections.append({
            "title": current_title or current_h1 or "Document",
            "headers": [h for h in [current_h1, current_h2] if h],
            "content": "\n".join(current_lines),
        })
    
    return sections


def _split_by_paragraphs(text: str, max_chars: int) -> list[str]:
    """Split text by paragraphs, merging small ones together up to max_chars."""
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = ""
    
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current)
            current = para
        else:
            current = current + "\n\n" + para if current else para
    
    if current:
        chunks.append(current)
    
    return chunks


def _add_header_context(text: str, headers: list[str]) -> str:
    """Prepend header breadcrumb if the chunk doesn't already start with one."""
    if not headers:
        return text
    if text.startswith("#"):
        return text
    breadcrumb = " > ".join(headers)
    return f"[Context: {breadcrumb}]\n\n{text}"


def discover_markdown_files(knowledge_dir: str) -> list[str]:
    """Find all .md files in the knowledge directory (recursive)."""
    files = []
    for root, _dirs, filenames in os.walk(knowledge_dir):
        for fn in sorted(filenames):
            if fn.lower().endswith(".md") and fn.upper() != "README.MD":
                files.append(os.path.join(root, fn))
    return files
