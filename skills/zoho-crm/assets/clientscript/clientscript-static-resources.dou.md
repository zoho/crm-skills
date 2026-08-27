FILE_PURPOSE: Read when adding reusable JS modules to a Client Script via Static Resources — confirming upload limits, the 5-per-page import cap, and the no-DOM / no-window restriction.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/static-resources.html
TRIGGER_KEYWORDS: Static Resources, ZDK.Page.getField, ZDK.Client.showConfirmation, ZDK.Client.showMessage, .js upload, 5 MB resource, 200 files

TECHNICAL_CONSTRAINTS:
- Edition gating — Static Resources feature is available in Enterprise, Ultimate and Professional editions of Zoho CRM.
- File type — JS files only.
- Hard caps — each file ≤ 5 MB; up to 200 files per org; up to 5 static resources imported per Client Script page; all imported resources are available to every script on that page.
- `document` and `window` references are not available during Client Script execution; DOM- or window-dependent libraries must not be uploaded as static resources.
- Resource upload is served from a static server; reference the resource by Name from the IDE Static Resources panel.
- Functions defined in a static resource are callable directly from any Client Script that imports the resource (e.g. `is_socialSecurity_Number(ssn)` inside a script after `ssnCheck.js` is added).
- Minified JS distribution is recommended in source to reduce network latency.

REQUIRED_PARAMETERS:
- Upload payload — Name, Description, File (a .js file ≤ 5 MB).
- Per-script import — open the IDE Static Resources panel (right pane, below Information) and click `Add` next to the resource Name; Remove via hover → Remove on the Added row.
- Invocation contract — call the exported function by its bare name (no namespace) from inside the Client Script body; combine with `ZDK.Page.getField("API_Name")` to read field values.

UI_ONLY_ACTIONS:
- Upload a Static Resource: `Setup → Developer Hub → Client Script → Static Resources tab → New Resource → Name + Description + Choose File → Save`. Note: No API equivalent — UI-only.
- Add resource to a script: open the script in the IDE → right-pane Static Resources icon → `Add` next to the resource Name. Note: No API equivalent — UI-only.
- Remove resource from a script: in the right-pane Static Resources panel, hover the Added row and click `Remove`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- Uploading a non-JS file: rejected; only `.js` is accepted.
- File > 5 MB: rejected at upload time; minify or split before re-uploading.
- 200-file cap hit: new uploads rejected; delete unused resources to free slots.
- Importing a 6th resource on the same script page: rejected at the cap of 5 per page; consolidate logic into fewer files.
- Static resource containing `document.*` / `window.*` / DOM access executes inside an environment where those globals are absent → the call throws at runtime and the dependent script halts. (sandbox-binding)
- Field API names quoted in the static resource (e.g. `ZDK.Page.getField("SSN")`) must match the module's field API name exactly; quoting a display label silently returns no field. (label-vs-api-name)
