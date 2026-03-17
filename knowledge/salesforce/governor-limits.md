# Salesforce Governor Limits — Quick Reference

## Per-Transaction Limits (Synchronous)

| Resource | Limit | Notes |
|----------|-------|-------|
| SOQL queries | 100 | Use bulkified queries, selector pattern |
| SOQL rows returned | 50,000 | Use LIMIT, filter wisely |
| DML statements | 150 | Batch records into single DML calls |
| DML rows | 10,000 | Split large operations into async |
| Heap size | 6 MB | Watch out for large collections |
| CPU time | 10,000 ms | Profile complex logic |
| Callouts | 100 | Batch external API calls |
| Callout timeout | 120 seconds | Set appropriate timeouts |
| Future calls | 50 | Use Queueable instead when possible |
| Queueable jobs | 50 | Chain if more needed |
| Email invocations | 10 | Use SingleEmailMessage lists |
| SOSL queries | 20 | Rarely a bottleneck |

## Per-Transaction Limits (Asynchronous)

| Resource | Limit | Notes |
|----------|-------|-------|
| SOQL queries | 200 | Double sync limit |
| Heap size | 12 MB | Double sync limit |
| CPU time | 60,000 ms | 6x sync limit |
| Other limits | Same as sync | DML, rows, etc. unchanged |

## Daily/Org Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| API requests | Based on edition + user count | Monitor in Setup > API Usage |
| Async Apex executions | 250,000 or licensed qty | Batch + Future + Queueable |
| Email (single) | 5,000/day | Includes workflow emails |
| Email (mass) | 5,000/day | Marketing emails |
| Platform Events published | Based on entitlement | Check Setup > Platform Events |

## Common Anti-Patterns (DON'T DO THIS)

### SOQL in a Loop ❌
```apex
// BAD — hits 100 query limit with >100 records
for (Case c : Trigger.new) {
    Account a = [SELECT Name FROM Account WHERE Id = :c.AccountId];
}

// GOOD — one query, then map
Set<Id> accountIds = new Set<Id>();
for (Case c : Trigger.new) { accountIds.add(c.AccountId); }
Map<Id, Account> accounts = new Map<Id, Account>(
    [SELECT Id, Name FROM Account WHERE Id IN :accountIds]
);
```

### DML in a Loop ❌
```apex
// BAD — hits 150 DML limit
for (Case c : cases) {
    c.Status = 'Closed';
    update c;
}

// GOOD — single DML
for (Case c : cases) {
    c.Status = 'Closed';
}
update cases;
```

### Unbounded Queries ❌
```apex
// BAD — could return 50,000+ rows and hit heap limit
List<Case> allCases = [SELECT Id, Subject FROM Case];

// GOOD — filtered and limited
List<Case> recentCases = [SELECT Id, Subject FROM Case 
                          WHERE CreatedDate = LAST_N_DAYS:30 
                          LIMIT 200];
```

## Monitoring

- **Setup → Apex Jobs:** Monitor batch, scheduled, queueable job status
- **Setup → API Usage Notifications:** Set alerts at 70%, 90%
- **Debug Logs:** Check `Limits.getQueries()`, `Limits.getDMLStatements()` in code
- **Developer Console → Query Plan:** Optimize slow SOQL
