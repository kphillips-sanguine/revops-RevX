# OpenClaw — Sanguine Bio Team Deployment

Central OpenClaw Gateway for team AI agents, deployed on Sevalla VPS.

## Architecture

```
Team (browser/Discord/Slack)
        │
        ▼
  Sevalla HTTPS endpoint
  (openclaw-xxxxx.sevalla.app)
        │
        ▼
┌──────────────────────────────┐
│  Docker Container            │
│  ┌────────────────────────┐  │
│  │  OpenClaw Gateway      │  │
│  │  - Multi-agent routing │  │
│  │  - SF CLI baked in     │  │
│  │  - Control UI (web)    │  │
│  └────────────────────────┘  │
│         │                    │
│  Persistent Disk             │
│  /home/node/.openclaw/       │
│  - openclaw.json (config)    │
│  - workspace/ (agent files)  │
│  - agents/ (multi-agent)     │
└──────────────────────────────┘
        │
        ▼
  AI Provider APIs (Anthropic, OpenAI)
  Channel APIs (Discord, Slack)
```

## What's Included

| Tool | Purpose |
|------|---------|
| OpenClaw Gateway | AI agent runtime + Control UI |
| Salesforce CLI | SF org queries, deploys, metadata |
| sfdx-git-delta | Delta deploys for CI/CD |
| Git | Version control from agents |
| Python 3 | Scripting support |

## Local Development

### Prerequisites
- Docker Desktop
- Copy `.env.example` → `.env` and fill in values

### Build & Run
```bash
docker compose build
docker compose up -d
```

### Access
- Control UI: http://localhost:18789
- Paste your `OPENCLAW_GATEWAY_TOKEN` in Settings

### Logs
```bash
docker compose logs -f openclaw-gateway
```

## Deploy to Sevalla

### 1. Create Sevalla Application
- New Application → Build from Dockerfile
- Connect this git repo
- Set port to `8080`

### 2. Add Secrets (Environment Variables)
In Sevalla dashboard → Application → Settings → Secrets:
- `OPENCLAW_GATEWAY_TOKEN` (generate: `openssl rand -hex 32`)
- `ANTHROPIC_API_KEY`
- `DISCORD_BOT_TOKEN` (when ready)
- Any other keys from `.env.example`

### 3. Attach Persistent Storage
- Create a persistent volume (~10 GB)
- Mount at: `/home/node/.openclaw`
- This preserves config, sessions, and workspace across deploys

### 4. Deploy
Push to the connected git branch → Sevalla auto-builds and deploys.

### 5. First Access
- Visit: `https://your-app.sevalla.app`
- Paste gateway token in Control UI
- Run onboarding or upload `config/openclaw.json`

## Multi-Agent Setup (Phase 2)

Each team member gets an isolated agent with their own:
- Workspace (SOUL.md, AGENTS.md, USER.md, memory)
- Sessions (chat history)
- Auth profiles (API keys, OAuth)

Edit `config/openclaw.json` to uncomment the `agents.list` and `bindings` sections.

See [OpenClaw Multi-Agent Docs](https://docs.openclaw.ai/concepts/multi-agent) for details.

## Security Notes

- **Gateway token** controls all access — keep it secret
- **Multi-agent isolation** is convenience, not security (shared control plane)
- For sensitive personal data (email, calendar), keep those on local OpenClaw instances
- Team gateway should be business-only (Salesforce, code, DevOps)

## Files

```
├── Dockerfile          # Container image definition
├── docker-compose.yml  # Local dev/test compose
├── config/
│   └── openclaw.json   # Gateway configuration template
├── .env.example        # Environment variable template
├── .gitignore
└── README.md
```
