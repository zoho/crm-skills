FILE_PURPOSE: Read when authoring or refactoring a Client Script — applying the ten documented best practices for static-resource reuse, event-arg usage, layout coverage, Trusted-Domains whitelist, and 10 s-timeout loader pattern.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/client-script-best-practices.html
TRIGGER_KEYWORDS: ZDK.Page.getField, ZDK.Client.showLoader, ZDK.Client.hideLoader, ZDK.Apps.CRM.Functions.execute, Trusted Domains, Reorder, log statement, Static Resources, 30 scripts per page

TECHNICAL_CONSTRAINTS:
- Client Script execution is bounded by a 10-second timeout; long-running ZDK Web (CRM) API or third-party calls must be wrapped in a loader to pause the user-perceived flow.
- Hard cap — up to 30 Client Scripts per page.
- Hard cap — up to 5 Static Resources per page (echoes [clientscript-static-resources.dou.md](./clientscript-static-resources.dou.md)).
- Per-event argument injection — each event handler receives a documented argument variable; the handler reads the injected variable directly instead of re-fetching via ZDK.
- Reorder of script execution order is scoped to a single Page + Event combo within a module — cross-event / cross-page ordering is not configurable.
- Third-party API calls from Client Script require the target domain to be whitelisted in `Trusted Domains` before the request will succeed.

REQUIRED_PARAMETERS:
- Per-event injected arguments (from source's event-argument table):
    · Create / Clone / Edit Page — Page `onChange` → `field_name`; Page `onLoad` → none; Page `onSave` → none; Field `onChange` → `value`.
    · Detail Page (Canvas) — Page `onLoad` → none; Field `onBeforeUpdate` → `value`; Mandatory Fields Form `onBeforeMandatoryFormSave` → `value`, `onMandatoryFormLoad` → `field`; Blueprint `beforeTransition` → `transition`; Tag `onTagChanged` → `tag, added and removed`; Canvas / Icon / Text `onClick` → none.
    · Detail Page (Standard) — same shape as Detail (Canvas).
    · List Page (Standard) — Page `onCustomViewLoad` → `custom_view`; `onBeforeCustomViewChange` → `custom_view`.
    · Create / Edit Page (Wizard) — Wizard `onLoad` → none; `onChange` → `field_name`; `onTransition` → `screen`; `onBeforeTransition` → `source_screen, target_screen`; `onBeforeSave` → none; Field `onChange` → `value`.
- Loader pattern (10 s timeout workaround):
    ```javascript
    if (value == 'Delivered') {
      ZDK.Client.showLoader({ type: 'page', template: 'spinner', message: 'Sending Quotation...' });
      ZDK.Apps.CRM.Functions.execute("Send_Quote");
      ZDK.Client.hideLoader();
      ZDK.Client.showMessage('Quotation sent successfully', { type: 'success' });
    }
    ```
- Static-resource reuse — extract repeated logic (e.g. SSN regex `is_socialSecurity_Number`) into a JS file uploaded as a Static Resource, then call by bare function name from the script.
- Multi-field handling on the same page — prefer one Page `onChange` script with `switch(field_name)` over multiple Field `onChange` scripts.
- Debug logging — `log(...)` statements surface in the IDE Run → Messages panel; do not rely on browser `console.log` (see [clientscript-ide-components.dou.md](./clientscript-ide-components.dou.md)).
- Ad-hoc ZDK invocation — use the Run → Terminal panel (e.g. `ZDK.Client.showMessage('...', { type: 'info' })`) to test ZDK calls without saving a script.
- Event-type → use-case mapping (Best Practice #9, source-verbatim):
    · Pre-save validation across the whole record — Page `onSave`.
    · Validation as soon as data is entered on a single field — Field `onChange`.
    · Validation as soon as data is entered across multiple fields — Page `onChange` (with `switch(field_name)`).
    · Custom message / information box on page open — Page `onLoad`.

UI_ONLY_ACTIONS:
- Reorder scripts within a Page + Event combo: `Setup → Developer Hub → Client Script → Reorder` (scoped to one Page + Event per module). Note: No API equivalent — UI-only.
- Whitelist a third-party domain: add the domain under `Setup → Developer Space → Trusted Domains` before the script's `fetch` will succeed. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- ZDK Web (CRM) API call inside an `onType` handler exhausts API credits; prefer `onChange` or page-level events for API-bearing logic. (rate-limit)
- Skipping the loader on a > 10 s ZDK / third-party call: execution halts at 10 s; user-perceived save / transition appears frozen. (timeout)
- Third-party `fetch(...)` to a non-whitelisted domain returns a network error; add the domain to Trusted Domains before retry. (trusted-domain)
- Multiple Field `onChange` scripts on the same page create ordering ambiguity even with Reorder applied; consolidate into one Page `onChange` with a `switch(field_name)`.
- Layout binding — Client Scripts execute only for the configured layout; multi-layout coverage requires one script per layout (see [clientscript-overview.dou.md](./clientscript-overview.dou.md)). (layout-binding)
- The injected `value` argument is scoped to the current event family — `value` in Field `onChange` is the new field value; in Mandatory-Form events it is the form-level map. Reusing the variable name across event types misreads the payload.
- 30-script cap per page — adding a 31st script is rejected; consolidate using `switch` blocks.
- `field_name` argument is provided only on Page `onChange` and Wizard `onChange` per the source table — relying on it inside Page `onLoad` / `onSave` returns `undefined`.
