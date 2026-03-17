# Knowledge Base

This directory contains the source-of-truth markdown files for RevX's RAG knowledge base.

## Structure

```
knowledge/
├── business/       # Company context, org structure, processes
├── salesforce/     # Objects, fields, flows, automations, architecture
├── apps/           # LWCs, Apex classes, integrations
└── runbooks/       # Deployment procedures, troubleshooting guides
```

## How It Works

1. Add or edit `.md` files in the appropriate subdirectory
2. Commit and push to trigger a container rebuild
3. On startup, the RAG sync script reads all files → chunks them → generates embeddings → stores in PostgreSQL
4. RevX searches this knowledge base semantically when it needs context

## Writing Good Knowledge Docs

- **Use clear headers** (`##`, `###`) — the chunker splits on these
- **One topic per file** — helps categorization and retrieval
- **Be specific** — "The Account object has a custom field `Revenue_Tier__c`" beats "we have some custom fields"
- **Include context** — why something exists, not just what it is
- **Keep files under 5000 words** — very long files produce many chunks and dilute relevance

## Manual Sync

RevX can trigger a re-sync at any time:
```
rag sync          # sync changed files only
rag sync --force  # re-embed everything
```

## Dynamic Knowledge

RevX can also store knowledge learned at runtime (from conversations, Salesforce metadata inspection, etc.) using `rag add`. These are stored as "dynamic" documents in the database and persist across container rebuilds.
