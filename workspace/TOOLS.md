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

## Environment

- Container OS: Debian Bookworm (Node 22)
- SF CLI: latest (installed at build)
- Python 3: available for scripting
- Git: available for delta operations

---

*Add org-specific notes, user IDs, and common operations as you learn them.*
