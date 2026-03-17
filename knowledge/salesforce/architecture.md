# Salesforce Architecture — Sanguine Bio

## Org Landscape

| Alias | Type | Purpose | Access Level |
|-------|------|---------|-------------|
| prod | Production (DevHub) | Live business operations | Read + Support RevOps Cases |
| dev | Sandbox (Developer) | Primary development environment | Full access |
| qa | Sandbox (Developer) | Pre-production validation | Full access |
| b2cdev | Sandbox (Developer) | B2C Commerce development | Full access |

## Deployment Pipeline

```
Developer → dev sandbox → GitHub PR → QA sandbox → manual review → Production
```

### Detailed Flow
1. Developer works in **dev sandbox** (or scratch org)
2. Code committed to feature branch in `sanguinebio/salesforce` repo
3. **Pull Request** created → GitHub Actions validates (runs tests, checks coverage)
4. PR merged to main → auto-deploys to **QA sandbox**
5. QA validation by team
6. Manual **production deployment** via CI pipeline (never automated to prod)

### Delta Deployments
- Uses **sfdx-git-delta** (`sf sgd source delta`) to generate minimal deployment packages
- Compares git commits to determine what changed
- Only deploys modified metadata, reducing deployment time and risk

## Key Technologies

### Apex
Server-side custom logic:
- Complex business rules that can't be handled by Flows
- **Trigger handler pattern** — one trigger per object, all logic in handler class
- REST/SOAP API integrations with external systems
- Batch and scheduled jobs for data processing
- Service layer pattern for reusable business logic

### Lightning Web Components (LWC)
Custom UI components:
- Internal user interfaces (case management, dashboards, tools)
- Experience Cloud portal components
- Follow container/presentational component architecture
- Wire service for read operations, imperative Apex for DML

### Salesforce Flows
Declarative automation:
- Record-triggered flows for field updates and notifications
- Screen flows for guided user processes
- Scheduled flows for periodic data operations
- Preferred over Apex for simple automation (maintainability)

### Experience Cloud
External-facing portals:
- Partner site portals
- Donor/patient portals (potential)
- Built with LWC components
- Separate guest user and community user profiles

## Source Control

### Repository
- **GitHub org:** sanguinebio
- **Main repo:** `sanguinebio/salesforce`
- **Branch strategy:** Feature branches → PR → main
- **Naming:** `feature/description`, `bugfix/case-description`, `hotfix/critical`

### CI/CD (GitHub Actions)
- **PR validation:** Runs Apex tests, checks coverage (>85%)
- **QA deploy:** Auto-deploys on merge to main
- **Prod deploy:** Manual trigger with approval gate
- **Note:** GitHub Free plan — rulesets don't enforce on private repos; use classic branch protection rules

## Integrations

### n8n Workflow Automation
- **Instance:** https://n8n-z5fpv.sevalla.app
- **Purpose:** Orchestrates workflows between Salesforce and external services
- **Pattern:** SF triggers/platform events → n8n webhook → process → callback to SF
- **Used for:** AI agent orchestration, data sync, notifications

### Sevalla Proxy
- **Instance:** https://sevalla-ru8at.sevalla.app
- **Purpose:** Hosts SF CLI + git for CI/CD operations
- **Source:** Docker on Sevalla VPS
- **Used by:** n8n workflows that need SF CLI access

### RevX (OpenClaw)
- **Instance:** https://revops-revx-ae440.sevalla.app
- **Purpose:** AI team assistant — project management, case tracking, development
- **Channel:** Slack (socket mode)
- **Agents:** RevX (coordinator), Spec Ops (requirements), Code Monkey (developer)
