FILE_PURPOSE: Read when picking the Page Type + Event Family + Event Name for a Client Script — confirming per-page event lists, supported/unsupported field types, and `return false` cancel semantics.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/client-script-events.html
TRIGGER_KEYWORDS: onLoad, onChange, onSave, onBeforeUpdate, beforeTransition, onBeforeMandatoryFormSave, BeforeRowDelete, onCustomViewLoad, onType, onTagChanged

TECHNICAL_CONSTRAINTS:
- For a fast Page→Type→Events lookup table (including the exact "Type" dropdown value and where each Type is configured), see [clientscript-event-type-matrix.dou.md](./clientscript-event-type-matrix.dou.md).
- Event-configurable pages — Create page, Clone page, Edit page, List Page (Standard), Detail Page (Standard), Detail Page (Canvas), Create Page (Wizard), Edit Page (Wizard), Create / Clone / Edit Page (Canvas), List Page (Canvas), Quick Create popup.
- Field `onChange` fires when focus leaves the field; `onType` fires as the user keys characters.
- Layout binding — picking a layout during script creation restricts execution to that layout; multi-layout coverage requires one script per layout.
- Custom-button-bound Client Scripts are created from the Buttons page only; they appear under the Button Event slot on every supported page.
- Mandatory Fields Form is a CRM-generated pop-up triggered by Layout Rules during inline edit on Detail (Canvas) / Detail (Standard); its events are exposed only on those page types.
- Multi-select field timing nuances (source-verbatim):
    · Create/Clone/Edit Page (Canvas) Page `onChange` on a Multi-select Picklist fires immediately after the user adds or modifies the selection.
    · Wizard `onChange` on a Multi-select Picklist fires immediately after add/modify; on a Multi-select Lookup it fires after the field's value is updated.
    · Field `onBeforeUpdate` (Create/Clone/Edit Canvas, Wizard) fires for Multi-select Lookup as soon as the "confirm" button is clicked and before the value is committed.

REQUIRED_PARAMETERS:
- Create / Clone / Edit Page events:
    · Page Event: `onLoad`, `onChange`, `onSave`.
    · Field Event: `onChange`, `onType`.
    · Subform Event: `onRowAdd`, `onCellChange`, `onRowDelete`, `BeforeRowDelete`.
    · Button Event (from Buttons page).
- Create / Clone / Edit Page Field Event — supported field types: Single Line, Multi-Line, Email, Phone, Pick List, Date, Number, Currency, Decimal, Percent, Long Integer, Checkbox, URL, Lookup, Owner Lookup, Multi-select Picklist.
- Create / Clone / Edit Page Field Event — unsupported fields: Salutation, Adjustment, Discount.
- Detail Page (Canvas) events:
    · Page Event: `onLoad`.
    · Field Event: `onBeforeUpdate`.
    · Mandatory Fields Form Event: `onBeforeMandatoryFormSave`, `onMandatoryFormLoad`.
    · Blueprint Event: `beforeTransition`.
    · Tag Event: `onTagChanged`.
    · Canvas Button Event: `onClick`.
    · Icon Event: `onClick`.
    · Text Event: `onClick`.
    · Subform Event: `onRowAdd`, `onCellChange`, `onRowDelete`, `BeforeRowDelete`, `BeforeRowUpdate`.
    · Notes Related List: `onBeforeAdd`, `onBeforeUpdate`.
    · Button Event.
- Detail Page (Canvas) Field Event — unsupported fields: Reporting To, Currency, Probability, Pricing Model, Wizard, Territory Updated Time.
- Detail Page (Standard) events — same event families as Detail Page (Canvas) (Page `onLoad`, Field `onBeforeUpdate`, Mandatory Form, Blueprint `beforeTransition`, Tag `onTagChanged`, Subform inc. `BeforeRowUpdate`, Notes Related List, Button Event); supported / unsupported field-type lists identical to Detail Page (Canvas).
- Create / Clone / Edit Page (Canvas) events:
    · Page Event: `onLoad`, `onChange`, `onSave`.
    · Field Event: `onChange`, `onType`, `onBeforeUpdate` (multi-select lookup).
    · Mandatory Fields Form Event: `onMandatoryFormLoad`.
    · Canvas Button Event: `onClick`.
    · Icon Event: `onClick`.
    · Text Event: `onClick`.
    · Subform Event: `onRowAdd`, `onCellChange`, `RowDelete`, `BeforeRowDelete`.
    · Button Event.
- Create / Edit Page (Wizard) events:
    · Wizard Event: `onLoad`, `onChange`, `onBeforeSave`, `onTransition`, `onBeforeTransition`.
    · Field Event: `onChange`, `onType`, `onBeforeUpdate` (multi-select lookup).
    · Subform Event: `onRowAdd`, `onCellChange`, `onRowDelete`, `BeforeRowDelete`.
    · Button Event.
- List Page (Standard) events: Page Event `onCustomViewLoad`, `onBeforeCustomViewChange`; Button Event.
- List Page (Canvas) events: Page Event `onLoad`, `onBeforeCustomViewChange`; Canvas Button Event `onClick`; Icon Event `onClick`; Text Event `onClick`; Button Event (per `eventdict-list-canvas.dou.md`, no `context` arg on this surface).
- Quick Create popup events: Page Event `onLoad`, `onChange`, `onSave`; Field Event `onChange`, `onType`.
- `return false` cancel semantics — append `return false` at the end of these handlers to cancel the corresponding native action: `onSave` (block record save), `BeforeRowDelete` (block subform row delete), `BeforeRowUpdate` (block subform row update), `beforeTransition` (block Blueprint transition), `onBeforeSave` (block Wizard save), `onBeforeTransition` (block Wizard transition), `onBeforeUpdate` (block Detail-page inline field save), `onBeforeMandatoryFormSave` (block Mandatory Fields Form save).
- A single Client Script with Page `onChange` can replace many Field `onChange` scripts on the same page when multiple fields need handling.

UI_ONLY_ACTIONS:
- Pick the Page Type during creation: `Setup → Developer Hub → Client Script → +New Script → Page` (no API to bulk-bind events). Note: No API equivalent — UI-only.
- Bind a Button Event handler: create the Client Script from the module's Buttons page (the standalone Client Script setup page rejects button-event creation). Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- `return false` omitted from an `onSave` / `onBeforeSave` / `BeforeRowDelete` / `BeforeRowUpdate` / `beforeTransition` / `onBeforeTransition` / `onBeforeUpdate` / `onBeforeMandatoryFormSave` handler → native action proceeds even after validation logic reports an error. (cancel-semantics)
- Field Event configured on an unsupported field type for the page (e.g. Salutation / Adjustment / Discount on Create / Clone / Edit; Reporting To / Currency / Probability / Pricing Model / Wizard / Territory Updated Time on Detail pages) → handler never fires; no error surfaced.
- `onType` triggers on every keystroke — wiring ZDK Web (CRM) API calls into `onType` exhausts API credits.
- `onChange` vs `onType` confusion — `onChange` waits for focus loss; using `onChange` when keystroke-level reaction is required produces "delayed" UX that looks like no-fire.
- Blueprint `beforeTransition` and Wizard `onBeforeTransition` are the only documented hooks to block transitions; relying on `onSave` to gate transitions silently no-ops.
- Layout binding silent no-fire — a record on a non-bound layout will never trigger the script; verify Layouts on the script definition. (layout-binding)
- Tag Event `onTagChanged` fires on Add-Tags save only.
- Custom-button-bound Client Script attempted from the standalone Client Script setup page is rejected — create only from the Buttons page.
