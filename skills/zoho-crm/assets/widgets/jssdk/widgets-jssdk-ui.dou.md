FILE_PURPOSE: Read when manipulating CRM UI from a Widget — resize iframe, open record forms, open WebTab Widgets, control Dialer, and close popups via `ZOHO.CRM.UI.*`.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_UI, https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_UI_Popup, https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_UI_Dialer, https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_UI_Record, https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_UI_Widget
TRIGGER_KEYWORDS: ZOHO.CRM.UI, Resize, Popup.close, closeReload, Dialer.maximize, Record.create, Record.edit, Record.open, Record.populate, UI.Widget.open

TECHNICAL_CONSTRAINTS:
- Five UI sub-namespaces — `UI`, `UI.Popup`, `UI.Dialer`, `UI.Record`, `UI.Widget`. All methods return Promises resolved with `true | false`.
- `UI.Resize({ height, width })`: dimensions in **pixels** as integers — applies to the Widget container iframe.
- `UI.Popup.close()` / `UI.Popup.closeReload()`: scoped to widgets opened as popups (e.g. Custom Button widgets). `closeReload` triggers a reload of the underlying CRM view; `close` does not.
- `UI.Dialer.maximize() | minimize() | notify()`: scoped to telephony / call-center widgets only — `notify` plays an audible alert.
- `UI.Record.create({ Entity })` opens the create form; `UI.Record.edit({ Entity, RecordID })` and `UI.Record.open({ Entity, RecordID })` open edit / detail forms.
- `UI.Record.populate(RecordData)` pre-fills the **currently open** create / edit form using field API name keys — only valid while a record form is mounted in the host CRM context.
- `UI.Widget.open({ Entity, Message })` opens a target WebTab Widget by its WebTab name and passes `Message` (any JSON-serializable object) — the target widget receives it via its `PageLoad` event payload.
- `Entity` is the module API name / SysRefName; for `UI.Widget.open`, `Entity` is the WebTab Widget's name (not its display label).
- Dialer methods apply only when the org has a telephony integration installed and the CallCenter window is registered with CRM.

REQUIRED_PARAMETERS:
- `UI.Resize({ height: number, width: number })` — integers, pixels.
- `UI.Popup.close()` / `UI.Popup.closeReload()` — no args.
- `UI.Dialer.maximize() | minimize() | notify()` — no args.
- `UI.Record.create({ Entity })`.
- `UI.Record.edit({ Entity, RecordID })`.
- `UI.Record.open({ Entity, RecordID })`.
- `UI.Record.populate(RecordData)` — object keyed by field API names.
- `UI.Widget.open({ Entity, Message })` — `Entity` is WebTab Widget name; `Message` is any serializable payload.

UI_ONLY_ACTIONS:
- Map a WebTab Widget so `UI.Widget.open` can target it: `Setup → Customization → Modules and Fields → {module} → Web Tabs`. Note: no SDK equivalent — WebTab placement is admin-only.
- Bind a Widget to a Custom Button (popup): `Setup → Customization → Modules and Fields → {module} → Links and Buttons → Custom Buttons`. Note: `UI.Popup.close*` only applies to widgets launched via this binding.

CRITICAL_FAILURE_MODES:
- `UI.Resize` dimensions passed as strings with `px` suffix (e.g. `"200px"`): SDK accepts numeric strings per source examples, but mixed unit suffixes silently no-op — pass plain integer strings or numbers.
- `UI.Popup.close*` invoked from a Widget that was **not** opened as a popup: resolves `false`, no UI change — branch on the resolution value.
- `closeReload` vs `close` confusion: caller wants the host list / record view refreshed after a write but uses `close()` — view shows stale data.
- `UI.Record.populate` called before the create / edit form mount finishes rendering: data is dropped silently — listen for the host form's ready event before populating.
- `UI.Record.populate` keyed by field display labels instead of API names: fields silently unfilled — `label-vs-api-name`.
- `UI.Record.create / edit / open` `Entity` is the module display label (`"Contact"`) instead of module API name (`Contacts`): navigation fails.
- `UI.Widget.open` `Entity` populated with the WebTab display label instead of the WebTab Widget name: target never opens — `label-vs-api-name`.
- `UI.Widget.open` target Widget caches its first `PageLoad.Message` payload across re-opens: subsequent re-opens pass new `Message` but UI shows the first — re-read `data` on every `PageLoad`, never cache outside the event closure.
- `UI.Dialer.*` invoked when no telephony integration is registered: resolves `false` — feature-detect before exposing dialer controls.
- `UI.Resize` invoked on a Widget hosted in a non-resizable location (e.g. a fixed-size dashboard tile): resolves `false`, no UI change — verify location supports resize via parent-skill [widgets-usage.dou.md](../widgets-usage.dou.md).
- `UI.Record.edit` `RecordID` for a record the user lacks update permission on: navigation opens but save fails downstream — pre-check via [widgets-jssdk-meta.dou.md](./widgets-jssdk-meta.dou.md) profile / layout data.
- Calling `UI.Popup.closeReload` from a popup that just performed a `zoho.crm.update` with `{"trigger":[]}`: workflow / blueprint state still stale on the reloaded view — see parent-skill Top-5 Gotcha #3.
- `UI.Record.populate` invoked on a detail-page-only context (no edit form mounted): silently no-op — gate on the current form mode from `PageLoad`.
- `UI.Resize` invoked repeatedly inside a window-resize handler: layout thrash — debounce or throttle the call.
- `UI.Widget.open` `Message` payload containing a `Date` object: JSON-serialization drops the type — stringify ISO-8601 before send and parse on receive.
- `UI.Dialer.notify` invoked while the host page is muted by browser autoplay policy: audible alert silently suppressed — accompany with a visual cue.
- `UI.Record.open` for a record in a module the user can read but not edit: opens detail page only — caller expecting an edit form must use `edit` and handle 403.
- `UI.Record.create` `Entity` for a custom module whose layouts vary per profile: form opens with default layout, not the user's profile-bound layout — layout binding is admin-set, not caller-controlled.
- `UI.Popup.close` invoked twice from the same click handler: second call rejects — guard with a `done` flag.
- `UI.Widget.open` target Widget bound to a WebTab the current user lacks profile access to: navigation no-ops silently — feature-detect via [widgets-jssdk-meta.dou.md](./widgets-jssdk-meta.dou.md) `getModules`.
