#!/bin/bash
# RAG CLI — wrapper for RevX to interact with the knowledge base
# Usage:
#   rag search "how does the pricing calculator work?"
#   rag search "salesforce objects" --category salesforce --top 3
#   rag sync [--force]
#   rag add --title "Title" --category "cat" --content "markdown content"
#   rag sources [--category salesforce]
#   rag stats

RAG_URL="${RAG_URL:-http://127.0.0.1:8081}"
CMD="${1:-help}"
shift

case "$CMD" in
  search)
    QUERY="$1"
    shift
    TOP_K=5
    CATEGORY=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --top|-k) TOP_K="$2"; shift 2 ;;
        --category|-c) CATEGORY="$2"; shift 2 ;;
        *) shift ;;
      esac
    done

    BODY="{\"query\": \"$QUERY\", \"top_k\": $TOP_K"
    if [ -n "$CATEGORY" ]; then
      BODY="$BODY, \"category\": \"$CATEGORY\""
    fi
    BODY="$BODY}"

    RESPONSE=$(curl -s -X POST "$RAG_URL/rag/search" \
      -H "Content-Type: application/json" \
      -d "$BODY")

    # Pretty-print results
    COUNT=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('count',0))" 2>/dev/null)
    
    if [ "$COUNT" = "0" ] || [ -z "$COUNT" ]; then
      echo "No results found for: $QUERY"
      exit 0
    fi

    echo "=== RAG Search: \"$QUERY\" — $COUNT results ==="
    echo ""
    echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for i, r in enumerate(data.get('results', []), 1):
    sim = r.get('similarity', 0)
    print(f'--- [{i}] {r[\"document_title\"]} > {r[\"section_title\"]} (score: {sim:.3f}) ---')
    print(f'Source: {r[\"source_path\"]} [{r[\"category\"]}]')
    print(r['content'][:800])
    print()
"
    ;;

  sync)
    FORCE="false"
    if [ "$1" = "--force" ]; then
      FORCE="true"
    fi
    curl -s -X POST "$RAG_URL/rag/sync" \
      -H "Content-Type: application/json" \
      -d "{\"force\": $FORCE}" | python3 -m json.tool
    ;;

  add)
    TITLE="" CATEGORY="dynamic" CONTENT=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --title|-t) TITLE="$2"; shift 2 ;;
        --category|-c) CATEGORY="$2"; shift 2 ;;
        --content) CONTENT="$2"; shift 2 ;;
        --file|-f) CONTENT=$(cat "$2"); shift 2 ;;
        *) shift ;;
      esac
    done
    
    if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
      echo "Usage: rag add --title \"Title\" --content \"markdown\" [--category cat]"
      echo "       rag add --title \"Title\" --file /path/to/file.md [--category cat]"
      exit 1
    fi

    # Use python to safely JSON-encode the content
    python3 -c "
import json, sys, subprocess
body = json.dumps({'title': '''$TITLE''', 'content': sys.stdin.read(), 'category': '''$CATEGORY'''})
import urllib.request
req = urllib.request.Request('$RAG_URL/rag/documents', data=body.encode(), headers={'Content-Type': 'application/json'}, method='POST')
resp = urllib.request.urlopen(req)
print(json.dumps(json.loads(resp.read()), indent=2))
" <<< "$CONTENT"
    ;;

  sources|documents)
    CATEGORY=""
    if [ "$1" = "--category" ] || [ "$1" = "-c" ]; then
      CATEGORY="?category=$2"
    fi
    curl -s "$RAG_URL/rag/documents$CATEGORY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
docs = data.get('documents', [])
print(f'Knowledge Base: {len(docs)} documents')
print()
for d in docs:
    chunks = d.get('chunk_count', 0)
    cat = d.get('category', '?')
    src = d.get('source_type', '?')
    print(f'  [{d[\"id\"]}] {d[\"title\"]}  ({cat}, {src}, {chunks} chunks)')
    print(f'       {d[\"source_path\"]}')
"
    ;;

  stats)
    curl -s "$RAG_URL/rag/stats" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Documents: {data[\"documents\"]}')
print(f'Chunks:    {data[\"chunks\"]}')
print('Categories:')
for c in data.get('categories', []):
    print(f'  {c[\"category\"]}: {c[\"count\"]}')
"
    ;;

  health)
    curl -s "$RAG_URL/rag/health" | python3 -m json.tool
    ;;

  *)
    echo "RevX RAG Knowledge Base"
    echo ""
    echo "Usage: rag <command> [options]"
    echo ""
    echo "Commands:"
    echo "  search <query> [-k top_k] [-c category]   Semantic search"
    echo "  sync [--force]                             Sync markdown files to DB"
    echo "  add --title T --content C [-c category]    Add dynamic knowledge"
    echo "  add --title T --file F [-c category]       Add from file"
    echo "  sources [-c category]                      List all documents"
    echo "  stats                                      Knowledge base stats"
    echo "  health                                     Check RAG service health"
    ;;
esac
