# Apex Development Patterns — Sanguine Bio

## Trigger Handler Pattern

One trigger per object, all logic in a handler class:

```apex
// Trigger (thin — just delegates)
trigger CaseTrigger on Case (before insert, before update, after insert, after update) {
    CaseTriggerHandler handler = new CaseTriggerHandler();
    handler.run();
}

// Handler (where the logic lives)
public class CaseTriggerHandler extends TriggerHandler {
    public override void beforeInsert() {
        // logic here
    }
    public override void afterUpdate() {
        // logic here
    }
}
```

### Rules
- **Never put logic in the trigger file** — always delegate to handler
- **One trigger per object** — multiple triggers on the same object cause ordering issues
- **Bulkify everything** — handlers receive `Trigger.new` (list), process all records
- **No SOQL/DML in loops** — collect IDs, query once, process, DML once

## Service Layer Pattern

Reusable business logic separated from triggers and controllers:

```apex
public class CaseService {
    public static void assignToQueue(List<Case> cases, Id queueId) {
        for (Case c : cases) {
            c.OwnerId = queueId;
        }
        // Caller is responsible for DML
    }
    
    public static List<Case> getOpenCasesByOwner(Id ownerId) {
        return [SELECT Id, CaseNumber, Subject, Status, Priority 
                FROM Case 
                WHERE OwnerId = :ownerId AND IsClosed = false
                ORDER BY CreatedDate DESC];
    }
}
```

### Rules
- **Static methods** for stateless operations
- **Services don't do DML** unless they own the full transaction
- **Reusable** across triggers, controllers, batch jobs, REST endpoints

## Selector Pattern

Centralize SOQL queries:

```apex
public class CaseSelector {
    public static List<Case> selectById(Set<Id> caseIds) {
        return [SELECT Id, CaseNumber, Subject, Status, Priority, 
                       Contact.Name, Contact.Email, Account.Name
                FROM Case 
                WHERE Id IN :caseIds];
    }
    
    public static List<Case> selectOpenByAccount(Id accountId) {
        return [SELECT Id, CaseNumber, Subject, Status 
                FROM Case 
                WHERE AccountId = :accountId AND IsClosed = false];
    }
}
```

### Rules
- **One selector per object**
- **All SOQL for that object goes through the selector**
- **Consistent field lists** — don't query different fields in different places
- **Supports test isolation** — easy to mock in tests

## Test Patterns

```apex
@IsTest
private class CaseServiceTest {
    
    @TestSetup
    static void setup() {
        Account a = new Account(Name = 'Test Account');
        insert a;
        
        Contact c = new Contact(LastName = 'Test', AccountId = a.Id);
        insert c;
        
        List<Case> cases = new List<Case>();
        for (Integer i = 0; i < 200; i++) {
            cases.add(new Case(
                Subject = 'Test Case ' + i,
                ContactId = c.Id,
                AccountId = a.Id,
                Status = 'New'
            ));
        }
        insert cases;
    }
    
    @IsTest
    static void testAssignToQueue_Bulk() {
        List<Case> cases = [SELECT Id FROM Case];
        Id queueId = [SELECT Id FROM Group WHERE Type = 'Queue' LIMIT 1].Id;
        
        Test.startTest();
        CaseService.assignToQueue(cases, queueId);
        update cases;
        Test.stopTest();
        
        // Meaningful assertions
        List<Case> updated = [SELECT OwnerId FROM Case WHERE Id IN :cases];
        for (Case c : updated) {
            System.assertEquals(queueId, c.OwnerId, 'Case should be assigned to queue');
        }
    }
}
```

### Rules
- **@TestSetup** for shared test data (runs once per test class)
- **Test.startTest() / Test.stopTest()** to reset governor limits
- **Test bulk** (200+ records) to verify bulkification
- **Meaningful assertions** — not just "it didn't crash"
- **No seeAllData=true** unless absolutely necessary
- **Minimum 85% coverage** per class, aim for meaningful coverage

## Governor Limit Best Practices

| Limit | Per Transaction | Strategy |
|-------|----------------|----------|
| SOQL queries | 100 | Use selector pattern, query outside loops |
| DML statements | 150 | Collect records, single DML per operation |
| SOQL rows | 50,000 | Use LIMIT, pagination for large datasets |
| Heap size | 6 MB (sync) / 12 MB (async) | Stream large data, avoid storing full datasets |
| CPU time | 10,000 ms (sync) / 60,000 ms (async) | Move heavy work to async (Batch/Queueable) |
| Callouts | 100 per transaction | Batch external API calls, use Queueable chains |

## Async Patterns

### Queueable (preferred for most async work)
```apex
public class MyQueueable implements Queueable {
    public void execute(QueueableContext context) {
        // async work here
    }
}
// Enqueue: System.enqueueJob(new MyQueueable());
```

### Batch (for processing large datasets)
```apex
public class MyBatch implements Database.Batchable<SObject> {
    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator('SELECT Id FROM Case WHERE ...');
    }
    public void execute(Database.BatchableContext bc, List<Case> scope) {
        // process batch of records
    }
    public void finish(Database.BatchableContext bc) {
        // cleanup, send notification
    }
}
// Execute: Database.executeBatch(new MyBatch(), 200);
```

### Scheduled (recurring jobs)
```apex
public class MyScheduled implements Schedulable {
    public void execute(SchedulableContext sc) {
        Database.executeBatch(new MyBatch());
    }
}
// Schedule: System.schedule('Daily Cleanup', '0 0 2 * * ?', new MyScheduled());
```
