# Experience Cloud — Sanguine Bio

## Overview

Sanguine Bio uses Salesforce Experience Cloud for external-facing portals that allow partner sites, donors, and other external stakeholders to interact with the platform.

## Current Portals

### Partner Site Portal
- **Purpose:** External portal for research partner sites to manage interactions with Sanguine Bio
- **Users:** Partner site coordinators, principal investigators
- **Key Features:**
  - View and manage studies/projects
  - Track sample shipments and status
  - Communication with Sanguine Bio team
  - Document sharing and management

## Architecture

### User Access
- **Community User Profiles:** Separate from internal profiles
- **Permission Sets:** Grant specific access per portal role
- **Sharing Rules:** Control data visibility between partner sites
- **Guest User:** Limited pre-authentication access (login page, public info)

### Components
- Portal pages built with **Lightning Web Components (LWC)**
- Components must work in both Lightning Experience and Community contexts
- Use `@api` properties for configurable components in Experience Builder
- Follow responsive design patterns for mobile access

### Security Considerations
- All portal components must respect sharing rules (use `with sharing` in Apex)
- Field-level security enforced through permission sets
- No direct access to internal-only objects or fields
- CRUD/FLS checks in all Apex controllers serving portal pages

## Development Notes

- **Testing portal components:** Deploy to dev sandbox, configure community, test with community user
- **Experience Builder:** Used for page layout and component placement (declarative)
- **Custom themes:** Can override default styling with custom CSS in the community
- **URL format:** `[domain].force.com/[community-name]/s/`
