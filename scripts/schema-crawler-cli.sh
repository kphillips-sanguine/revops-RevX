#!/bin/bash
# Wrapper for schema-crawler that RevX can call via: rag crawl [args]
# Installed alongside the rag CLI script

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/../scripts/schema-crawler.sh" "$@"
