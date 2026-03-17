# TOOLS.md — Spec Ops

## Salesforce CLI — Org Research

**Org aliases:**
- `prod` — Production (READ only)
- `dev` — Development sandbox (default)
- `qa` — QA sandbox

### Discover the Data Model
```bash
# List custom objects
sf data query --query "SELECT DeveloperName, Label, Description FROM EntityDefinition WHERE IsCustomizable = true AND IsCustomSetting = false ORDER BY Label" --target-org dev

# Fields on a specific object
sf data query --query "SELECT DeveloperName, DataType, Label, Description, IsRequired FROM FieldDefinition WHERE EntityDefinition.DeveloperName = 'MyObject'" --target-org dev

# Record types on an object
sf data query --query "SELECT DeveloperName, Name, Description, IsActive FROM RecordType WHERE SObjectType = 'MyObject__c'" --target-org dev

# Page layouts
sf data query --query "SELECT Name, TableEnumOrId FROM Layout WHERE TableEnumOrId = 'MyObject__c'" --target-org dev

# Validation rules
sf data query --query "SELECT ValidationName, Active, Description, ErrorMessage FROM ValidationRule WHERE EntityDefinition.DeveloperName = 'MyObject'" --target-org dev
```

### Discover Existing Components
```bash
# LWC components in the repo
find /home/node/.openclaw/workspace/salesforce -name "*.js-meta.xml" -path "*/lwc/*" | sort

# Apex classes
find /home/node/.openclaw/workspace/salesforce -name "*.cls" | sort

# Apex triggers
find /home/node/.openclaw/workspace/salesforce -name "*.trigger" | sort

# Flows
find /home/node/.openclaw/workspace/salesforce -name "*.flow-meta.xml" | sort

# Permission sets
find /home/node/.openclaw/workspace/salesforce -name "*.permissionset-meta.xml" | sort

# Read a specific file
cat /home/node/.openclaw/workspace/salesforce/force-app/main/default/classes/SomeClass.cls
```

### Discover Users & Permissions
```bash
# Profiles
sf data query --query "SELECT Name FROM Profile WHERE UserType = 'Standard' ORDER BY Name" --target-org dev

# Permission sets
sf data query --query "SELECT Name, Label, Description FROM PermissionSet WHERE IsCustom = true ORDER BY Label" --target-org dev

# Connected apps
sf data query --query "SELECT Name, ContactEmail FROM ConnectedApplication ORDER BY Name" --target-org dev
```

### Data Volume & Shape
```bash
# Record counts
sf data query --query "SELECT COUNT() FROM Account" --target-org dev
sf data query --query "SELECT COUNT() FROM Case" --target-org dev

# Sample records to understand data patterns
sf data query --query "SELECT Id, Name, RecordType.Name, CreatedDate FROM MyObject__c ORDER BY CreatedDate DESC LIMIT 10" --target-org dev
```

## RAG Knowledge Base

Search for Salesforce documentation and patterns:
```bash
rag search "experience cloud portal setup"
rag search "custom login flow lightning"
```

## File Operations

Write specs to the sf-dev workspace:
```bash
# Specs go here
/home/node/.openclaw/workspace/sf-dev/specs/{project-name}/
```
