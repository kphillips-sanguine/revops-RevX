# LWC Development Patterns — Sanguine Bio

## Component Architecture

### Container vs Presentational Components

**Container components** handle data:
```javascript
// caseListContainer.js — fetches data, manages state
import { LightningElement, wire } from 'lwc';
import getCases from '@salesforce/apex/CaseController.getCases';

export default class CaseListContainer extends LightningElement {
    @wire(getCases)
    cases;
    
    handleCaseSelected(event) {
        const caseId = event.detail.caseId;
        // Navigate or update state
    }
}
```

**Presentational components** render UI:
```javascript
// caseCard.js — receives data via @api, renders it
import { LightningElement, api } from 'lwc';

export default class CaseCard extends LightningElement {
    @api caseRecord;
    
    get statusClass() {
        return this.caseRecord.Status === 'Closed' ? 'slds-badge_success' : 'slds-badge';
    }
}
```

### Rules
- **Container components** do data fetching, state management, and business logic
- **Presentational components** receive data via `@api` and emit events
- **Keep components small** — if over 300 lines of JS, split it
- **One responsibility per component**

## Data Patterns

### Wire Service (for read operations)
```javascript
import { LightningElement, wire } from 'lwc';
import getRecords from '@salesforce/apex/MyController.getRecords';

export default class MyComponent extends LightningElement {
    @wire(getRecords, { accountId: '$recordId' })
    wiredRecords;
}
```
- **Reactive** — automatically re-fetches when parameters change
- **Cached** — Lightning Data Service manages caching
- **Use for:** Read-only data display, lookup queries

### Imperative Apex (for DML and complex operations)
```javascript
import saveRecord from '@salesforce/apex/MyController.saveRecord';

async handleSave() {
    try {
        const result = await saveRecord({ record: this.formData });
        this.dispatchEvent(new ShowToastEvent({
            title: 'Success',
            message: 'Record saved',
            variant: 'success'
        }));
    } catch (error) {
        this.dispatchEvent(new ShowToastEvent({
            title: 'Error',
            message: error.body?.message || 'Unknown error',
            variant: 'error'
        }));
    }
}
```
- **Use for:** Create, update, delete operations
- **Always handle errors** with try/catch
- **Show toast notifications** for user feedback

### Lightning Data Service (single record CRUD)
```html
<lightning-record-form
    record-id={recordId}
    object-api-name="Case"
    fields={fields}
    mode="edit"
    onsuccess={handleSuccess}>
</lightning-record-form>
```
- **Use for:** Simple single-record forms
- **Benefits:** Built-in validation, FLS enforcement, no Apex needed

## Event Patterns

### Child → Parent (Custom Events)
```javascript
// Child dispatches
this.dispatchEvent(new CustomEvent('caseselected', {
    detail: { caseId: this.case.Id }
}));

// Parent handles
<c-case-card oncaseselected={handleCaseSelected}></c-case-card>
```

### Cross-component (Lightning Message Service)
```javascript
import { publish, MessageContext } from 'lightning/messageService';
import CASE_CHANNEL from '@salesforce/messageChannel/CaseSelected__c';

@wire(MessageContext) messageContext;

selectCase(caseId) {
    publish(this.messageContext, CASE_CHANNEL, { caseId: caseId });
}
```
- **Use for:** Communication between unrelated components on the same page
- **Create Message Channel** metadata for each communication pattern

## Experience Cloud Considerations

When building LWCs for Experience Cloud portals:

### Exposed Properties
```xml
<!-- myComponent.js-meta.xml -->
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>59.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightningCommunity__Page</target>
        <target>lightningCommunity__Default</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightningCommunity__Default">
            <property name="title" type="String" label="Title" default="My Component"/>
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

### Key Rules for Portal Components
- Include `lightningCommunity__Page` and `lightningCommunity__Default` targets
- Use `@api` properties for Experience Builder configurability
- **Always use `with sharing` in Apex** — portal users have different sharing context
- Test with community user profiles, not admin
- **Responsive design** — portal users may be on mobile
- **Accessibility** — ARIA labels, keyboard navigation, screen reader support

## Styling

### SLDS (Salesforce Lightning Design System)
- **Always use SLDS classes** for consistent look and feel
- Reference: https://www.lightningdesignsystem.com/
- Use `slds-` utility classes for layout, spacing, typography

### Custom CSS
```css
/* myComponent.css */
:host {
    display: block;
}

.custom-header {
    padding: var(--lwc-spacingMedium);
    border-bottom: 1px solid var(--lwc-colorBorder);
}
```
- **Use CSS custom properties** from SLDS for theming consistency
- **Scope styles** — LWC shadow DOM keeps styles contained
- **No !important** unless overriding SLDS base components

## Error Handling

```javascript
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { reduceErrors } from 'c/ldsUtils';

handleError(error) {
    const messages = reduceErrors(error);
    this.dispatchEvent(new ShowToastEvent({
        title: 'Error',
        message: messages.join(', '),
        variant: 'error',
        mode: 'sticky'
    }));
}
```

### `reduceErrors` utility (create in a shared utils component):
```javascript
// ldsUtils.js
export function reduceErrors(errors) {
    if (!Array.isArray(errors)) errors = [errors];
    return errors
        .filter(error => !!error)
        .map(error => {
            if (Array.isArray(error.body)) return error.body.map(e => e.message);
            if (error.body && typeof error.body.message === 'string') return error.body.message;
            if (typeof error.message === 'string') return error.message;
            return error.statusText || 'Unknown error';
        })
        .flat();
}
```
