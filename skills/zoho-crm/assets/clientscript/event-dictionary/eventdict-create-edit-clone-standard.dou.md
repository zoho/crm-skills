FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on Create / Edit / Clone Page of a Standard layout — canonical wire signature.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_create_edit_clone_standard
TRIGGER_KEYWORDS: onLoad, onChange, onSave, onType, onRowAdd, onCellChange, beforeRowDelete, onClick, Interceptor

TECHNICAL_CONSTRAINTS:
- Page-type scope — Standard Create Page, Edit Page, Clone Page (one event-dictionary covers all three).
- Interceptor events accept `return false` at end-of-script to cancel the gesture; non-interceptor events cannot block.
- Field events fire per-field; Page-level `onChange` fires for any field change on the page and dispatches the field's API name.
- Subform events are scoped to a specific subform; the script binds to a subform handle via `getSubform(<subform_api_name>)`.
- Custom Button `onClick` Client Scripts are configured **only** from the Buttons page (not from the Client Script setup list directly); existing scripts then appear on the Client Script setup page.

REQUIRED_PARAMETERS:
- **Page events** (Type: Page Event):
    · `onLoad()` — fires when the create/clone/edit page loads. No args.
    · `onChange(field_name)` — `field_name` = API name of the modified field. Supported field types: Single Line, Multi-Line, Email, Phone, Pick List, Date, Number, Currency, Decimal, Percent, Long Integer, Checkbox, URL, Lookup, Owner Lookup, Multi-select Picklist.
    · `onSave()` — **Interceptor**. Fires after Save / Save and New click, before persistence. `return false` cancels save.
- **Field events** (Type: Field Event):
    · `onChange(value)` — `value` = current value in the field. Fires on blur / focus-out after edit. Supported field types: identical to Page-onChange list above (incl. Multi-select Picklist).
    · `onType(value)` — `value` = current value. Fires per keystroke / per type event.
- **Subform events** (Type: Subform Event; bound to a subform):
    · `onRowAdd(row_data, index)` — `row_data` = object details of newly added row; `index` = its row index.
    · `onCellChange(field_name, value, index)` — `field_name` = edited cell's field API name; `value` = new value; `index` = row index.
    · `onRowDelete(row_data, index)` — fires after row deletion. `row_data` / `index` as above.
    · `beforeRowDelete(row_data, index)` — **Interceptor**. Fires after delete-icon click, before row removal. `return false` cancels deletion.
- **Button event** (Type: Button Event):
    · `onClick(context)` — `context` returns `{ Module API Name, ID }`.

UI_ONLY_ACTIONS:
- Custom Button Client Script binding — `Setup → Customization → Modules and Fields → <Module> → Links and Buttons → Buttons → Create / select button → action = Client Script`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- `onChange` (Page or Field) does not fire on field types outside the source-enumerated supported list above — silent listener miss. (unsupported-field-type)
- `field_name` in Page `onChange` is the field **API name**, not the display label — `switch(field_name) { case "Last_Name": ... }` works, `case "Last Name"` does not. (label-vs-api-name)
- `onSave` `return false` cancels save **only when returned synchronously**; an async `return false` after a `Promise` resolves leaves the save uncancelled.
- `beforeRowDelete` is **camelCase** in this event-dictionary; the legacy `client-script-events.html` doc spells it `BeforeRowDelete` (PascalCase). Treat the event-dictionary spelling as authoritative for new scripts. (case-mismatch)
- **No `onBeforeUpdate` field event on Create/Edit/Clone Standard** — only Detail Page exposes field `onBeforeUpdate`. Attempting that hook on the create surface registers no listener.
- **No Mandatory-Form events on Create/Edit/Clone Standard** — Mandatory Form fires only on Detail-Page surfaces.
- **No Subform `beforeRowUpdate`** — only Detail-Page subforms expose `beforeRowUpdate`; subform-row edits on Create/Edit cannot be intercepted.
- Custom Button `context` does **not** include selected related-list IDs on this surface — that variant only exists on Detail Page button context. (button-context-shape)
- Per-layout binding — script bound to one layout does not fire on other layouts of the same module. (layout-binding)
