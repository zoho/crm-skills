FILE_PURPOSE: Read when debugging a Client Script — using the in-IDE `log()` Messages panel and the in-browser `debugger;` pause / inspect workflow with Chrome DevTools source maps.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/troubleshooting.html
TRIGGER_KEYWORDS: log statement, debugger, ZDK.Page.getField, JavaScript Source Maps, DevTools, F12, Cmd+Option+I, Ctrl+Shift+I

TECHNICAL_CONSTRAINTS:
- `log(...)` writes to the IDE Run → Messages panel; it surfaces only when the script is executed via the IDE Run option.
- `debugger;` is the standard JavaScript debugger statement — when encountered with the browser DevTools open, the browser pauses execution at that line; with DevTools closed, the statement is a no-op.
- DevTools shortcut keys (source-verbatim): Windows / Linux — `Ctrl + Shift + I` or `F12`; Mac — `Cmd + Option + I`.
- Source-map mapping back to the original Client Script source requires enabling `JavaScript Source Maps` in Chrome DevTools settings.
- Only two debugging primitives are documented on this page: `log` and `debugger`.

REQUIRED_PARAMETERS:
- `log(<expression>)` — call to emit a Messages-panel entry; runs only under IDE Run.
- `debugger;` — bare statement; place at any line where execution should pause once DevTools is open.
- DevTools enablement — open DevTools before the user action that triggers the script; pre-trigger is required because the statement is no-op when DevTools is closed.

UI_ONLY_ACTIONS:
- Open the Messages panel for log inspection: open the script in the IDE → click Run → execute → Messages panel at the bottom. Note: No API equivalent — UI-only.
- Enable JavaScript Source Maps: Chrome DevTools → Settings → check `JavaScript Source Maps`. Note: Browser-side toggle; no CRM API equivalent.

CRITICAL_FAILURE_MODES:
- `debugger;` left in a saved script + a user runs the script with DevTools open → unrelated end-users hit the pause line and their CRM page freezes; strip `debugger;` before activating.
- `debugger;` with DevTools closed = no-op — relying on it in a production debug pass without instructing the operator to open DevTools yields zero visibility.
- `log(...)` calls do not surface anywhere outside the IDE Run → Messages panel — they are invisible to end-users and provide no production telemetry.
- Source-map view diverges from the saved Client Script body when Source Maps is disabled in DevTools — debugger pauses on the transformed source and variable names do not align.
- The page documents only `log` and `debugger`; profile / layout / Developer-Permissions silent no-fire modes are not covered here (see [clientscript-overview.dou.md](./clientscript-overview.dou.md)).
