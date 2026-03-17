# Salesforce Architecture — Sanguine Bio

## Org Landscape

| Alias | Type | Purpose |
|-------|------|---------|
| prod | Production (DevHub) | Live business operations |
| dev | Sandbox (Developer) | Primary development environment |
| qa | Sandbox (Developer) | Pre-production validation |
| b2cdev | Sandbox (Developer) | B2C Commerce development |

## Deployment Pipeline

```
dev sandbox → GitHub PR → QA sandbox → manual review → Production
```

- **Source control:** GitHub (`sanguinebio/salesforce` repository)
- **Delta deployments:** sfdx-git-delta compares git commits to build minimal deployment packages
- **CI/CD:** GitHub Actions runs validation on PR, deploys to QA on merge
- **Production:** Manual deployment only — never automated to prod

## Key Technologies

### Apex
Server-side custom logic. Used for:
- Complex business rules that can't be handled by Flows
- Trigger handlers (bulkified pattern)
- REST/SOAP API integrations
- Batch and scheduled jobs

### Lightning Web Components (LWC)
Custom UI components for both internal users and Experience Cloud portals.

### Salesforce Flows
Declarative automation for record-triggered logic, screen flows, and scheduled processes.

### Experience Cloud
External-facing portals for partner sites and potentially donors.

## Custom Objects

*(To be documented as RevX inspects the org — use `rag add` to populate this dynamically)*

## Integrations

*(To be documented — n8n workflows, external APIs, etc.)*
