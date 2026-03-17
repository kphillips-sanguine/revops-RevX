# Integrations — Sanguine Bio Salesforce

## Integration Architecture

```
Salesforce ←→ n8n Workflows ←→ External Services
    ↑                              ↑
    └── Platform Events ───────────┘
    └── REST API ──────────────────┘
    └── Outbound Messages ─────────┘
```

## n8n Workflow Automation

### Instance
- **URL:** https://n8n-z5fpv.sevalla.app
- **Hosting:** Sevalla VPS
- **Purpose:** Orchestrates multi-step workflows between Salesforce and external services

### Common Patterns

#### SF → n8n → External Service
1. Salesforce triggers an action (record change, platform event, scheduled)
2. n8n webhook receives the event
3. n8n processes data, calls external APIs
4. n8n callbacks to Salesforce with results

#### External Service → n8n → SF
1. External service sends webhook to n8n
2. n8n transforms and validates data
3. n8n creates/updates records in Salesforce via REST API

### Key Workflows
- **AI Agent Orchestration:** SF chat UI → n8n → Gemini/Claude → SF Platform Events
- **DevOps Pipeline:** GitHub webhook → n8n → SF CLI operations → status update to SF
- **Data Sync:** Scheduled sync between systems via n8n cron triggers

## Sevalla Proxy Server

### Instance
- **URL:** https://sevalla-ru8at.sevalla.app
- **Source:** `C:\Code\sevalla` (Docker on Sevalla VPS)
- **Purpose:** Hosts SF CLI + git for operations that need CLI access

### Capabilities
- SF CLI commands (deploy, retrieve, query, test)
- Git operations (clone, branch, commit, push)
- API endpoint for n8n workflows to trigger CLI operations
- Used by the DevOps Tool pipeline

## Platform Events

### What They Are
- Real-time messaging system within Salesforce
- Publish from Apex, Flow, or external via API
- Subscribe in LWC (empApi), Apex triggers, or external via CometD

### Pattern for AI Agents
```
User sends chat message (LWC)
  → Apex publishes Agent_Request__e platform event
  → n8n subscribes and receives the event
  → n8n calls AI model (Gemini/Claude) with tool calling
  → AI responds with tool calls → n8n executes them
  → n8n publishes Agent_Response__e platform event
  → LWC subscribes and displays response in real-time
```

### LWC Subscription Example
```javascript
import { subscribe } from 'lightning/empApi';

connectedCallback() {
    subscribe('/event/Agent_Response__e', -1, (message) => {
        this.handleAgentResponse(message.data.payload);
    });
}
```

## REST API

### Inbound (External → Salesforce)
- **Connected Apps** for OAuth authentication
- **Named Credentials** for secure credential storage
- Custom REST endpoints via `@RestResource` Apex classes

### Outbound (Salesforce → External)
- **HTTP Callouts** from Apex (named credentials preferred)
- **Outbound Messages** from workflow rules (legacy, SOAP-based)
- **External Services** — register OpenAPI specs, auto-generates Apex

### Authentication Patterns
- **Named Credentials** (preferred) — credentials managed in Setup, not in code
- **Custom Metadata** — store API keys and endpoints as custom metadata records
- **Never hardcode** credentials in Apex or LWC
