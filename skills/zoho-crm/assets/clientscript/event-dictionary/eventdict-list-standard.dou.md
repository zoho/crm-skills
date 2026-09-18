FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on List Page (Standard) — canonical wire signature for custom-view and list-button hooks.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_list
TRIGGER_KEYWORDS: onCustomViewLoad, onBeforeCustomViewChange, onClick, custom_view, Util Menu, Mass Action

TECHNICAL_CONSTRAINTS:
- Page-type scope — List Page (Standard layout). For List Page (Canvas), see eventdict-list-canvas.
- Only two Page events exist — view-load and view-change. There is **no** Page `onLoad`, `onChange`, `onSave`, or `onType` on List Page (Standard).
- Interceptor event — `onBeforeCustomViewChange`. `return false` blocks the view-change.
- Custom Button binding — configured only from the Buttons page; existing scripts appear on the Client Script setup list after creation.

REQUIRED_PARAMETERS:
- **Page events** (Type: Page Event):
    · `onCustomViewLoad(custom_view)` — fires when a custom view loads. `custom_view` = `{ ID, name }` of the current custom view.
    · `onBeforeCustomViewChange(custom_view)` — **Interceptor**. Fires before the user changes the current custom view. `custom_view` = `{ ID, name }`. `return false` cancels the change.
- **Button event** (Type: Button Event): `onClick(context)` — `context` is **shape-variant by placement**:
    · Util Menu placement → `{ Module API Name, ID }`.
    · Each Record placement → `{ Module API Name, ID, record ID }`.
    · Mass Action Menu placement → `{ Module API Name, ID, selected record IDs (array) }`.

UI_ONLY_ACTIONS:
- Custom Button placement (Util Menu vs. Each Record vs. Mass Action Menu): chosen at button creation under `Setup → Customization → Modules and Fields → <Module> → Links and Buttons → Buttons → Placement`. Note: No API equivalent — UI-only.
- Custom-view creation (the target of `onCustomViewLoad`): `Setup → ... → <Module> → List → Create View`. Note: No API equivalent for the script-binding side — UI-only.

CRITICAL_FAILURE_MODES:
- **Button `context` shape varies by placement** (3 variants) — code that assumes `context.record_id` (Each Record shape) on a Util Menu button hits `undefined`; code that assumes a single `record_id` on a Mass Action button misses the array. (button-context-placement)
- **No record-level events on List Page (Standard)** — there is no `onRowClick`, `onRecordSelect`, or `onSort` event. Such logic must live in a custom button or in row-level styling via `ZDK.Page.getList().style(...)` invoked in `onCustomViewLoad`.
- **No `onLoad` Page event** — initial-page-load logic must hook `onCustomViewLoad`, which fires per custom-view switch (including initial default-view load).
- **`onBeforeCustomViewChange` blocks only the view-switch** — it does not block other navigation away from the list page; URL navigation away triggers no event.
- **Custom-view delete / rename is not hooked** — `onBeforeCustomViewChange` does not fire on view metadata changes, only on which view is currently active.
- **List-Page scripts are silently absent on mobile** — see `../clientscript-mobile.dou.md`. (mobile-listpage-absent)
- **Mass-Action selected-IDs array can be large** — combined with the 10 s execution cap, iterating many selected records via Web API risks timeout. (timeout)
