FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on Detail Page (Standard) — canonical wire signature including Blueprint, Mandatory Form, Tag, Notes hooks.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_detail
TRIGGER_KEYWORDS: onLoad, onBeforeUpdate, beforeTransition, onBeforeMandatoryFormSave, onMandatoryFormLoad, onTagChanged, beforeRowUpdate, onBeforeAdd

TECHNICAL_CONSTRAINTS:
- Page-type scope — Detail Page (Standard layout). For Detail Page (Canvas), see eventdict-detail-canvas.
- Detail Page has **no** field write-through (`setValue`) — field edits go through Mandatory Form pop-up or Web-API Update Record. See `../clientscript-faqs.dou.md` for the workaround.
- Interceptor events: `onBeforeUpdate` (field), `beforeTransition` (blueprint), `onBeforeMandatoryFormSave`, `beforeRowDelete` / `beforeRowUpdate` (subform), `onBeforeAdd` / `onBeforeUpdate` (notes).
- Mandatory Form events fire when a field edit triggers the system's "fill required fields" pop-up.
- Notes events scope to the Notes Related List only.

REQUIRED_PARAMETERS:
- **Page event** (Type: Page Event): `onLoad()` — fires on detail-page load. No args.
- **Field event** (Type: Field Event): `onBeforeUpdate(value)` — **Interceptor**. Fires on tick-icon click after inline field edit. `value` = current value. `return false` cancels the save. (Source does not enumerate supported field types here.)
- **Blueprint event** (Type: Blueprint Event): `beforeTransition(transition)` — **Interceptor**. `transition` = `{ ID, name }` of the current transition. `return false` cancels the blueprint transition.
- **Mandatory Fields Form events** (Type: Mandatory Fields Form Event):
    · `onBeforeMandatoryFormSave(form)` — **Interceptor**. `form` = values of all fields in the mandatory form + current value of the base field. `return false` cancels.
    · `onMandatoryFormLoad(form)` — fires when the mandatory-form pop-up opens. `form` = same shape.
- **Tag event** (Type: Tag Event): `onTagChanged(tag, added, removed)` — **three** args: `tag` = list of tags; `added` = list of tags added; `removed` = list of tags removed. Fires on Save of the Add-Tags dialog.
- **Subform events** (Type: Subform Event):
    · `onRowAdd(row_data, index)`, `onCellChange(field_name, value, index)`, `onRowDelete(row_data, index)` — non-interceptor; signatures identical to create/edit/clone.
    · `beforeRowDelete(row_data, index)` — **Interceptor**. `return false` cancels deletion.
    · `beforeRowUpdate(row_data, index)` — **Interceptor**. Fires after tick-icon click during inline row update. `return false` cancels.
- **Button event** (Type: Button Event): `onClick(context)` — `context` is **shape-variant**:
    · In Record placement → `{ Module API Name, ID }`.
    · Related List placement → `{ Module API Name of the related list, ID, selected record ID }`.
- **Notes events** (Type: Notes Related List — no "Event" suffix; Related List Notes only):
    · `onBeforeAdd(notes)` — **Interceptor**. `notes` = `{ title, content }` of the note about to be added. `return false` blocks the add.
    · `onBeforeUpdate(notes)` — **Interceptor**. `notes` = `{ title, content }` of the note about to be updated. `return false` blocks the update.

UI_ONLY_ACTIONS:
- Custom Button placement (Record top-bar vs. Related List) is chosen at button creation: `Setup → Customization → Modules and Fields → <Module> → Links and Buttons → Buttons → Placement`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **Field `setValue` silently no-op on Detail Page** — direct field writes do nothing; only Mandatory-Form fields support `setValue`. Use Web-API Update Record + `$Client.refresh()`. (detail-page-setvalue)
- **Tag event arg shape differs across surfaces** — Detail Standard = `(tag, added, removed)` 3-arg; Detail Canvas = `(tags_added, tags_removed)` 2-arg. Scripts ported across surfaces hit `undefined` args. (cross-surface-arg-shape)
- **Mandatory-Form `onBeforeMandatoryFormSave` arg shape differs across surfaces** — Detail Standard = `form` (full form values + base); Detail Canvas = `value`. (cross-surface-arg-shape)
- **Button `context` shape varies by placement** — assuming the In-Record shape on a Related-List button silently reads `undefined` for the selected record ID. (button-context-placement)
- **`beforeRowUpdate` exists only on Detail-Page subforms** — not on Create/Edit/Clone subforms; cross-surface scripts hit silent no-listener.
- `beforeRowDelete` / `beforeRowUpdate` are **camelCase**; legacy `client-script-events.html` uses PascalCase (`BeforeRowDelete` / `BeforeRowUpdate`). Treat event-dictionary as authoritative.
- `beforeTransition` only blocks the transition — it does **not** revert state changes already made by other listeners; chain ordering matters. (listener-order)
- Blueprint `afterTransition` is **absent** here but present in the mobile Detail-Standard matrix; cross-surface scripts that key on `afterTransition` fire on mobile only. (cross-surface-blueprint)
- `onTagChanged` fires only on Save of the Add-Tags dialog, not on row-level inline tag edits.
