# RevX Team Guide 🚀

*Everything you need to know about RevX and the AI agents powering Sanguine Bio's RevOps engineering.*

---

## What is RevX?

RevX is our AI team assistant built on OpenClaw. It lives in Slack and on the web at [revops-revx-ae440.sevalla.app](https://revops-revx-ae440.sevalla.app). Think of it as a team member that's always available — it tracks projects, answers Salesforce questions, writes code, and keeps everyone in the loop.

---

## The Agent Team

RevX isn't just one agent — it's a team of four, each with a specific role:

### ⚡ RevX — The Coordinator
**What it does:** Project management, case tracking, team communication, general questions.

**Talk to RevX when you need:**
- Project status updates
- Salesforce questions ("What fields are on the Case object?")
- Help with cases or tasks
- To kick off a new feature or project

**How to use it:**
- **Slack:** Message RevX directly or mention `@RevX` in the team channel
- **Web:** Chat at the RevX web portal

**Examples:**
> "What's the status of the DevOps Tool project?"
> "Check my open cases in Salesforce"
> "I need a new portal feature built — here are the requirements"

---

### 🎯 Spec Ops — The Requirements Agent
**What it does:** Gathers requirements, researches the Salesforce org, and produces detailed specification documents before any code is written.

**You'll interact with Spec Ops when:**
- Starting a new project or feature
- RevX delegates a requirements-gathering session to Spec Ops

**What to expect:**
1. Spec Ops asks you questions in organized batches (not one at a time)
2. It researches the existing org — fields, objects, components — so it doesn't ask you things it can look up
3. It produces a complete spec package that Code Monkey will build from

**What it produces:**
- `requirements.md` — What we're building and why
- `data-model.md` — Objects, fields, relationships
- `field-mapping.md` — Which fields map to which UI elements
- `ui-specs.md` — Page layouts, navigation, user flows
- `business-logic.md` — Validation rules, automation, calculations
- `permissions.md` — Who can access what
- `test-plan.md` — How we verify it works

---

### 🐒 Code Monkey — The Developer
**What it does:** Writes Apex, LWCs, and other Salesforce code. Runs tests, creates PRs, deploys to dev/QA.

**You'll see Code Monkey when:**
- RevX delegates a coding task
- A feature is ready to be built (specs are done)

**What it does automatically:**
- Follows our coding standards (trigger handler pattern, service layer, etc.)
- Writes test classes (85%+ coverage)
- Creates feature branches and PRs
- Updates progress so RevX can report back
- Maintains `CLAUDE.md` files for codebase documentation

**Important:** Code Monkey never deploys directly to production. Everything goes through the standard dev → QA → PR → prod pipeline.

---

### 🖱️ Click Ops — The Admin Agent
**What it does:** Handles declarative Salesforce admin changes — custom fields, page layouts, picklist values, and permissions. No code involved.

**Talk to Click Ops (through RevX) when you need:**
- A new custom field added to an object
- Fields added to or rearranged on a page layout
- New picklist values added (standard, custom, or global value sets)
- Field-level security or permission set updates
- Record type picklist value assignments changed

**What to expect:**
1. Click Ops researches the current state of the org (existing fields, layouts, permissions)
2. It retrieves the relevant metadata via SF CLI
3. It makes precise XML metadata changes
4. It deploys to dev first, verifies, then promotes as directed

**What it does NOT do:**
- Write Apex, LWC, or any code (that's Code Monkey's job)
- Build complex automation (Flows, Process Builder)
- Make changes directly to production without approval

**Examples:**
> "Add a 'Preferred Contact Method' picklist to the Contact object"
> "Add the new field to the Contact page layout"
> "Give the Sales team read access to the new field"
> "Add 'Referral' as a new Lead Source picklist value"

---

## The Workflow

Here's how a typical feature request flows through the system:

```
1. You tell RevX what you need
        ↓
2. RevX spawns Spec Ops to gather requirements
        ↓
3. Spec Ops interviews you + researches the org
        ↓
4. Spec Ops produces spec documents
        ↓
5. RevX spawns Code Monkey to build it
        ↓
6. Code Monkey writes code, runs tests, creates a PR
        ↓
7. RevX posts a [RevX] case comment with the status
        ↓
8. Team reviews the PR → merge → deploy to QA → validate → prod
```

You can jump in at any point. Not every request needs the full pipeline — asking RevX a quick Salesforce question skips straight to an answer.

---

## Knowledge Base (RAG)

RevX has a searchable knowledge base with documentation about our Salesforce org, coding patterns, business context, and operational procedures.

### What's in there:

| Category | Content |
|----------|---------|
| **Salesforce** | Architecture, Apex patterns, LWC patterns, governor limits, Experience Cloud, integrations, permissions |
| **Business** | Company overview, business glossary, team structure |
| **Apps** | Case Gantt/Kanban LWC, DevOps Tool documentation |
| **Runbooks** | Deploy to production, sandbox refresh, troubleshooting guide |
| **Org Schema** | Auto-generated object/field documentation from the live org |

### Asking RevX about the org:

RevX can search this knowledge base, so you can ask things like:
> "What custom fields are on the Account object?"
> "How do we deploy to production?"
> "What's the trigger handler pattern we use?"
> "How does the n8n integration work?"

### Schema Crawler

RevX can auto-generate documentation from the live Salesforce org:
> "Run the schema crawler on the dev org"

This pulls all objects, fields, record types, validation rules, and permission sets — then uses AI to write useful descriptions of everything. The docs land in the knowledge base so everyone benefits.

---

## Salesforce Case Integration

RevX connects projects to Salesforce Cases:

- **Each project** links to a Case number
- **RevX reads** case comments for team updates
- **RevX posts** `[RevX]` comments when significant progress is made
- **You'll see** comments like: `[RevX] Login page LWC complete — PR #42 ready for review`

This means the whole team sees progress in Salesforce without needing to be in Slack or the RevX portal.

---

## Project Tracking

RevX maintains a `PROJECTS.md` file with all active projects. Each project tracks:
- Goal and current status
- Linked Salesforce Case
- Which orgs are involved
- Repo/code location
- Current focus and next steps

Ask RevX anytime:
> "What are the active projects?"
> "What's the status of [project name]?"

---

## Tips & Best Practices

### Do's ✅
- **Be specific** — "Build an LWC that shows open Cases for the current Account" beats "make a case thing"
- **Provide context** — Share field lists, mockups, prototypes, or reference existing components
- **Review the specs** — When Spec Ops produces docs, review them before Code Monkey starts building. Catching issues in specs is 10x cheaper than catching them in code
- **Review PRs** — Code Monkey creates great code, but human review is always the final gate
- **Ask questions** — RevX knows the org, the codebase, and the architecture. Use it.

### Don'ts ❌
- **Don't skip specs** for anything non-trivial — it saves time in the long run
- **Don't bypass QA** — Even AI-written code needs validation in QA before prod
- **Don't share sensitive data** — RevX has access to org metadata and cases, but don't paste passwords or tokens into chat

### Quick Commands
| What you want | What to say |
|---------------|-------------|
| Check your cases | "Show my open cases" |
| Project status | "What are the active projects?" |
| Org question | "What fields are on [Object]?" |
| Start a feature | "I need to build [feature]. Here's what I need..." |
| Run schema crawler | "Crawl the dev org schema" |
| Deployment help | "How do I deploy to production?" |
| Troubleshooting | "I'm getting [error]. How do I fix it?" |

---

## Architecture (For the Curious)

```
┌─────────────────────────────────────────────┐
│              Sevalla VPS (Docker)             │
│                                               │
│  ⚡ RevX (Opus)          — Coordinator        │
│  🎯 Spec Ops (Sonnet 4)  — Requirements      │
│  🐒 Code Monkey (Sonnet 4) — Developer       │
│  🖱️ Click Ops (Sonnet 4)  — Admin            │
│  🧠 RAG Service           — Knowledge Base    │
│  🔧 SF CLI                — Org Access        │
│  📂 Git                   — Code Management   │
│                                               │
│  Channels: Slack (socket mode) + Web Portal   │
└─────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
   Salesforce Orgs      GitHub Repo
   (prod/dev/qa)     (sanguinebio/salesforce)
```

---

## Need Help?

- **Slack:** Message RevX directly
- **Web:** [revops-revx-ae440.sevalla.app](https://revops-revx-ae440.sevalla.app)
- **Issues:** Talk to Kevin Phillips

---

*Last updated: March 17, 2026*
