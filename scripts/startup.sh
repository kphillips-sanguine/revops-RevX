#!/bin/bash
# RevX Startup Script
# Runs before OpenClaw gateway starts
# Authenticates SF CLI orgs and clones GitHub repo

set -e

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
    git clone "https://${GITHUB_PAT}@github.com/sanguinebio/salesforce.git" "$REPO_DIR" 2>/dev/null && \
      echo "  ✅ Repo cloned" || echo "  ⚠️ Git clone failed"
  fi
else
  echo "  ⚠️ GITHUB_PAT not set, skipping repo clone"
fi

echo "🚀 RevX startup complete, launching gateway..."

# Start OpenClaw gateway (exec replaces this process)
exec node /app/openclaw.mjs gateway --allow-unconfigured "$@"
