# Salesforce Development Standards — Sanguine Bio

## Apex

### Naming Conventions
- **Classes:** PascalCase — `AccountService`, `CaseHandler`, `OpportunityTriggerHandler`
- **Test classes:** `[ClassName]Test` — `AccountServiceTest`, `CaseHandlerTest`
- **Methods:** camelCase — `getActiveAccounts()`, `processCaseUpdate()`
- **Constants:** UPPER_SNAKE_CASE — `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE`
- **Trigger handlers:** `[Object]TriggerHandler` — one trigger per object, logic in handler

### Patterns
- **One trigger per object** — all logic delegated to handler class
- **Service layer** for business logic — keep triggers and controllers thin
- **Selector pattern** for SOQL — centralize queries in selector classes
- **Bulkification** — always handle collections, never single records
- **Governor limit awareness** — no SOQL/DML in loops, ever

### Testing
- **Minimum 85% coverage** — but aim for meaningful assertions, not just line coverage
- **@TestSetup** for shared test data
- **Test positive, negative, and bulk** scenarios
- **No seeAllData=true** unless absolutely necessary (and document why)
- **Use Test.startTest()/stopTest()** to reset governor limits

### Error Handling
- Custom exceptions extend a base `SanguineException` class
- Log errors via custom logging framework (if exists) or System.debug with structured format
- Never swallow exceptions silently

## Lightning Web Components (LWC)

### Naming
- **Components:** camelCase folders — `caseDetail`, `accountSearch`, `portalHeader`
- **Files:** Match component name — `caseDetail.html`, `caseDetail.js`, `caseDetail.css`
- **Events:** `CustomEvent` with descriptive names — `accountselected`, `filterchanged`

### Patterns
- **Wire service** for read operations when possible
- **Imperative Apex** for DML or complex operations
- **Lightning Data Service** for single-record CRUD
- **CSS custom properties** for theming — align with org's design system
- **Accessibility** — proper ARIA labels, keyboard navigation, screen reader support

### Component Architecture
- **Container components** handle data fetching and state
- **Presentational components** receive data via @api and render UI
- **Keep components small** — if it's over 300 lines, split it

## Metadata & Configuration

### Custom Objects
- **API Name:** `Snake_Case__c` — `Source_Change__c`, `Agent_Tool_Definition__c`
- **Labels:** Human-readable — "Source Change", "Agent Tool Definition"
- **Description:** Always populated — explain the object's purpose

### Custom Fields
- **API Name:** `Snake_Case__c` — `Case_Number__c`, `Is_Active__c`
- **Help text:** Always populated for user-facing fields
- **Field-level security:** Explicitly set, never rely on defaults

### Permission Sets
- Prefer **Permission Sets** over Profiles for granting access
- Name pattern: `[App]_[Role]` — `RevX_Admin`, `Portal_User`
- Document what each permission set grants and who should have it

## Git & Deployment

### Commit Messages
```
type(scope): description

feat(lwc): add case detail component
fix(apex): handle null contact on case creation
test(apex): add bulk test for CaseHandler
refactor(apex): extract case validation to service layer
```

### Branch Naming
```
feature/short-description
bugfix/case-number-description
hotfix/critical-issue
```

### Deployment Order
1. **Dev sandbox** — build and test
2. **QA sandbox** — validate with team
3. **Prod** — deploy via PR + CI pipeline

## Documentation

- **Apex:** JSDoc-style comments on public methods
- **LWC:** Component-level JSDoc + inline comments for complex logic
- **README:** Every new feature gets a section in the project README
- **PR description:** What changed, why, how to test, screenshots if UI
