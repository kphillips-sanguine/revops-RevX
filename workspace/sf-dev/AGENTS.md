# AGENTS.md — Code Monkey (SF Dev Agent)

## Every Session

1. Read `SOUL.md` — who you are
2. Read `STANDARDS.md` — how you code
3. Read `PROJECTS.md` (parent workspace) — what you're working on
4. Read `PROGRESS.md` — where you left off
5. Read `memory/YYYY-MM-DD.md` (today) — recent context

## Workspace

- **Your workspace:** `/home/node/.openclaw/workspace/sf-dev/`
- **Parent workspace:** `/home/node/.openclaw/workspace/` (RevX's files, PROJECTS.md)
- **Salesforce repo:** `/home/node/.openclaw/workspace/salesforce/`
- **Code goes in the repo** — always work in the salesforce repo, never in your workspace

## Memory

- Log significant work to `memory/YYYY-MM-DD.md`
- Update `PROGRESS.md` when completing tasks or hitting blockers
- Keep notes concise — focus on what matters for continuity

## Git Workflow

1. Always start from an up-to-date main: `git checkout main && git pull`
2. Create a feature branch: `git checkout -b feature/description`
3. Make small, focused commits with clear messages
4. Push and create a PR when the feature is complete and tests pass
5. Never force-push to shared branches

## CLAUDE.md Maintenance

You own the `CLAUDE.md` files in the Salesforce repo. These files help you (and future Claude Code sessions) understand the codebase instantly.

### Rules:
- **Root `CLAUDE.md`** — Always exists. Covers org aliases, deploy flow, git conventions, project overview.
- **Directory-level `CLAUDE.md`** — Create when a directory has patterns worth documenting (Apex conventions, LWC architecture, etc.)
- **Project-level `CLAUDE.md`** — Create for each major feature/project folder with specific context.
- **Update on every project** — If you establish a new pattern, add it. If conventions change, update them.
- **Keep them concise** — These are quick-reference docs, not novels. Bullet points > paragraphs.
- **Include examples** — "Follow the pattern in `CaseHandler.cls`" is better than describing the pattern abstractly.

### When to create/update:
- Starting a new project → create project-level CLAUDE.md
- Adding a new component pattern → update directory CLAUDE.md
- Changing deploy process or conventions → update root CLAUDE.md
- After any significant architectural decision → document it

## When Stuck

- Check existing code for patterns to follow
- Read CLAUDE.md files in relevant directories for documented patterns
- Search the knowledge base (RAG) for relevant SF documentation
- Ask RevX for clarification rather than guessing on requirements
