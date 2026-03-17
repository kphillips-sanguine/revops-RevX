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

# ---------------------------------------------------------------------------
# RAG Service — Python FastAPI sidecar for knowledge base search
# ---------------------------------------------------------------------------
COPY rag/requirements.txt /opt/rag/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /opt/rag/requirements.txt

COPY --chown=node:node rag/ /opt/rag/
COPY --chown=node:node knowledge/ /home/node/.openclaw/workspace/knowledge/
COPY --chown=node:node scripts/rag-cli.sh /usr/local/bin/rag
RUN chmod +x /usr/local/bin/rag

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

# RevX branding overrides
COPY --chown=node:node branding/favicon.svg /app/dist/control-ui/favicon.svg

# Patch the ORIGINAL index.html in-place (preserves correct asset hashes)
# 1. Replace page title
RUN sed -i 's|<title>[^<]*</title>|<title>RevX</title>|' /app/dist/control-ui/index.html

# 2. Inject branding CSS + DOM rename script before </head> and </body>
RUN sed -i 's|</head>|<style>\
  :root { --claw-accent: #F59E0B !important; --claw-accent-hover: #D97706 !important; --claw-primary: #F59E0B !important; }\
  [style*="--claw"] { --claw-accent: #F59E0B !important; }\
</style>\n</head>|' /app/dist/control-ui/index.html \
    && sed -i 's|</body>|<script>\
(function(){var R=[["OpenClaw","RevX"],["openclaw","RevX"]];function w(n){\
if(n.nodeType===3){var t=n.textContent;R.forEach(function(p){t=t.split(p[0]).join(p[1])});\
if(t!==n.textContent)n.textContent=t}else if(n.nodeType===1\&\&n.tagName!=="SCRIPT"\&\&n.tagName!=="STYLE"){\
["placeholder","title","aria-label","alt"].forEach(function(a){if(n.hasAttribute(a)){var v=n.getAttribute(a);\
R.forEach(function(p){v=v.split(p[0]).join(p[1])});n.setAttribute(a,v)}});n.childNodes.forEach(w)}}\
new MutationObserver(function(ms){ms.forEach(function(m){m.addedNodes.forEach(w);\
if(m.type==="characterData")w(m.target)})}).observe(document.body,{childList:true,subtree:true,characterData:true});\
setTimeout(function(){w(document.body)},500);setTimeout(function(){w(document.body)},2000)})();\
</script>\n</body>|' /app/dist/control-ui/index.html


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
