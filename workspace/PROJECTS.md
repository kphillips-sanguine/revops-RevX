# Active Projects

*RevX checks this file every session for current project context.*
*When a project completes, move a summary to MEMORY.md and remove it from here.*

<!-- last-reviewed: 2026-03-17 -->

---

## 🔥 RevX — Team OpenClaw on Sevalla
- **Case:** *(add Case Number)*
- **Goal:** OpenClaw Gateway deployment for Sanguine Bio team
- **Status:** Live — ongoing improvements
- **Org:** prod (read-only), dev, qa
- **Repo:** `https://github.com/kphillips-sanguine/revops-RevX.git`
- **Live URL:** `https://revops-revx-ae440.sevalla.app`
- **Key context:** Docker on Sevalla, auto-deploys on push. Agent named "RevX". Slack channel enabled. RAG knowledge base for SF docs.
- **Current focus:** Fixing workspace persistence, adding project context
- **Next steps:** *(update as needed)*

## 🛠️ SF DevOps Tool
- **Case:** *(add Case Number)*
- **Goal:** Salesforce CI/CD pipeline for managing changes between orgs
- **Status:** Phase 1 code complete — Phase 2 next
- **Org:** dev, qa, prod
- **Repo/Path:** `sanguinebio/salesforce` — existing caseGanttChart app
- **Key context:** Extends existing Kanban LWC. Uses n8n + proxy on Sevalla for SF CLI/git operations.
- **Next steps:** Phase 2 implementation

## 🤖 SF Admin Agent
- **Case:** *(add Case Number)*
- **Goal:** 95% Salesforce production support automation via AI agents
- **Status:** Planning complete (PLAN.md v0.2) — ready to scaffold
- **Org:** dev (development), prod (target)
- **Repo/Path:** `sanguinebio/salesforce` (sf-admin-agent subfolder)
- **Key context:** Multi-agent architecture (Coordinator → Admin/DevOps/Case agents). Claude Agent SDK + Node.js/React. Two human checkpoints required.
- **Next steps:** Scaffold project structure

## ⚡ SF Agent Framework
- **Case:** *(add Case Number)*
- **Goal:** Salesforce-native AI agent with Gemini LLM, LWC chat UI, n8n orchestration
- **Status:** Design v0.1 complete — ready for review
- **Org:** dev
- **Repo/Path:** *(add path)*
- **Key context:** Data-driven tools (Agent_Tool_Definition__c). Gemini 2.0 Flash. Platform Events for real-time.
- **Next steps:** Design review, then build

---

## Salesforce Case Integration

RevX can sync project status with Salesforce Cases:

### How it works
- Each project links to a SF Case via **Case Number** above
- During heartbeats, RevX can check case status/comments for updates from the team
- When RevX makes progress or decisions, it posts a Case Comment summarizing what happened
- Team members see updates in Salesforce without needing Slack/OpenClaw access

### Commands RevX uses
```bash
# Check case details
sf data query --query "SELECT Id, CaseNumber, Subject, Status, Priority, Description FROM Case WHERE CaseNumber = 'XXXXX'" --target-org prod

# Get recent case comments
sf data query --query "SELECT Id, CommentBody, CreatedDate, CreatedBy.Name FROM CaseComment WHERE ParentId = 'CASE_ID' ORDER BY CreatedDate DESC LIMIT 5" --target-org prod

# Post a case comment (requires appropriate permissions)
sf data create record --sobject CaseComment --values "ParentId='CASE_ID' CommentBody='[RevX] Status update: ...'" --target-org prod
```

### Guidelines
- Prefix comments with `[RevX]` so team knows it's from the agent
- Keep comments concise — decisions made, blockers hit, milestones reached
- Don't spam — one comment per significant event, not every small change
- Check for new team comments during heartbeats to stay in sync
