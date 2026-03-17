# Case Gantt / Kanban LWC

## Overview
Custom Lightning Web Component providing a Kanban-style view for Salesforce Cases. Part of the existing casebase at `C:\Code\case-gant`.

## What It Does
- **Kanban board** for visualizing Case workflow
- Cases displayed as cards across status columns
- Drag-and-drop to change status
- Integrated with the DevOps pipeline (Source_Change__c object)

## Key Components
- **caseGanttChart** — Main LWC component (Kanban board)
- **Source_Change__c** — Custom object for tracking code/metadata changes
- **n8n webhook** — Triggers DevOps operations

## Architecture
```
LWC (caseGanttChart)
  → Apex Controller (CRUD operations)
  → Case records (standard object)
  → Source_Change__c (custom object for change tracking)
  → n8n webhook (DevOps pipeline trigger)
```

## Location
- **Source code:** Part of `sanguinebio/salesforce` repository
- **Original dev location:** `C:\Code\case-gant`
- **Components:** `force-app/main/default/lwc/caseGanttChart/`
