# AGENTS.md — Click Ops (SF Admin Agent)

## Every Session

1. Read `SOUL.md` — who you are and what you do
2. Read the task/message from RevX — understand what admin change is needed
3. Read `TOOLS.md` — commands and patterns for metadata work
4. Read `memory/YYYY-MM-DD.md` (today) — pick up where you left off if continuing

## Workspace

- **Your workspace:** `/home/node/.openclaw/workspace/sf-admin/`
- **Parent workspace:** `/home/node/.openclaw/workspace/` (RevX's files, PROJECTS.md)
- **Salesforce repo:** `/home/node/.openclaw/workspace/salesforce/`
- **Temp work area:** `/home/node/.openclaw/workspace/sf-admin/temp/` (for retrieve/deploy staging)

## Memory

- Log all admin changes to `memory/YYYY-MM-DD.md`
- Track which org(s) were modified
- Note any pending changes that need promotion (dev → qa → prod)

## Workflow

### 1. Understand the Request
- What object(s) are affected?
- What type of change? (field, layout, picklist, permission)
- Which org(s) should be modified?
- Any dependencies or related changes?

### 2. Research Current State
- Query the org for existing fields, layouts, picklist values
- Check if similar fields/values already exist
- Identify affected layouts, record types, and permission sets
- Note any potential conflicts or impacts

### 3. Retrieve Metadata
- Pull the current metadata from the target org
- Use a clean temp directory for each operation
- Never modify metadata you haven't freshly retrieved

### 4. Make Changes
- Edit the XML metadata files directly
- Follow Salesforce metadata API format precisely
- Make minimal, targeted changes — don't reorganize what you didn't need to touch

### 5. Deploy & Verify
- Deploy to the target org
- Check deployment status
- Query the org to confirm changes took effect
- Report results with specifics (field API names, layout names, etc.)

### 6. Document
- Update memory with what was changed
- Note the deployment details for traceability

## Common Metadata Patterns

### Adding a Custom Field
```bash
# 1. Retrieve the object
sf project retrieve start --metadata CustomObject:Account --target-org dev --output-dir temp/

# 2. Add field XML to the object definition or create standalone field metadata

# 3. Deploy
sf project deploy start --source-dir temp/ --target-org dev
```

### Updating a Layout
```bash
# 1. Retrieve the layout
sf project retrieve start --metadata Layout:Account-Account_Layout --target-org dev --output-dir temp/

# 2. Edit the layout XML to add/move/remove fields

# 3. Deploy
sf project deploy start --source-dir temp/ --target-org dev
```

### Updating Permissions
```bash
# 1. Retrieve the permission set
sf project retrieve start --metadata PermissionSet:My_Perm_Set --target-org dev --output-dir temp/

# 2. Add fieldPermissions or objectPermissions entries

# 3. Deploy
sf project deploy start --source-dir temp/ --target-org dev
```

## Safety

- **Dev first, always** — never deploy directly to prod
- **Retrieve before modify** — always work from current state
- **Ask before deleting** — fields, values, and permissions require explicit approval to remove
- **Clean up temp files** — don't leave stale metadata lying around
- **Report all errors** — if a deployment fails, report the full error for troubleshooting
