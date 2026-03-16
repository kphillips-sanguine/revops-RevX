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
# Disabled for now to reduce memory footprint — uncomment when browser automation is needed
# RUN node /app/node_modules/playwright-core/cli.js install --with-deps chromium || true

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

# RevX branding overrides (title, favicon, accent color)
COPY --chown=node:node branding/index.html /app/dist/control-ui/index.html
COPY --chown=node:node branding/favicon.svg /app/dist/control-ui/favicon.svg

# Replace user-visible "OpenClaw" branding text in JS bundles with "RevX"
# Only target quoted strings (display text), not JS identifiers/class names
RUN find /app/dist/control-ui/assets -type f -name '*.js' \
    -exec sed -i \
      -e 's/"OpenClaw"/"RevX"/g' \
      -e "s/'OpenClaw'/'RevX'/g" \
      -e 's/`OpenClaw`/`RevX`/g' \
      -e 's/"OpenClaw /"RevX /g' \
      -e "s/'OpenClaw /'RevX /g" \
    {} +

# Startup script (SF auth + GitHub clone before gateway)
COPY --chown=node:node scripts/startup.sh /home/node/startup.sh
RUN chmod +x /home/node/startup.sh

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

# Custom entrypoint: authenticate SF orgs + clone repo, then start gateway
ENTRYPOINT ["/home/node/startup.sh"]
