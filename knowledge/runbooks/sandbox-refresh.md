# Runbook: Sandbox Refresh

## When to Refresh
- **Dev sandbox:** As needed (usually after major production releases)
- **QA sandbox:** Before major testing cycles
- **Schedule:** Coordinate with team — refresh wipes all sandbox data and config

## Pre-Refresh Checklist
- [ ] Notify team members who use the sandbox
- [ ] Export any sandbox-specific test data that needs to be preserved
- [ ] Document any sandbox-specific configuration (connected apps, auth providers)
- [ ] Save SF CLI auth URLs (they'll need to be regenerated post-refresh)

## Steps

### 1. Initiate Refresh
1. Go to **Production** → Setup → Sandboxes
2. Find the sandbox to refresh
3. Click **Refresh**
4. Select source (usually Production)
5. Select sandbox license type (Developer for dev/qa)
6. Click **Create**

### 2. Wait for Completion
- Developer sandboxes: Usually 1-4 hours
- Partial/Full sandboxes: Can take 24+ hours
- Monitor via Setup → Sandboxes (status column)

### 3. Post-Refresh Setup

#### Activate the Sandbox
1. Check email for activation link
2. Log in with production credentials + `.sandboxname` suffix
3. Verify access

#### Re-authenticate SF CLI
```bash
# Generate new SFDX auth URL
sf org login web --alias dev --instance-url https://test.salesforce.com

# Or use existing auth URL file
sf org login sfdx-url --sfdx-url-file /path/to/auth-url.txt --alias dev
```

#### Update Connected Apps (if applicable)
- Check connected app callback URLs
- Verify OAuth consumer key/secret
- Test API access

#### Deploy Latest Code
```bash
# Deploy full source to refreshed sandbox
sf project deploy start --source-dir force-app --target-org dev --wait 30

# Run tests to verify
sf apex run test --test-level RunLocalTests --target-org dev --result-format human
```

#### Load Test Data
- Run any data loading scripts
- Create test users with appropriate profiles/permission sets
- Verify data relationships are intact

### 4. Update RevX Auth
If refreshing dev or qa sandbox, update the Sevalla environment variable:
1. Go to Sevalla dashboard → RevX app → Environment variables
2. Update `SF_DEV_AUTH_URL` or `SF_QA_AUTH_URL`
3. Redeploy the container

## Post-Refresh Verification
- [ ] SF CLI can authenticate to the sandbox
- [ ] Latest code is deployed and tests pass
- [ ] Key features work (LWCs load, triggers fire, flows execute)
- [ ] API integrations connect (n8n, external services)
- [ ] RevX agents can query the sandbox

## Contacts
- **Sandbox issues:** Kevin Phillips or Deepthi Katragadda
- **License/limits:** Brian Vong
