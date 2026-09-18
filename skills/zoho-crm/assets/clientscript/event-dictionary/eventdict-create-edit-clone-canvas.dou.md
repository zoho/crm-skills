FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on Create / Clone / Edit Page (Canvas) — canonical wire signature including canvas-button / icon / text hooks.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_create_edit_clone_canvas
TRIGGER_KEYWORDS: onLoad, onChange, onSave, onType, onMandatoryFormLoad, Canvas Button, Icon, Text, beforeRowDelete

TECHNICAL_CONSTRAINTS:
- Page-type scope — Canvas Create Page, Edit Page, Clone Page (one event-dictionary covers all three).
- Interceptor events: Page `onSave`, Subform `beforeRowDelete`.
- Canvas-only event families: Canvas Button `onClick()`, Icon `onClick()`, Text `onClick()` — these fire on click of canvas-design elements and take no args.
- Mandatory Form has only the load hook here (`onMandatoryFormLoad`); there is **no** `onBeforeMandatoryFormSave` on Canvas Create/Edit/Clone.
- Custom Button binding configured only from the Buttons page.

REQUIRED_PARAMETERS:
- **Page events** (Type: Page Event):
    · `onLoad()` — fires when the canvas create/clone/edit page loads. No args.
    · `onChange(field_name)` — `field_name` = API name of the modified field. Supported field types: Single Line, Multi-Line, Email, Phone, Pick List, Date, Number, Currency, Decimal, Percent, Long Integer, Checkbox, URL, Lookup, Owner Lookup, Multi-select Picklist.
    · `onSave()` — **Interceptor**. Fires after Save / Save and New click, before persistence. `return false` cancels save.
- **Field events** (Type: Field Event):
    · `onChange(value)` — `value` = current value. Fires on blur. Supported field types: same as Page-onChange list above (incl. Multi-select Picklist).
    · `onType(value)` — `value` = current value. Fires per keystroke.
- **Mandatory Form event** (Type: Mandatory Fields Form Event): `onMandatoryFormLoad(field)` — `field` = `{ base field API name, value }`.
- **Canvas Button event** (Type: Canvas Button Event): `Canvas Button onClick()` — no args, fires on click of a canvas button.
- **Icon event** (Type: Icon Event): `Icon onClick()` — no args, fires on click of a canvas icon.
- **Text event** (Type: Text Event): `Text onClick()` — no args, fires on click of canvas text.
- **Subform events** (Type: Subform Event):
    · `onRowAdd(row_data, index)`, `onCellChange(field_name, value, index)`, `onRowDelete(row_data, index)` — non-interceptor.
    · `beforeRowDelete(row_data, index)` — **Interceptor**. `return false` cancels deletion.
- **Button event** (Type: Button Event): `onClick(context)` — `context` returns `{ Module API Name, ID }`.

UI_ONLY_ACTIONS:
- Canvas-element script binding — `Setup → Customization → Canvas → <canvas> → select element (Button / Icon / Text) → Actions → Client Script`. Note: No API equivalent — UI-only.
- Custom Button (top-bar) binding — `Setup → Customization → Modules and Fields → <Module> → Links and Buttons → Buttons → Placement`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **SOURCE_CONFLICT — Field `onBeforeUpdate`**: legacy `client-script-events.html` documents `onBeforeUpdate` (Field) for Multi-select Lookup on Canvas Create/Edit/Clone, but this event-dictionary lists **only** `onChange` and `onType` under Field events. Treat event-dictionary as authoritative for new scripts; legacy `onBeforeUpdate` may not fire here. (event-absent-in-wire-signature)
- **No `onBeforeMandatoryFormSave` on Canvas Create/Edit/Clone** — only `onMandatoryFormLoad`; mandatory-form-save interception is not possible on this surface. (intercept-gap)
- **No Subform `beforeRowUpdate`** — only `beforeRowDelete`; subform-row in-place edits cannot be intercepted.
- **No Blueprint / Tag / Notes events** — those fire only on Detail surfaces; cross-surface scripts hit silent no-listener.
- **Canvas-element `onClick` events take no args** — there is no `context` for Canvas Button / Icon / Text; deriving record-id requires reading the form state via `getForm().getValues()`. (no-canvas-context)
- **`onChange` does not fire on field types outside the source-enumerated supported list above** — silent listener miss. (unsupported-field-type)
- **`field_name` arg is API name, not display label** — `case "Last_Name"` works, `case "Last Name"` does not. (label-vs-api-name)
- **Per-layout binding** — script bound to one Canvas layout does not fire on other layouts. (layout-binding)
