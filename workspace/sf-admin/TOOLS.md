# TOOLS.md — Click Ops (SF Admin Agent)

## Salesforce CLI

**Org aliases:**
- `prod` — Production (READ ONLY unless explicitly told otherwise)
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

# Retrieve multiple items
sf project retrieve start --metadata "CustomField:Account.My_Field__c,Layout:Account-Account_Layout" --target-org dev --output-dir temp/
```

### Metadata Deployment
```bash
# Deploy from a directory
sf project deploy start --source-dir temp/ --target-org dev

# Deploy with specific tests (if needed)
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
```

## RAG Knowledge Base

Search for Salesforce admin documentation:
```bash
rag search "page layout best practices"
rag search "field level security"
rag search "picklist values metadata"
```

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
