FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on List Page (Canvas) — canonical wire signature including canvas-element per-record click hooks.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_list_page_canvas
TRIGGER_KEYWORDS: onLoad, onBeforeCustomViewChange, onClick, Canvas Button, Icon, Text, custom_view, context

TECHNICAL_CONSTRAINTS:
- Page-type scope — List Page (Canvas layout). For List Page (Standard), see eventdict-list-standard.
- Interceptor event — Page `onBeforeCustomViewChange`. `return false` blocks the view-change.
- Canvas-element events here **do take a `context` arg** (unlike Canvas Create / Detail surfaces where canvas-element `onClick` takes no args) — each click returns the record ID of the canvas row clicked.
- Custom Button binding configured only from the Buttons page.

REQUIRED_PARAMETERS:
- **Page events** (Type: Page Event):
    · `onLoad()` — fires when the List Page (Canvas) loads. No args.
    · `onBeforeCustomViewChange(custom_view)` — **Interceptor**. Fires before custom-view change. `custom_view` = `{ ID, name }`. `return false` cancels.
- **Canvas Button event** (Type: Canvas Button Event): `Canvas Button onClick(context)` — `context` = `{ Record ID, Module API name, ID }`.
- **Icon event** (Type: Icon Event): `Icon onClick(context)` — `context` = `{ Record ID, Module API name, ID }`.
- **Text event** (Type: Text Event): `Text onClick(context)` — `context` = `{ Record ID, Module API name, ID }`.
- **Button event** (Type: Button Event): `onClick()` — fires on Client-Script-configured custom button click. **No `context` arg listed on this surface** (contrast with List-Standard which exposes 3 placement-variant contexts).

UI_ONLY_ACTIONS:
- Canvas list-row design (which buttons / icons / text appear per row): `Setup → Customization → Canvas → <list canvas> → Row Design`. Note: No API equivalent — UI-only.
- Custom Button (top-bar) placement on Canvas list: `Setup → Customization → Modules and Fields → <Module> → Links and Buttons → Buttons`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **Canvas-element `onClick` has `context` HERE but no `context` on Detail / Create canvas surfaces** — cross-surface scripts that read `context.record_id` work on List Canvas but read `undefined` on Detail / Create Canvas. (cross-surface-arg-shape)
- **Button `onClick` takes no `context` on List Canvas** per this source (contrast with List Standard's 3 placement-variants: Util Menu, Each Record, Mass Action Menu). Scripts that need selected-record IDs from a Mass Action button on List Canvas have no documented event signature.
- **No Field / Subform / Mandatory Form / Blueprint / Tag / Notes events** — List Canvas is read-only at the field level; record-level edits must navigate to Detail / Edit.
- **No record-selection event** — there is no `onRecordSelect` or `onSort`. Per-row interactions must hook the per-row canvas-element clicks.
- **`onBeforeCustomViewChange` blocks only the view-switch** — does not block URL navigation away from the page.
- **List Canvas is not in the mobile-supported page matrix** (`../clientscript-mobile.dou.md` lists no List Canvas row) — scripts silently no-op on mobile. (mobile-listpage-absent)
- **No Page `onChange` / `onSave` events** — only `onLoad` and the view-change interceptor.
