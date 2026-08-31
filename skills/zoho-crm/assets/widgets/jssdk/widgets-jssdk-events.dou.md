FILE_PURPOSE: Read when authoring a Widget bootstrap — wiring `ZOHO.embeddedApp.on` listeners (PageLoad / Dial / Notify / ContextUpdate) before the single `init()` call against JS-SDK v1.5.
SOURCE_DOC: widgets/create-widget.md, https://www.zohocrm.dev/explore/widgets/v1.5/jssdk
TRIGGER_KEYWORDS: ZOHO.embeddedApp, ZOHO.embeddedApp.on, ZOHO.embeddedApp.init, PageLoad, DialerActive, Dial, Notify, NotifyAndWait, ContextUpdate, widget.html

TECHNICAL_CONSTRAINTS:
- JS-SDK version pinned at v1.5 — load `https://live.zwidgets.com/js-sdk/1.5/ZohoEmbededAppSDK.min.js` inside `app/widget.html` before any `ZOHO.embeddedApp.*` call.
- Bootstrap script lives in `app/widget.html`; CLI lifecycle is owned by [widgets-zet-cli.dou.md](../widgets-zet-cli.dou.md); runtime sandbox + SDK surfaces are owned by [widgets-overview.dou.md](../widgets-overview.dou.md).
- Single global `ZOHO.embeddedApp.init()` boots the listener registry — call exactly once per Widget bootstrap; activates listeners already registered.
- Six listener events registered via `ZOHO.embeddedApp.on(...)`: `DialerActive`, `Dial`, `Notify`, `NotifyAndWait`, `PageLoad`, `ContextUpdate`. `init` is the bootstrap method, not a listenable event — registering `on("init", ...)` no-ops.
- `PageLoad` is the canonical entity-context event; payload exposes API-named context — for example `{ "Entity": "Leads", "EntityId": "3000000032096" }` on record / related-list surfaces. Non-record locations (Web Tab, Settings, Dashboard) ship reduced payload that can omit `EntityId`.
- `ContextUpdate` fires on every Wizard-form field edit — debounce before triggering side effects.
- `NotifyAndWait` runs synchronously against the ClientScript flyout — caller blocks until the widget invokes `ZDK.Client.sendResponse(data.id, payload)`.
- `Dial` fires when the CRM call icon is clicked; `DialerActive` fires whenever the softphone window is toggled.
- `Notify` carries the ClientScript flyout `notify()` payload; `NotifyAndWait` carries the same plus a `data.id` UUID.
- CDN URL is DC-agnostic — the same `live.zwidgets.com` host serves every CRM data centre.
- Widget iframe reloads on every host-page navigation — listener registry resets per page mount.
- All `ZOHO.CRM.*` data / UI / config calls must be issued from inside a `PageLoad` (or equivalent) callback so the SDK runtime is fully initialised.
- Optional `.js` companions and stylesheets live alongside `widget.html` under `app/`; the entry HTML controls which assets the iframe loads.

REQUIRED_PARAMETERS:
- Authoring artefact — `app/widget.html`; CRM data calls routed through the JS SDK (see [widgets-jssdk-api.dou.md](./widgets-jssdk-api.dou.md)).
- Listener signature: `ZOHO.embeddedApp.on(eventName: string, callback: (data: any) => void): void`.
- Bootstrap signature: `ZOHO.embeddedApp.init(): void` — no arguments.
- Bootstrap contract (mandatory order — listener BEFORE init):
  ```javascript
  ZOHO.embeddedApp.on("PageLoad", function(data) {
      // data.Entity / data.EntityId — API names, not display labels
  });
  ZOHO.embeddedApp.init();
  ```
- `NotifyAndWait` callback `data.id` is a UUID and is the first argument of `ZDK.Client.sendResponse(id, payload)` (see [widgets-jssdk-client.dou.md](./widgets-jssdk-client.dou.md)).
- Sample / reference Widgets — `zohocrm.dev/explore/widgets/codesamples`.

UI_ONLY_ACTIONS:
- In-context testing requires associating the saved Widget with a host component — see [widgets-usage.dou.md](../widgets-usage.dou.md) for the full association flow. Note: No API equivalent.

CRITICAL_FAILURE_MODES:
- Listener registered AFTER `ZOHO.embeddedApp.init()` never fires — no console warning, no `PageLoad` callback. Register every `on()` before the single `init()` call. (listener-order)
- Same event subscribed twice via `on()` executes the callback twice per event — guard against double-registration in framework re-renders.
- `PageLoad` payload field accessed by display label (`"Lead Status"`) instead of API name (`Lead_Status`): returns `undefined` silently — `label-vs-api-name`.
- Multiple `ZOHO.embeddedApp.init()` calls in one load: undefined behavior — keep `init()` as the final bootstrap line.
- Direct browser visit to `https://127.0.0.1:<port>/app/widget.html` for testing (default ZET port defined in `server/index.js`): `ZOHO.embeddedApp.*` runtime is absent because no CRM host is present — always test in-context via CRM (Internal or External hosting).
- `PageLoad` not fired on Dashboard placement or when widget is accessed directly in a browser tab: if the widget fetches only external data and needs no CRM record context, add a `setTimeout` fallback (~1500 ms) after `ZOHO.embeddedApp.init()` to trigger the fetch if `PageLoad` has not fired; use a `fetchCalled` boolean guard to prevent double-invocation.
- CDN URL pinned to an older minor (e.g. `1.4`) when code calls a v1.5-only event: event never fires — pin to v1.5 explicitly.
- `init()` invoked inside an async `then` handler racing against later listener registration: listeners arriving after sync init resolution miss the first `PageLoad`.
- `ContextUpdate` handler that triggers a CRM API write per keystroke: workflow recursion + rate-limit risk — debounce before writing.
- `ZOHO.CRM.CONFIG.getCurrentUser()` (or any `ZOHO.CRM.*` call) invoked before `init()` resolves: rejects / returns undefined — defer into the `PageLoad` callback.
- Long-running synchronous work inside `PageLoad`: blocks subsequent listeners and freezes the host record page — chunk into async tasks.
- Write calls (`ZOHO.CRM.API.updateRecord` / `insertRecord` / `upsertRecord`) issued without an explicit `trigger` map fire workflows / blueprints / approvals — pass the explicit `trigger` subset only when suppression is intended (see parent SKILL Top-5 #3). (automation-interaction)
- Exceptions thrown inside the `PageLoad` callback are swallowed by the SDK runtime: wrap risky code in try / catch and log explicitly to surface failures in devtools.
- `sendResponse` for `NotifyAndWait` never called because of an early `return` / thrown exception: caller hangs until ClientScript timeout — wrap callback in try / finally and always respond.
- Custom event name typo passed to `on()` (e.g. `"pageload"` lowercase): SDK silently ignores — event names are case-sensitive PascalCase verbatim.
- `Notify` / `NotifyAndWait` payload assumed to carry an `EntityId`: neither event guarantees record context — cross-reference the originating ClientScript flyout config.
- `DialerActive` listener attached without paired teardown on Widget unmount: duplicate listeners accumulate across SPA navigation — remove on unmount.
- Single-page-app reuses one Widget iframe across virtual route changes: stale closures still hold the first `PageLoad` data — re-fetch context from `data` each event, do not cache.
- `ZOHO.embeddedApp.on('Dial', ...)` registered without a paired softphone integration installed: callback never fires — feature-detect via `ZOHO.CRM.UI.Dialer` presence.
- `init()` called in a React `useEffect` without empty dependency array: re-runs per render and re-boots the SDK — use empty deps + cleanup.
- Listener callback that returns a Promise: SDK does not await it for events other than `NotifyAndWait` — do not rely on async completion for event ordering.
- `init()` skipped under the assumption that listeners self-bootstrap: nothing fires — `init()` is the only trigger that flushes the registry.
- Bootstrap script loaded with `defer` while inline `<script>` after it calls `ZOHO.embeddedApp.on(...)`: SDK not yet defined at call time — load order matters.
- Mixing `ZOHO.embeddedApp.on` with raw `window.addEventListener('message', ...)`: postMessage path is undocumented — stick to SDK events.
- `ContextUpdate` payload assumed to contain the full record snapshot: source describes Wizard-form modification only — it does not promise the entire record.
- Source file edited without refreshing the host CRM page: iframe serves the cached bundle — reload the CRM page.
