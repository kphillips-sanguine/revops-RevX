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

## When Stuck

- Check existing code for patterns to follow
- Search the knowledge base (RAG) for relevant SF documentation
- Ask RevX for clarification rather than guessing on requirements
