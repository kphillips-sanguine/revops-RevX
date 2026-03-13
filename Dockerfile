# =============================================================================
# OpenClaw Gateway — Sanguine Bio Team Deployment
# Base: official OpenClaw pre-built image (Node 22 + Bookworm)
# Adds: Salesforce CLI, sfdx-git-delta, git, gog CLI, common tools
# =============================================================================

FROM ghcr.io/openclaw/openclaw:latest

# Switch to root for package installation
USER root

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    openssh-client \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Salesforce CLI (latest)
RUN npm install -g @salesforce/cli@latest

# sfdx-git-delta plugin (as SF CLI plugin)
# Install as root, then fix ownership for node user
RUN sf plugins install sfdx-git-delta \
    && chown -R node:node /root/.local/share/sf || true

# gog CLI (Google Workspace) — install globally
# Uncomment when needed:
# RUN npm install -g @nicholasgasior/gog

# Playwright browsers for browser tool (Chromium only)
RUN node /app/node_modules/playwright-core/cli.js install --with-deps chromium || true

# Create persistent directories
RUN mkdir -p /home/node/.openclaw \
             /home/node/.openclaw/workspace \
             /home/node/.openclaw/workspace/memory \
             /home/node/.openclaw/agents \
    && chown -R node:node /home/node/.openclaw

# Bake in workspace files (agent identity, config, tools)
COPY --chown=node:node workspace/ /home/node/.openclaw/workspace/

# Bake in gateway config
COPY --chown=node:node config/openclaw.json /home/node/.openclaw/openclaw.json

# Performance: Node compile cache
ENV NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
RUN mkdir -p /var/tmp/openclaw-compile-cache && chown node:node /var/tmp/openclaw-compile-cache

# Avoid respawn overhead in container
ENV OPENCLAW_NO_RESPAWN=1

# Switch back to non-root user
USER node

# Gateway config — Sevalla handles TLS, we bind to LAN
ENV OPENCLAW_GATEWAY_BIND=lan
ENV OPENCLAW_GATEWAY_PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8080/healthz || exit 1

EXPOSE 8080

# The base image CMD handles gateway startup
# OPENCLAW_GATEWAY_PORT and OPENCLAW_GATEWAY_BIND env vars configure binding
# --allow-unconfigured is the base image default
