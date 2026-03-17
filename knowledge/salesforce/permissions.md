# Permissions & Security — Sanguine Bio Salesforce

## Permission Model

### Principle
- **Permission Sets over Profiles** — profiles for login access and page layouts only
- **Least privilege** — grant minimum access needed
- **Permission Set Groups** for role-based bundles

### Hierarchy
```
Profile (base access + page layouts)
  └── Permission Set Group (role bundle)
        ├── Permission Set (feature-specific access)
        ├── Permission Set (feature-specific access)
        └── Permission Set (feature-specific access)
```

## Profiles

### Internal Users
- **System Administrator** — full access (Kevin, admins)
- **Standard User** — base CRM access
- **Custom profiles** — as needed per business role

### Portal Users (Experience Cloud)
- **Customer Community User** — basic portal access
- **Customer Community Plus User** — enhanced portal access with sharing
- **Partner Community User** — partner portal access

### Key Difference
Portal users operate under a **community license** with different sharing and visibility rules than internal users. Always test with portal user profiles.

## Permission Sets

### Naming Convention
`[App]_[Role]` — examples:
- `RevX_Admin` — RevX administration features
- `Portal_User` — Base portal access
- `DevOps_Deploy` — Deployment pipeline access

### Creating Permission Sets
- **Object access:** CRUD per object
- **Field-level security:** Read/edit per field
- **Apex class access:** Which classes can be executed
- **Visualforce page access:** Legacy, but still used
- **Tab access:** Which tabs are visible
- **App access:** Which Lightning apps are available

## Sharing Model

### Organization-Wide Defaults (OWD)
- Set the **most restrictive** baseline for each object
- Then use sharing rules to open up access where needed

### Sharing Rules
- **Criteria-based:** Share records matching specific criteria
- **Owner-based:** Share records owned by specific groups
- **Guest user rules:** Special rules for unauthenticated portal users

### Apex Sharing Keywords
```apex
// with sharing — respects user's sharing rules (USE THIS for portal)
public with sharing class PortalController { }

// without sharing — ignores sharing rules (admin operations)
public without sharing class AdminService { }

// inherited sharing — inherits from calling class
public inherited sharing class UtilityClass { }
```

**Rule:** Always use `with sharing` unless you have a documented reason not to.

## Field-Level Security (FLS)

### Enforcement
- **LWC + Lightning Data Service:** Automatically enforced
- **Apex:** Must be manually enforced in SOQL/DML
- **SOQL:** Use `WITH SECURITY_ENFORCED` or `Security.stripInaccessible()`

```apex
// Option 1: WITH SECURITY_ENFORCED (throws exception if no access)
List<Case> cases = [SELECT Id, Subject FROM Case WITH SECURITY_ENFORCED];

// Option 2: stripInaccessible (silently removes inaccessible fields)
SObjectAccessDecision decision = Security.stripInaccessible(
    AccessType.READABLE,
    [SELECT Id, Subject, Internal_Notes__c FROM Case]
);
List<Case> safeCases = decision.getRecords();
```

## CRUD Checks

```apex
// Before insert
if (!Schema.sObjectType.Case.isCreateable()) {
    throw new AuraHandledException('Insufficient access to create Case records');
}

// Before update
if (!Schema.sObjectType.Case.isUpdateable()) {
    throw new AuraHandledException('Insufficient access to update Case records');
}

// Before delete
if (!Schema.sObjectType.Case.isDeletable()) {
    throw new AuraHandledException('Insufficient access to delete Case records');
}
```

**Rule:** All Apex controllers serving LWC or portal pages must include CRUD/FLS checks.
