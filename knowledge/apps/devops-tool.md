# SF DevOps Tool

## Overview
Salesforce CI/CD pipeline for managing changes between orgs. Extends the existing Case Gantt/Kanban application.

## Status
- **Phase 1:** Code complete (metadata, Apex methods, LWC DevOps panel, test class)
- **Phase 2:** Next — details TBD

## Architecture

```
Salesforce LWC (DevOps Panel)
  → Apex Controller
  → Source_Change__c records
  → n8n webhook (https://n8n-z5fpv.sevalla.app)
  → Sevalla Proxy (https://sevalla-ru8at.sevalla.app)
  → SF CLI / git operations
  → Status callback to Salesforce
```

### Components
1. **LWC DevOps Panel** — UI for triggering and monitoring deployments
2. **Apex Controller** — Backend for DevOps operations
3. **Source_Change__c** — Tracks metadata changes
4. **n8n Workflows** — Orchestrates deployment steps
5. **Sevalla Proxy** — Docker container with SF CLI + git for CLI operations

### Infrastructure
- **n8n:** https://n8n-z5fpv.sevalla.app — workflow automation
- **Sevalla proxy:** https://sevalla-ru8at.sevalla.app — SF CLI + git operations
- **Proxy source:** `C:\Code\sevalla` (Docker on Sevalla VPS)

## Design
- **Design doc:** `C:\code\sf-devops-tool\DESIGN.md`
- **18 tasks across 4 phases** (~5 weeks estimated)
- Extends existing Kanban app, not a rebuild

## Key Decision
Build on existing `case-gant` codebase rather than starting from scratch. The Kanban LWC, Source_Change__c object, and n8n infrastructure are already in place.
