# TOOLS.md - RevX Local Notes

## Your Agents

You have two specialist agents you can delegate to. **Use them.** Don't try to write code or gather detailed specs yourself — that's their job.

### 🎯 Spec Ops — Requirements Agent
**When to use:** Any time a new feature, project, or significant change needs to be specced out.

```
sessions_spawn(agentId: "spec-ops", task: "Gather requirements for [description]. Here's what we know so far: [context]")
```

**What it does:**
- Interviews the user with targeted questions (in batches, not one at a time)
- Researches the existing SF org and codebase before asking questions
- Produces a complete spec package in `sf-dev/specs/{project-name}/`

**Give it:** Any docs, prototypes, field lists, or requirements the user provided.
**Get back:** Full spec package (requirements, data model, field mapping, UI specs, permissions, test plan).

### 🐒 Code Monkey — SF Developer Agent
**When to use:** When specs are ready and code needs to be written.

```
sessions_spawn(agentId: "sf-dev", task: "Build [feature] per specs in specs/[project-name]/. Deploy to dev org and create a PR.")
```

**What it does:**
- Reads spec documents, plans implementation
- Writes Apex, LWCs, metadata, test classes
- Follows coding standards (trigger handler, service layer, 85%+ coverage)
- Creates feature branches, commits, pushes, creates PRs
- Updates `PROGRESS.md` with status

**Give it:** The spec folder path and any additional context.
**Get back:** Working code, passing tests, a PR ready for review.

### The Typical Flow
```
User asks for something
  → You understand the request
  → Spawn Spec Ops with context → specs produced
  → Spawn Code Monkey with spec path → code built, PR created
  → You update the Case with a [RevX] comment
  → You report back to the user
```

For quick/simple requests (field change, small fix), you can skip Spec Ops and go straight to Code Monkey with clear instructions.

---

## RAG Knowledge Base

You have a searchable knowledge base. **Search it before answering questions** about SF architecture, business processes, org schema, or troubleshooting.

### Search
```bash
rag search "what fields are on the Case object"
rag search "how does the deploy pipeline work"
rag search "experience cloud portal setup" --category salesforce
rag search "team structure" --category business --top 3
```

### Schema Crawler — Generate Org Schema Docs
```bash
# Crawl dev org → writes files + pushes to RAG (raw data)
rag crawl --org dev --output both

# Crawl with AI enhancement (Gemini Flash enriches descriptions)
rag crawl --org dev --output both --enhance

# Crawl prod org
rag crawl --org prod --output both --enhance

# Crawl specific objects only
rag crawl --org dev --objects "Case,Account,Contact" --enhance
```

**When to crawl:**
- After a sandbox refresh (schema may have changed)
- When someone asks about objects/fields and search comes up empty
- Periodically (monthly) to keep schema docs current
- When starting a new project (crawl relevant objects)

### Add Knowledge at Runtime
```bash
# Add from text
rag add --title "New Integration Pattern" --category "salesforce" --content "## Details..."

# Add from a file
rag add --title "Meeting Notes" --file /tmp/notes.md --category "business"
```

**When to add knowledge:**
- After discovering something about the org (relationships, undocumented flows)
- After resolving a tricky issue (future troubleshooting reference)
- When a team member shares info worth preserving

### Other RAG Commands
```bash
rag sync              # Sync changed knowledge files to DB
rag sync --force      # Re-embed everything
rag sources           # List all documents in the knowledge base
rag stats             # Document/chunk counts by category
rag health            # Check if RAG service is running
rag debug             # Diagnose DB/pgvector issues
```

### What's in the Knowledge Base
| Category | Content |
|----------|---------|
| `salesforce` | Architecture, Apex patterns, LWC patterns, governor limits, Experience Cloud, integrations, permissions, org schema |
| `business` | Company overview, glossary, team structure |
| `apps` | Case Gantt/Kanban, DevOps Tool |
| `runbooks` | Deploy to prod, sandbox refresh, troubleshooting |

---

## Salesforce CLI

**Org aliases:**
- `prod` — Production (READ + Support RevOps Cases only)
- `dev` — Dev sandbox (default target)
- `qa` — QA sandbox
- `b2cdev` — B2C Dev sandbox

**Common commands:**
```bash
# Query data
sf data query --query "SELECT Id, Name FROM Account LIMIT 5" --target-org dev

# Kevin's open cases
sf data query --query "SELECT Id, CaseNumber, Subject, Status, Priority, CreatedDate FROM Case WHERE OwnerId = '005PW00000JHAhdYAH' AND IsClosed = false ORDER BY CreatedDate DESC LIMIT 20" --target-org prod

# Run tests
sf apex run test --test-level RunLocalTests --target-org dev --result-format human

# Deploy
sf project deploy start --source-dir force-app --target-org dev

# Retrieve
sf project retrieve start --metadata ApexClass:ClassName --target-org dev

# Check org limits
sf limits api display --target-org dev

# Delta deployment (sfdx-git-delta)
sf sgd source delta --from <commit> --to HEAD --output .
```

---

## Salesforce Case Comments

When posting updates to Cases:
```bash
# Post a [RevX] comment
sf data create record --sobject CaseComment --values "ParentId='CASE_ID' CommentBody='[RevX] Status update: ...'" --target-org prod
```

**Rules:**
- Always prefix with `[RevX]` so team knows it's from you
- Keep concise — decisions, milestones, blockers
- Don't spam — one comment per significant event

---

## Project Tracking

**PROJECTS.md** — Check this for active project status. Update it when projects change.

**Key files:**
- `PROJECTS.md` — Active projects with Case links
- `TEAM-GUIDE.md` — Team onboarding doc (share with new team members)
- `sf-dev/PROGRESS.md` — Code Monkey's task tracker
- `sf-dev/specs/` — Spec packages from Spec Ops

---

## Browser — Headless Chromium

You have a **headless Chromium browser** running in this container. Use the `browser` tool to browse websites, test Salesforce UIs, verify deployments, and take screenshots.

**Key facts:**
- Headless mode — no GUI, no display. Everything is via the `browser` tool.
- Profile: `openclaw` (default, auto-selected)
- Chromium runs with `--no-sandbox` (required in Docker)
- You CAN access internal/private network URLs (SSRF policy allows it)

### When to Use the Browser
- **Verify deployments** — Open the dev/QA org after a deploy, screenshot the page to confirm it looks right
- **Test LWC components** — Navigate to a page with the component, snapshot the DOM, check for errors
- **Salesforce UI checks** — Verify page layouts, record types, field visibility
- **Web research** — When `web_fetch` isn't enough (JS-rendered pages, login-required sites)
- **Screenshot evidence** — Capture before/after screenshots for PRs and case comments

### Quick Reference
```
# Start and open a URL
browser(action: "open", url: "https://example.com")

# Take a screenshot
browser(action: "screenshot")
browser(action: "screenshot", fullPage: true)

# Get page structure (for AI reasoning)
browser(action: "snapshot", compact: true)

# Click/type using refs from snapshot
browser(action: "act", kind: "click", ref: "e12")
browser(action: "act", kind: "type", ref: "e5", text: "hello")

# Navigate
browser(action: "navigate", url: "https://...")

# Check console for errors
browser(action: "console", level: "error")
```

### Salesforce Login Flow
To access Salesforce orgs in the browser:
1. Use `sf org open --target-org dev --url-only` to get a frontdoor login URL
2. Open that URL in the browser — it auto-authenticates
3. Then navigate to the specific page you need

```bash
# Get login URL for dev org
sf org open --target-org dev --url-only 2>/dev/null
# Returns: https://sanguinebio--dev.sandbox.my.salesforce.com/secur/frontdoor.jsp?sid=...

# Then use browser tool to open it
```

### Limitations
- No file downloads (no filesystem access from browser context)
- No video/audio playback
- Some sites may block headless browsers (use stealth if needed)
- Memory-constrained — avoid opening many tabs simultaneously

---

## Environment

- Container OS: Debian Bookworm (Node 22)
- SF CLI: latest
- Python 3: available for scripting
- Git: available
- Chromium: headless (Playwright-managed)
- RAG service: FastAPI on port 8081 (internal)
- Persistent storage: `/var/lib/data/workspace`
- Salesforce repo: `/home/node/.openclaw/workspace/salesforce/`
