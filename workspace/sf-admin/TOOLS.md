# TOOLS.md — Merlin 🪄 (SF Admin Agent)

## Salesforce CLI

**Org aliases:**
- `prod` — Production (⚠️ DO NOT deploy without explicit approval)
- `dev` — Development sandbox (default target for changes)
- `qa` — QA sandbox

### Metadata Retrieval
```bash
# Retrieve specific metadata types
sf project retrieve start --metadata CustomObject:My_Object__c --target-org dev --output-dir temp/
sf project retrieve start --metadata Layout:Account-Account_Layout --target-org dev --output-dir temp/
sf project retrieve start --metadata PermissionSet:My_Perm_Set --target-org dev --output-dir temp/
sf project retrieve start --metadata Profile:Admin --target-org dev --output-dir temp/
sf project retrieve start --metadata GlobalValueSet:My_Global_Set --target-org dev --output-dir temp/
sf project retrieve start --metadata RecordType:Account.Business_Account --target-org dev --output-dir temp/

# Retrieve multiple items
sf project retrieve start --metadata "CustomField:Account.My_Field__c,Layout:Account-Account_Layout" --target-org dev --output-dir temp/
```

### Metadata Deployment
```bash
# 🛑 ALWAYS ASK BEFORE RUNNING DEPLOY COMMANDS

# Deploy from a directory
sf project deploy start --source-dir temp/ --target-org dev

# Deploy with no tests (admin metadata usually doesn't need tests)
sf project deploy start --source-dir temp/ --target-org dev --test-level NoTestRun

# Check deploy status
sf project deploy report --target-org dev
```

### Org Queries (Research)
```bash
# List fields on an object
sf data query --query "SELECT QualifiedApiName, DataType, Label, Description FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName = 'Account'" --target-org dev --result-format json

# List page layouts for an object
sf data query --query "SELECT Name, TableEnumOrId FROM Layout WHERE TableEnumOrId = 'Account'" --target-org dev

# List permission sets
sf data query --query "SELECT Id, Name, Label FROM PermissionSet WHERE IsCustom = true ORDER BY Label" --target-org dev

# Check field-level security for a field
sf data query --query "SELECT Parent.Name, Field, PermissionsRead, PermissionsEdit FROM FieldPermissions WHERE Field = 'Account.My_Field__c'" --target-org dev

# List picklist values
sf data query --query "SELECT Value, IsActive FROM PicklistValueInfo WHERE EntityParticle.EntityDefinition.QualifiedApiName = 'Account' AND EntityParticle.QualifiedApiName = 'Industry'" --target-org dev

# List record types
sf data query --query "SELECT DeveloperName, Name, IsActive FROM RecordType WHERE SObjectType = 'Account'" --target-org dev

# List profiles
sf data query --query "SELECT Id, Name FROM Profile ORDER BY Name" --target-org dev

# List objects
sf data query --query "SELECT QualifiedApiName, Label, IsCustom FROM EntityDefinition WHERE IsCustomizable = true ORDER BY Label" --target-org dev
```

## Browser (Playwright)

Use the OpenClaw browser tool to navigate Salesforce Setup UI.

### Getting a Login URL
```bash
# Get frontdoor URL for browser login
sf org open --target-org dev --url-only
```

### Common Setup Navigation
After logging in via the browser tool:
- **Setup Home:** `/lightning/setup/SetupOneHome/home`
- **Object Manager:** `/lightning/setup/ObjectManager/home`
- **Specific Object:** `/lightning/setup/ObjectManager/<ObjectApiName>/FieldsAndRelationships`
- **Permission Sets:** `/lightning/setup/PermSets/home`
- **Profiles:** `/lightning/setup/EnhancedProfiles/home`
- **Page Layouts:** Object Manager → [Object] → Page Layouts

### When to Use Browser vs Metadata API
| Task | Preferred Method |
|------|-----------------|
| Add/edit custom fields | Metadata API (SF CLI) |
| Update page layouts | Metadata API (SF CLI) |
| Update permissions (FLS, CRUD) | Metadata API (SF CLI) |
| Manage picklist values | Metadata API (SF CLI) |
| Compact layouts | Browser (Setup UI) |
| Lightning page assignments | Browser (Setup UI) |
| Quick actions | Browser (Setup UI) |
| Verify changes visually | Browser (Setup UI) |
| Troubleshoot layout issues | Browser (Setup UI) |
| Record type page layout assignment | Either (browser is often easier) |

## RAG Knowledge Base

Search for Salesforce admin documentation:
```bash
rag search "page layout best practices"
rag search "field level security"
rag search "picklist values metadata"
rag search "record type configuration"
```

## Delegation

### DevOps → Piper
When changes need to be promoted between orgs or handled through CI/CD, delegate to Piper:
- Provide the list of metadata components
- Specify source and target orgs
- Let Piper handle the pipeline

### Code → Code Monkey 🐒
If a request needs Apex, LWC, triggers, or any code:
- Hand it off to Code Monkey
- Provide context about what the code needs to do
- You handle the declarative side; Code Monkey handles the code side

## Metadata XML Quick Reference

### Custom Field (in .object-meta.xml or standalone)
```xml
<fields>
    <fullName>My_Field__c</fullName>
    <label>My Field</label>
    <type>Text</type>
    <length>255</length>
    <required>false</required>
    <description>Description of the field</description>
    <inlineHelpText>Help text for users</inlineHelpText>
</fields>
```

### Picklist Field
```xml
<fields>
    <fullName>Status__c</fullName>
    <label>Status</label>
    <type>Picklist</type>
    <required>false</required>
    <valueSet>
        <restricted>true</restricted>
        <valueSetDefinition>
            <sorted>false</sorted>
            <value>
                <fullName>Active</fullName>
                <default>true</default>
                <label>Active</label>
            </value>
            <value>
                <fullName>Inactive</fullName>
                <default>false</default>
                <label>Inactive</label>
            </value>
        </valueSetDefinition>
    </valueSet>
</fields>
```

### Layout Field Entry
```xml
<layoutItems>
    <behavior>Edit</behavior>
    <field>My_Field__c</field>
</layoutItems>
```

### Permission Set Field Permission
```xml
<fieldPermissions>
    <editable>true</editable>
    <field>Account.My_Field__c</field>
    <readable>true</readable>
</fieldPermissions>
```

### Permission Set Object Permission
```xml
<objectPermissions>
    <allowCreate>true</allowCreate>
    <allowDelete>false</allowDelete>
    <allowEdit>true</allowEdit>
    <allowRead>true</allowRead>
    <modifyAllRecords>false</modifyAllRecords>
    <object>My_Object__c</object>
    <viewAllRecords>false</viewAllRecords>
</objectPermissions>
```

### Record Type
```xml
<recordTypes>
    <fullName>Business_Account</fullName>
    <active>true</active>
    <label>Business Account</label>
    <picklistValues>
        <picklist>Industry</picklist>
        <values>
            <fullName>Technology</fullName>
            <default>false</default>
        </values>
    </picklistValues>
</recordTypes>
```
