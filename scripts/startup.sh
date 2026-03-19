#!/bin/bash
# RevX Startup Script
# Runs before OpenClaw gateway starts
# 1. Sets up persistent storage
# 2. Authenticates SF CLI orgs
# 3. Clones GitHub repo
# 4. Starts RAG service + syncs knowledge base
# 5. Launches OpenClaw gateway

set -e

# ─── Persistent Storage ─────────────────────────────────────────────────────
# Workspace files live on persistent disk at /var/lib/data/workspace so they
# survive container redeploys. On first run, baked-in files are copied over.
# On subsequent runs, only NEW files from the image are added (no overwrites).
# ─────────────────────────────────────────────────────────────────────────────

PERSISTENT_WORKSPACE="/var/lib/data/workspace"
PERSISTENT_CONFIG="/var/lib/data/openclaw.json"
BAKED_WORKSPACE="/home/node/.openclaw/workspace"
BAKED_CONFIG="/home/node/.openclaw/openclaw.json"

echo "🔧 RevX startup: Setting up persistent storage..."

if [ -d "/var/lib/data" ]; then
  # ── Workspace persistence ──────────────────────────────────────────────
  if [ ! -d "$PERSISTENT_WORKSPACE" ]; then
    # First run: copy baked-in workspace to persistent storage
    echo "  📦 First run — copying workspace to persistent storage..."
    cp -a "$BAKED_WORKSPACE" "$PERSISTENT_WORKSPACE"
    echo "  ✅ Workspace initialized on persistent storage"
  else
    # Subsequent run: merge new files only (don't overwrite existing)
    echo "  📦 Persistent workspace exists — merging new files..."
    cp -rn "$BAKED_WORKSPACE"/. "$PERSISTENT_WORKSPACE"/ 2>/dev/null || true
    echo "  ✅ New files merged (existing files preserved)"
  fi

  # Ensure memory directory exists
  mkdir -p "$PERSISTENT_WORKSPACE/memory"

  # Replace workspace with symlink to persistent storage
  rm -rf "$BAKED_WORKSPACE"
  ln -s "$PERSISTENT_WORKSPACE" "$BAKED_WORKSPACE"
  echo "  🔗 Workspace symlinked: $BAKED_WORKSPACE → $PERSISTENT_WORKSPACE"

  # ── Config persistence ─────────────────────────────────────────────────
  # Runtime config changes (e.g. adding Slack channels) must survive redeploys.
  # Strategy: persistent copy wins, but baked-in config is used on first run.
  if [ ! -f "$PERSISTENT_CONFIG" ]; then
    # First run: seed persistent config from baked-in version
    echo "  📦 First run — copying config to persistent storage..."
    cp "$BAKED_CONFIG" "$PERSISTENT_CONFIG"
    echo "  ✅ Config initialized on persistent storage"
  else
    # Subsequent run: keep the persistent (runtime-modified) config,
    # but merge in any NEW Slack channels from the baked-in config.
    echo "  📦 Persistent config exists — preserving runtime config"
    if command -v jq >/dev/null 2>&1; then
      # Merge new Slack channels from baked config into persistent config
      # Uses jq '*' (multiply/merge) which adds new keys without overwriting existing ones
      MERGED=$(jq -s '
        .[0] as $persist | .[1] as $baked |
        $persist
        | .channels.slack.channels = ($baked.channels.slack.channels * $persist.channels.slack.channels)
        | .gateway.controlUi.allowedOrigins = ($baked.gateway.controlUi.allowedOrigins // $persist.gateway.controlUi.allowedOrigins)
      ' "$PERSISTENT_CONFIG" "$BAKED_CONFIG" 2>/dev/null) && \
        echo "$MERGED" > "$PERSISTENT_CONFIG" && \
        echo "  ✅ Merged new config from baked image (channels + allowedOrigins)" || \
        echo "  ⚠️ Config merge skipped (jq error)"
    fi
  fi

  # Symlink config to persistent copy
  rm -f "$BAKED_CONFIG"
  ln -s "$PERSISTENT_CONFIG" "$BAKED_CONFIG"
  echo "  🔗 Config symlinked: $BAKED_CONFIG → $PERSISTENT_CONFIG"
else
  echo "  ⚠️ /var/lib/data not mounted — using ephemeral workspace + config"
fi

echo "🔧 RevX startup: Authenticating SF orgs..."

# Authenticate prod org (READ + Support RevOps Cases only)
if [ -n "$SF_PROD_AUTH_URL" ]; then
  echo "$SF_PROD_AUTH_URL" > /tmp/prod-auth.txt
  sf org login sfdx-url --sfdx-url-file /tmp/prod-auth.txt --alias prod --no-prompt 2>/dev/null && \
    echo "  ✅ Prod org authenticated (read + Support RevOps Cases only)" || echo "  ⚠️ Prod org auth failed"
  rm -f /tmp/prod-auth.txt
fi

# Authenticate dev org
if [ -n "$SF_DEV_AUTH_URL" ]; then
  echo "$SF_DEV_AUTH_URL" > /tmp/dev-auth.txt
  sf org login sfdx-url --sfdx-url-file /tmp/dev-auth.txt --alias dev --no-prompt 2>/dev/null && \
    echo "  ✅ Dev org authenticated" || echo "  ⚠️ Dev org auth failed"
  rm -f /tmp/dev-auth.txt
fi

# Authenticate QA org
if [ -n "$SF_QA_AUTH_URL" ]; then
  echo "$SF_QA_AUTH_URL" > /tmp/qa-auth.txt
  sf org login sfdx-url --sfdx-url-file /tmp/qa-auth.txt --alias qa --no-prompt 2>/dev/null && \
    echo "  ✅ QA org authenticated" || echo "  ⚠️ QA org auth failed"
  rm -f /tmp/qa-auth.txt
fi

# Set dev as default org
sf config set target-org dev 2>/dev/null || true

echo "🔧 RevX startup: Setting up GitHub access..."

# Authenticate gh CLI + git credential helper for multi-repo access
if [ -n "$GITHUB_PAT" ]; then
  # Export GH_TOKEN so gh CLI picks it up automatically (most reliable method)
  export GH_TOKEN="$GITHUB_PAT"
  echo "  ✅ GH_TOKEN exported for gh CLI"

  # Also do explicit auth login as backup
  echo "$GITHUB_PAT" | gh auth login --with-token 2>&1 && \
    echo "  ✅ gh auth login succeeded" || echo "  ⚠️ gh auth login failed (GH_TOKEN still works)"

  # Set up git credential helper so any repo works without embedding token in URL
  git config --global credential.helper store
  echo "https://x-access-token:${GITHUB_PAT}@github.com" > ~/.git-credentials
  chmod 600 ~/.git-credentials
  echo "  ✅ Git credential helper configured (multi-repo)"

  # Set git identity
  git config --global user.name "RevX"
  git config --global user.email "revx@sanguinebio.com"
else
  echo "  ⚠️ GITHUB_PAT not set, skipping GitHub setup"
fi

echo "🔧 RevX startup: Cloning GitHub repo..."

# Clone or pull the Salesforce repo
REPO_DIR="/home/node/.openclaw/workspace/salesforce"
if [ -n "$GITHUB_PAT" ]; then
  if [ -d "$REPO_DIR/.git" ]; then
    echo "  📦 Repo exists, pulling latest..."
    cd "$REPO_DIR" && git pull origin main 2>/dev/null && \
      echo "  ✅ Repo updated" || echo "  ⚠️ Git pull failed"
  else
    echo "  📦 Cloning repo..."
    git clone "https://github.com/sanguinebio/salesforce.git" "$REPO_DIR" 2>/dev/null && \
      echo "  ✅ Repo cloned" || echo "  ⚠️ Git clone failed"
  fi
else
  echo "  ⚠️ GITHUB_PAT not set, skipping repo clone"
fi

# ---------------------------------------------------------------------------
# RAG Service — Knowledge Base
# ---------------------------------------------------------------------------
echo "🧠 RevX startup: Starting RAG service..."

if [ -n "$DATABASE_URL" ] && [ -n "$GOOGLE_API_KEY" ]; then
  # Start RAG service in background on port 8081
  # PYTHONPATH ensures 'from rag.xxx import ...' works
  export PYTHONPATH="/opt:$PYTHONPATH"
  cd /opt
  python3 -m uvicorn rag.server:app \
    --host 127.0.0.1 \
    --port "${RAG_PORT:-8081}" \
    --log-level warning \
    &
  RAG_PID=$!
  echo "  ✅ RAG service started (PID: $RAG_PID, port: ${RAG_PORT:-8081})"

  # Wait for RAG service to be ready (up to 15s)
  echo "  ⏳ Waiting for RAG service..."
  for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:${RAG_PORT:-8081}/rag/health > /dev/null 2>&1; then
      echo "  ✅ RAG service ready"
      break
    fi
    sleep 0.5
  done

  # Run initial knowledge sync
  echo "  📚 Syncing knowledge base..."
  SYNC_RESULT=$(curl -s -X POST http://127.0.0.1:${RAG_PORT:-8081}/rag/sync \
    -H "Content-Type: application/json" \
    -d '{"force": false}' 2>/dev/null || echo '{"error": "sync failed"}')
  echo "  📚 Sync result: $SYNC_RESULT"
else
  echo "  ⚠️ RAG service not started (requires DATABASE_URL and GOOGLE_API_KEY)"
  if [ -z "$DATABASE_URL" ]; then
    echo "     Missing: DATABASE_URL"
  fi
  if [ -z "$GOOGLE_API_KEY" ]; then
    echo "     Missing: GOOGLE_API_KEY"
  fi
fi

echo "🚀 RevX startup complete, launching gateway..."

# Start OpenClaw gateway (exec replaces this process)
# Note: using exec means the RAG background process becomes an orphan adopted by PID 1
# This is fine in a container context — both processes run until the container stops
exec node /app/openclaw.mjs gateway --allow-unconfigured "$@"
