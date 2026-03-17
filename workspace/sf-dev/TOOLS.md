# TOOLS.md — SF Dev Agent

## Salesforce CLI

**Org aliases:**
- `prod` — Production (READ + Support RevOps Cases only)
- `dev` — Development sandbox (default target)
- `qa` — QA sandbox

**Common commands:**
```bash
# Retrieve metadata from an org
sf project retrieve start --metadata ApexClass:MyClass --target-org dev

# Deploy metadata to an org
sf project deploy start --source-dir force-app --target-org dev

# Run specific test class
sf apex run test --class-names MyClassTest --target-org dev --result-format human

# Run all local tests
sf apex run test --test-level RunLocalTests --target-org dev --result-format human

# Execute anonymous Apex
echo "System.debug('hello');" | sf apex run --target-org dev

# Query data
sf data query --query "SELECT Id, Name FROM Account LIMIT 5" --target-org dev

# Create a scratch org (if needed)
sf org create scratch --definition-file config/project-scratch-def.json --alias scratch --duration-days 7
```

## Git

**Repo location:** `/home/node/.openclaw/workspace/salesforce/`
**Remote:** `https://github.com/sanguinebio/salesforce.git`

```bash
# Standard workflow
cd /home/node/.openclaw/workspace/salesforce
git checkout main && git pull
git checkout -b feature/my-feature
# ... make changes ...
git add -A && git commit -m "feat(scope): description"
git push origin feature/my-feature

# Create PR via GitHub CLI (if available) or provide link
gh pr create --title "feat: description" --body "Details..."
```

## sfdx-git-delta

For generating deployment packages based on git diffs:
```bash
# Generate delta package between branches
sf sgd source delta --from origin/main --to HEAD --output delta-package/

# Deploy only the delta
sf project deploy start --manifest delta-package/package/package.xml --target-org qa
```

## RAG Knowledge Base

Search the knowledge base for Salesforce documentation:
```bash
# Search via CLI
rag search "how to create a platform event"

# Or via API
curl -s http://127.0.0.1:8081/rag/search -H "Content-Type: application/json" \
  -d '{"query": "platform event trigger", "limit": 5}'
```
