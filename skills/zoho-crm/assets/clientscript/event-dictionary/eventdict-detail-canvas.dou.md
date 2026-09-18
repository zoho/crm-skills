FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on Detail Page (Canvas) — canonical wire signature including canvas-element, Blueprint, Mandatory Form, Tag, Notes hooks.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_view_canvas
TRIGGER_KEYWORDS: onLoad, onBeforeUpdate, beforeTransition, onBeforeMandatoryFormSave, onTagChanged, beforeRowUpdate, Canvas Button, onBeforeAdd

TECHNICAL_CONSTRAINTS:
- Page-type scope — Detail Page (Canvas layout). For Detail Page (Standard), see eventdict-detail-standard.
- Interceptor events: Field `onBeforeUpdate`, Blueprint `beforeTransition`, Mandatory Form `onBeforeMandatoryFormSave`, Subform `beforeRowDelete` / `beforeRowUpdate`, Notes `onBeforeAdd` / `onBeforeUpdate`.
- Canvas-only event families: Canvas Button `onClick()`, Icon `onClick()`, Text `onClick()` — no args.
- Detail Page has no direct field write-through; field edits go through Mandatory Form or Web-API Update Record + `$Client.refresh()`.

REQUIRED_PARAMETERS:
- **Page event** (Type: Page Event): `onLoad()` — fires when the canvas page loads. No args.
- **Field event** (Type: Field Event): `onBeforeUpdate(value)` — **Interceptor**. Fires on tick-icon click after inline field edit. `value` = current value. `return false` cancels. Supported field types: Single Line, Multi-Line, Email, Phone, Pick List, Date, Number, Currency, Decimal, Percent, Long Integer, Checkbox, URL, Lookup, Owner Lookup. **Multi-select Picklist is NOT in this list** (contrast with standard Create/Edit `onChange` list).
- **Mandatory Fields Form events** (Type: Mandatory Fields Form Event):
    · `onBeforeMandatoryFormSave(value)` — **Interceptor**. `value` = values of the fields in Mandatory form + base-field current value. `return false` cancels. **Note: arg name is `value`, not `form`** (Detail-Standard uses `form`).
    · `onMandatoryFormLoad(field)` — `field` = `{ base field API name, value }`.
- **Blueprint event** (Type: Blueprint Event): `beforeTransition(transition)` — **Interceptor**. `transition` = `{ ID, name }`. `return false` cancels.
- **Tag event** (Type: Tag Event): `onTagChanged(tags_added, tags_removed)` — **two** args: `tags_added` = list of tags added; `tags_removed` = list of tags removed. (No `tag` arg here, contrast with Detail-Standard which has 3-arg `(tag, added, removed)`.)
- **Canvas Button event** (Type: Canvas Button Event): `Canvas Button onClick()` — no args.
- **Icon event** (Type: Icon Event): `Icon onClick()` — no args.
- **Text event** (Type: Text Event): `Text onClick()` — no args.
- **Subform events** (Type: Subform Event):
    · `onRowAdd(row_data, index)`, `onCellChange(field_name, value, index)`, `onRowDelete(row_data, index)` — non-interceptor.
    · `beforeRowDelete(row_data, index)` — **Interceptor**. `return false` cancels deletion.
    · `beforeRowUpdate(row_data, index)` — **Interceptor**. `return false` cancels update.
- **Button event** (Type: Button Event): `onClick(context)` — **shape-variant**:
    · In Record → `{ Module API Name, ID }`.
    · Related List → `{ Module API Name of the related list, ID, selected record ID }`.
- **Notes events** (Type: Notes Related List — no "Event" suffix):
    · `onBeforeAdd(notes)` — **Interceptor**. `notes` = `{ title, content }`. `return false` blocks add.
    · `onBeforeUpdate(notes)` — **Interceptor**. `notes` = `{ title, content }`. `return false` blocks update.

UI_ONLY_ACTIONS:
- Canvas-element binding — `Setup → Customization → Canvas → <canvas> → element → Actions → Client Script`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **Tag event arg shape differs across Detail surfaces** — Canvas = `(tags_added, tags_removed)` 2-arg; Standard = `(tag, added, removed)` 3-arg. Cross-surface scripts that read `tag` on Canvas get `undefined`. (cross-surface-arg-shape)
- **Mandatory-Form `onBeforeMandatoryFormSave` arg differs across Detail surfaces** — Canvas = `value`; Standard = `form`. Cross-surface scripts read the wrong shape. (cross-surface-arg-shape)
- **Field `onBeforeUpdate` does NOT include Multi-select Picklist** on this Canvas surface — clicking save on an MSP field bypasses the interceptor. (msp-intercept-absent)
- **Field `setValue` silently no-op on Detail Page** — direct field writes do nothing; use Mandatory-Form fields or Web-API Update Record + `$Client.refresh()`. (detail-page-setvalue)
- **Linked-field cascade requires `$Client.refresh()`** — Detail Canvas does not re-render automatically after a Web-API write. (cascade-stale)
- **Canvas-element `onClick` events take no args** — derive record-id from `getForm().getValues()` or `$Page.record.id`. (no-canvas-context)
- **Button `context` shape varies by placement** — In Record vs Related List shapes differ. (button-context-placement)
- **`beforeTransition` blocks transition only, not parallel listener side-effects** — listener-order matters. (listener-order)
- **Blueprint `afterTransition` not in this surface** — mobile Detail-Standard exposes it; cross-surface scripts diverge.
