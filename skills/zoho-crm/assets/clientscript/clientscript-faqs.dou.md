FILE_PURPOSE: Read when answering operational Client Script questions — supported JS, scopes, layouts, debugging, unsupported APIs, setCriteria operators, Detail-Page setValue restriction, JS-method blocklist.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/faqs.html, https://www.zohocrm.dev/explore/client-script/faqs
TRIGGER_KEYWORDS: setCriteria, setValue, getInput, getForm, setValues, log, JSON.stringify, param_type, addTooltip, console.log

TECHNICAL_CONSTRAINTS:
- Language: JavaScript only — no other languages supported (FAQ #5). ES7 features supported including `let`, `const`, async functions (FAQ #19, #21).
- One Client Script binds to exactly one module-layout pair; multi-layout coverage requires one script per layout (FAQ #6).
- Execution timeout — 10 s; use a loader when exceeding (FAQ #43).
- Connection invocation `param_type` map (FAQ #23): `param_type = 1` → request parameter; `param_type = 2` → request body / payload.
- ZDK Web API calls from a Client Script consume the org's daily Zoho CRM API limit — every ZDK Web API execution counts (FAQ #2).
- `setCriteria(...)` operators supported (FAQ #27): only `starts_with` and `equals`. Other operators silently rejected.
- Contextual lookup filter (FAQ #32) — supported on single-lookup field only; Multi-select lookup contextual filter not yet supported.
- Static Resources scope (FAQ #28) — per-page; any script on the same page can use them.
- Custom libraries — upload as Static Resource and consume (FAQ #33).
- 3rd-party calls only to URLs in Trusted Domains (FAQ #34).
- Run-mode does not require Save before testing (FAQ #29); Run-mode CRM operations DO persist to the live account (per FAQ #4 note).
- Browser support — matches Zoho CRM's supported-browsers list (FAQ #12).
- Mobile coverage — see separate mobile DOU node; FAQ does not enumerate mobile events.
- Hover support — `addTooltip()` shows a hover tooltip; no `onHover` event exists (FAQ #38).
- Custom event creation not supported (FAQ #22) — only the documented event catalog fires.
- Alert line breaks — `\n` inside `ZDK.Client.showAlert(...)` renders multi-line (FAQ #46).
- **onChange Field vs onChange Page** (new-mirror FAQ) — bind Field `onChange` when the script must run only for one specific field's update; bind Page `onChange` when any field-update on the page must trigger the same script (use `if`/`switch..case` on the changed field inside the handler). Field-level fires for the bound field only; Page-level fires for every field on the page.
- **Display 3rd-party content (PDF, HTML, web page) inside CRM** (new-mirror FAQ) — there is no direct Client-Script render API for external HTML/PDF; the supported pattern is to render a Widget and open it via `ZDK.Client.openPopup` / Callout / Flyout. Client Script invokes the Widget; the Widget loads the external content.

REQUIRED_PARAMETERS:
- Lookup `setValue` requires both id and name (FAQ #3): `ZDK.Page.getField('Category').setValue({ "id": "<record_id>", "name": "<display_name>" })`.
- Subform get/set values — `ZDK.Page.getForm().getValues()` and `getForm().setValues(...)` (FAQ #14, #35); `getForm()` returns all fields on the current page (Create/Clone/Edit).
- Debug log — `log(<value>)` writes to the IDE Messages panel; `console.log(<value>)` writes to the browser console (FAQ #4, #20).
- Stringified ZDK response — `log("response stringified:", JSON.stringify(ZDK.Apps.CRM.Leads.fetch()))` (FAQ #45).
- Cancel save on validation failure — `onSave` event + `field.showError(<msg>)` (or `ZDK.Client.showMessage` / `showAlert`) + `return false` (FAQ #9).
- Detail Page (Canvas/Standard) field updates — `setValue` on direct fields is **not** supported; use the Update Record Web API + `$Client.refresh()` to re-render the page (FAQ #25, #42). Detail-Page Mandatory-Form fields **do** support `setValue`.
- Lookup fetch — `ZDK.Page.getField('Lookup').getValue()` returns `{ id, name }` (FAQ #26).
- Detail-Page Canvas linked-field cascade — must call `$Client.refresh()` after Web-API write to surface the change (FAQ #42).
- Disabling buttons — both custom and system buttons can be enabled/disabled via Client Script (FAQ #30, #37). Pre-delete validation is **not** supported (FAQ #37).
- Pseudo fields — `getInput()` creates a pop-up with pseudo fields scoped to the current execution (FAQ #40).
- **Dynamic forms from Dynamic-field values** (new-mirror FAQ) — three supported paths: (a) `getInput()` to build a pop-up form from pseudo fields driven by Dynamic-field values; (b) render a Widget that builds the form, then pass values back to the Page via Client Script; (c) `setVisibility()` to hide/show existing Page fields based on Dynamic values.
- **Dynamically populate one field from another field's input** (new-mirror FAQ) — supported via `onChange-field` (or Page `onChange`) handler reading source field and writing target field; see the `populate-age-based-on-date-of-birth-entered` code sample on `zohocrm.dev/developerspace/client-script/codesamples`.

UI_ONLY_ACTIONS:
- `localStorage` / `window.localStorage` — **not permitted** (FAQ #18). No alternate browser storage equivalent.
- Pages where Client Script runs (FAQ #10, #31): Create Page, Edit Page, Clone Page, Detail Page (Canvas), Detail Page (Standard), List Page (Standard), Create Page (Wizard), Edit Page (Wizard). Note: Quick Create is **excluded** per FAQ #11 — see SOURCE_CONFLICT below.
- ZDK reference inside the IDE — `Setup → Developer Hub → Client Script IDE → Library → Information → Help icon` (FAQ #1). Note: No API equivalent — UI-only.
- **Terminal section of the Client Script IDE** (new-mirror FAQ) — executes ZDK API statements instantly without binding to an event. Typing e.g. `ZDK.Client.showMessage('Welcome to Client Script IDE', { type: 'info' });` and pressing Enter renders the message immediately. Use for ad-hoc ZDK probing; no script-save required. UI-only surface, no programmatic equivalent.

CRITICAL_FAILURE_MODES:
- **JS method blocklist** (FAQ #44) — calling any of the following silently fails or breaks the script: `postMessage`, `importScripts`, `close`, `addEventListener`, `removeEventListener`, `getEventListeners`, `WebSocket`, `setInterval`, `setTimeout`, `clearTimeout`, `clearInterval`, `Worker`, `MessagePort`, `MessageEvent`, `MessageChannel`, `onmessage`, `onmessageerror`, `window`, `document`. (no-timer / no-dom)
- **Detail Page field-write silent no-op**: calling `field.setValue(...)` on a Detail Page (Canvas or Standard) direct field does nothing (FAQ #25). Must route through Web-API Update Record + `$Client.refresh()`. (detail-page-setvalue)
- **Linked-field cascade requires reload**: in Detail Page (Canvas), a linked field reads stale until `$Client.refresh()` is called; Detail Page (Standard) has no comparable refresh API yet (FAQ #42). (cascade-stale)
- **setCriteria operator silent-reject**: any operator other than `starts_with` / `equals` is ignored, returning the unfiltered lookup list (FAQ #27). (filter-operator-binding)
- **Multi-select lookup contextual filter unsupported**: `setCriteria` on a multi-select lookup does not narrow choices (FAQ #32). (multi-select-filter)
- **Lookup setValue without id**: setting only `{name: "..."}` on a lookup field silently saves nothing; both id and name required (FAQ #3). (lookup-id-missing)
- **Custom event creation impossible**: there is no API to register new event triggers — only the documented event catalog fires (FAQ #22). (custom-events-absent)
- **Pre-delete validation impossible**: `beforeDelete`-style hook does not exist for records; only `beforeRowDelete` for subform rows (FAQ #37). (no-pre-delete)
- **Per-layout binding**: a script tagged to one layout does not fire on other layouts of the same module; missing layout coverage looks like a silent listener miss (FAQ #6). (layout-binding)
- **Run-mode side-effects persist**: Run-mode CRM writes hit the live tenant (FAQ #4 note) — destructive samples can mutate production data.
- **SOURCE_CONFLICT — Quick Create**: FAQ #11 says "currently Client Script in Zoho CRM cannot be executed in Quick Create Page", but the dedicated event-dictionary page `module_quick_create` enumerates `onLoad/onChange/onSave/onChange-field/onType-field` for Quick Create Popup. Treat the event-dictionary as authoritative; FAQ entry is stale.
- **Portals — unsupported ZDK calls**: the following silently fail / are blocked when the script runs under a Portal User context: `ZDK.Apps.CRM.Functions.execute()`, `ZDK.Apps.CRM.Connections.invoke()`, `ZDK.Page.addTag()`, `ZDK.Page.removeTag()`, `ZDK.Page.getTags()`, `ZDK.Page.getList().freezeColumns`, `ZDK.Page.getList().selectRecords()`, `ZDK.Page.getList().clearSelection()`, `ZDK.Client.openMailer()`. (portal-unsupported)
- **Canvas copy-icon button — not yet shipped**: adding a copy-to-clipboard custom-icon action inside a Canvas view via Client Script is "under development" — no working API today. (canvas-copy-unavailable)
- **Flyout formatted text without Widget — not yet supported**: rendering rich/formatted text inside a Flyout currently requires rendering a Widget; a text-only formatted Flyout is on the feasibility-check list, not shipped. (flyout-richtext-absent)
