# TOOLS.md - RevX Local Notes

## Salesforce CLI

**Org aliases:**
- `prod` — Production (DevHub)
- `dev` — Dev sandbox
- `qa` — QA sandbox
- `b2cdev` — B2C Dev sandbox

**Common queries:**
```bash
# List recent deployments
sf project deploy report --target-org <alias>

# Check org limits
sf limits api display --target-org <alias>

# Run all tests
sf apex run test --target-org <alias> --wait 10

# Retrieve metadata
sf project retrieve start --target-org <alias> -m "ApexClass:ClassName"

# Delta deployment (sfdx-git-delta)
sf sgd source delta --from <commit> --to HEAD --output .
```

## sfdx-git-delta

Installed as SF CLI plugin. Use `sf sgd source delta` (not standalone `sgd`).

## RAG Knowledge Base

RevX has a semantic search knowledge base powered by PostgreSQL + pgvector + Google embeddings.

**CLI tool: `rag`**

```bash
# Search the knowledge base (semantic / AI-powered)
rag search "how does the pricing calculator work?"
rag search "salesforce objects" --category salesforce --top 3

# Sync markdown knowledge files from disk → database
rag sync              # only changed files
rag sync --force      # re-embed everything

# Add runtime knowledge (persists in DB across container rebuilds)
rag add --title "New Integration" --category "apps" --content "## Details\n..."
rag add --title "Troubleshooting Guide" --file /tmp/guide.md --category "runbooks"

# List all knowledge documents
rag sources
rag sources --category salesforce

# Stats
rag stats

# Health check
rag health
```

**When to use RAG search:**
- Before answering questions about business processes, architecture, or Salesforce config
- When you need context about how something works at Sanguine Bio
- When a team member asks about something that might be documented

**When to add knowledge:**
- After discovering something important about an org (object relationships, flow logic, etc.)
- After resolving a tricky issue (add a runbook entry)
- When a team member shares institutional knowledge worth preserving

**Knowledge sources (baked into container):**
- `knowledge/business/` — Company context, org structure, processes
- `knowledge/salesforce/` — Objects, fields, flows, architecture
- `knowledge/apps/` — LWCs, Apex classes, integrations
- `knowledge/runbooks/` — Deployment procedures, troubleshooting

**API (advanced):**
- RAG service runs at `http://127.0.0.1:8081`
- Docs: `http://127.0.0.1:8081/rag/docs`
- Search: `POST /rag/search {"query": "...", "top_k": 5, "category": "..."}`
- Add: `POST /rag/documents {"title": "...", "content": "...", "category": "..."}`

## Environment

- Container OS: Debian Bookworm (Node 22)
- SF CLI: latest (installed at build)
- Python 3: available for scripting
- Git: available for delta operations
- RAG service: FastAPI on port 8081 (internal only)

---

*Add org-specific notes, user IDs, and common operations as you learn them.*
