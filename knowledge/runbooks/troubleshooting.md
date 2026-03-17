# Runbook: Troubleshooting Guide

## Common Issues

### Deployment Failures

#### "Dependent class is invalid" 
- **Cause:** A class references another class that has compile errors
- **Fix:** Deploy the dependent class first, or deploy both together
- **Prevention:** Always deploy related classes in the same package

#### "Code coverage below 75%"
- **Cause:** Overall org test coverage dropped below threshold
- **Fix:** Run `sf apex run test --test-level RunLocalTests --target-org dev` to find failing tests
- **Check:** `sf apex run test --code-coverage --target-org dev --result-format human`

#### "Apex test failure"
- **Cause:** Test class fails in target org (different data, config, or code state)
- **Fix:** Check test failures, fix assertions or test data setup
- **Common:** Tests that rely on org-specific data (record types, queue names, etc.)

### SF CLI Issues

#### "The org cannot be found"
- **Cause:** Auth token expired or org alias not set
- **Fix:** Re-authenticate: `sf org login web --alias dev`

#### "INVALID_SESSION_ID"
- **Cause:** Session expired or was revoked
- **Fix:** `sf org logout --target-org dev` then re-login

#### "Socket timeout" on deploy
- **Cause:** Large deployment or slow org response
- **Fix:** Use `--wait 60` for longer timeout, or deploy in smaller batches

### LWC Issues

#### Component not showing in Experience Builder
- **Check:** `isExposed: true` in `.js-meta.xml`
- **Check:** Correct targets (`lightningCommunity__Page`, `lightningCommunity__Default`)
- **Check:** Component deployed to the org
- **Fix:** Clear cache, try incognito browser

#### "Cannot read properties of undefined"
- **Cause:** Wire service returned data before component is ready
- **Fix:** Add null checks: `if (this.wiredData?.data) { ... }`

#### "You don't have access to this record"
- **Cause:** Sharing rules or FLS blocking access for the running user
- **Fix:** Check profile/permission set, verify `with sharing` context

### Integration Issues

#### n8n webhook not receiving events
- **Check:** Webhook URL is correct and accessible
- **Check:** Salesforce outbound connection is not blocked
- **Check:** n8n workflow is active (not paused)
- **Fix:** Test with `curl` to verify webhook endpoint

#### Platform Events not delivering
- **Check:** Subscriber is connected (empApi in LWC, or CometD external)
- **Check:** Event was actually published (check debug logs)
- **Check:** Replay ID — subscriber might have missed events
- **Fix:** Re-subscribe from `-1` (latest) or `-2` (all available)

## Diagnostic Commands

```bash
# Check org status
sf org display --target-org dev

# List all orgs
sf org list

# Run specific test with debug
sf apex run test --class-names MyClassTest --target-org dev --result-format human --code-coverage

# Check deployment status
sf project deploy report --target-org dev

# Execute anonymous Apex for quick debugging
echo "System.debug([SELECT COUNT() FROM Case]);" | sf apex run --target-org dev

# Check governor limit usage in a running transaction (add to code)
# System.debug('Queries used: ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
```

## Logs

### Enable Debug Logs
```bash
# For your user (1 hour)
sf apex log tail --target-org dev

# Specific log level
sf apex log get --target-org dev --number 5
```

### Key Log Categories
- **Apex Code:** FINEST for line-by-line execution
- **SOQL:** DEBUG for query details
- **Callout:** DEBUG for external HTTP requests
- **Validation:** INFO for validation rule evaluation
