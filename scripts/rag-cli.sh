#!/bin/bash
# RAG CLI — wrapper for RevX to interact with the knowledge base
# Usage:
#   rag search "how does the pricing calculator work?"
#   rag search "salesforce objects" --category salesforce --top 3
#   rag sync [--force]
#   rag add --title "Title" --category "cat" --content "markdown content"
#   rag sources [--category salesforce]
#   rag stats
#   rag debug

RAG_URL="${RAG_URL:-http://127.0.0.1:8081}"
CMD="${1:-help}"
shift

# Helper: make a request and handle errors
_request() {
  local METHOD="$1" URL="$2" BODY="$3"
  local RESPONSE HTTP_CODE

  if [ "$METHOD" = "GET" ]; then
    RESPONSE=$(curl -sw "\n%{http_code}" -X GET "$URL" 2>/dev/null)
  else
    RESPONSE=$(curl -sw "\n%{http_code}" -X "$METHOD" "$URL" \
      -H "Content-Type: application/json" \
      -d "$BODY" 2>/dev/null)
  fi

  # Split response body and HTTP code
  HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
  BODY_CONTENT=$(echo "$RESPONSE" | sed '$d')

  if [ -z "$BODY_CONTENT" ]; then
    echo "ERROR: Empty response from RAG service (HTTP $HTTP_CODE)"
    echo "Is the RAG service running? Try: curl -s $RAG_URL/rag/health"
    return 1
  fi

  if [ "$HTTP_CODE" -ge 400 ] 2>/dev/null; then
    echo "ERROR (HTTP $HTTP_CODE):"
    echo "$BODY_CONTENT" | python3 -m json.tool 2>/dev/null || echo "$BODY_CONTENT"
    return 1
  fi

  echo "$BODY_CONTENT"
  return 0
}

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

    RESPONSE=$(_request POST "$RAG_URL/rag/search" "$BODY") || exit 1

    # Pretty-print results
    echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f'JSON parse error: {e}')
    sys.exit(1)
count = data.get('count', 0)
if count == 0:
    print('No results found.')
    sys.exit(0)
print(f'=== RAG Search: \"{data.get(\"query\", \"\")}\" — {count} results ===')
print()
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
    RESPONSE=$(_request POST "$RAG_URL/rag/sync" "{\"force\": $FORCE}") || exit 1
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
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
import json, sys, urllib.request
content = sys.stdin.read()
body = json.dumps({'title': '$TITLE', 'content': content, 'category': '$CATEGORY'})
try:
    req = urllib.request.Request('$RAG_URL/rag/documents', data=body.encode(), headers={'Content-Type': 'application/json'}, method='POST')
    resp = urllib.request.urlopen(req)
    print(json.dumps(json.loads(resp.read()), indent=2))
except urllib.error.HTTPError as e:
    print(f'ERROR (HTTP {e.code}): {e.read().decode()}')
    sys.exit(1)
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" <<< "$CONTENT"
    ;;

  sources|documents)
    CATEGORY=""
    if [ "$1" = "--category" ] || [ "$1" = "-c" ]; then
      CATEGORY="?category=$2"
    fi
    RESPONSE=$(_request GET "$RAG_URL/rag/documents$CATEGORY") || exit 1
    echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f'JSON parse error: {e}')
    sys.exit(1)
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
    RESPONSE=$(_request GET "$RAG_URL/rag/stats") || exit 1
    echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f'JSON parse error: {e}')
    sys.exit(1)
print(f'Documents: {data[\"documents\"]}')
print(f'Chunks:    {data[\"chunks\"]}')
print('Categories:')
for c in data.get('categories', []):
    print(f'  {c[\"category\"]}: {c[\"count\"]}')
"
    ;;

  health)
    RESPONSE=$(_request GET "$RAG_URL/rag/health") || exit 1
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    ;;

  debug)
    echo "Running RAG diagnostics..."
    RESPONSE=$(_request GET "$RAG_URL/rag/debug") || exit 1
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    ;;

  crawl)
    echo "🔍 Running Schema Crawler..."
    /opt/scripts/schema-crawler.sh "$@"
    ;;

  *)
    echo "RevX RAG Knowledge Base"
    echo ""
    echo "Usage: rag <command> [options]"
    echo ""
    echo "Commands:"
    echo "  search <query> [-k top_k] [-c category]   Semantic search"
    echo "  sync [--force]                             Sync markdown files to DB"
    echo "  crawl [--org dev] [--output both] [--enhance]  Crawl SF org schema → RAG"
    echo "  add --title T --content C [-c category]    Add dynamic knowledge"
    echo "  add --title T --file F [-c category]       Add from file"
    echo "  sources [-c category]                      List all documents"
    echo "  stats                                      Knowledge base stats"
    echo "  health                                     Check RAG service health"
    echo "  debug                                      Diagnose DB connection + pgvector"
    ;;
esac
