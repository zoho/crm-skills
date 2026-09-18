FILE_PURPOSE: Read first when determining which "Type" dropdown value and Event to select for a given Page — single-table fast lookup, cross-checked against the official event catalog and every per-page event-dictionary file.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/client-script-events.html, https://www.zoho.com/crm/developer/docs/client-script/creation.html
TRIGGER_KEYWORDS: Type dropdown, Event Details, Page Event, Field Event, Blueprint Event, Button Event, Subform Event, Mandatory Fields Form Event, Tag Event, Notes Related List, Canvas Button Event, Icon Event, Text Event, Wizard Event

TECHNICAL_CONSTRAINTS:
- This file is the authoritative fast-scan lookup for "which Type value + which Events" per Page. For full argument signatures, interceptor semantics, and failure modes, defer to the matching `eventdict-*.dou.md` (derivable 1:1 from the Page name, e.g. Detail (Standard) → `eventdict-detail-standard.dou.md`).
- Type values here are exactly what appears in the CRM Create Script "Type" dropdown (Event Details section). Type options are gated by the Page selected first (Page Details section).
- **Type does not apply to Category = Commands** — Commands scripts have no Page/Type/Event fields at all; they trigger via Command Palette or a per-user keyboard shortcut (see [clientscript-commands.dou.md](./clientscript-commands.dou.md)).
- **Wizard Create/Edit pages** additionally require choosing which Wizard in the **Page Details** section (`Page = Create/Edit Page (Wizard) → Wizard = <name>`), before Type/Event are even shown — analogous to Layout, this applies uniformly regardless of which Type is later chosen on that page. It is **not** an Event-Details/after-Type selector.
- `Field` is the only genuine **post-Type, Event-Details** selector (confirmed via `creation.html`'s literal "In the Event Details section, select the Type... For a field event, select the Field..." ordering).
- `Subform Event` has **no creation-time subform picker** — the target subform is chosen in code via `ZDK.Page.getSubform(<subform_api_name>)`, not via a UI field.
- Canvas Button Event, Icon Event, and Text Event are **3 distinct Types** (each with its own `onClick`), not one combined "Canvas Button/Icon/Text" type.
- List-page custom-view events (`onCustomViewLoad` / `onBeforeCustomViewChange`) are still **Page Event** — not a separate "Custom View Event" type.

REQUIRED_PARAMETERS:
- Full Page × Type × Events matrix (44 rows, 8 Page surfaces):

| Page | Type | Events | Configured via | Extra selector after Type |
|---|---|---|---|---|
| Create/Clone/Edit (Standard) | Page Event | onLoad, onChange, onSave | Type dropdown | None |
| Create/Clone/Edit (Standard) | Field Event | onChange, onType | Type dropdown | Field |
| Create/Clone/Edit (Standard) | Subform Event | onRowAdd, onCellChange, onRowDelete, beforeRowDelete | Type dropdown | None (targeted via `getSubform()` in code) |
| Create/Clone/Edit (Standard) | Button Event | onClick | Buttons page | None |
| Detail (Standard) | Page Event | onLoad | Type dropdown | None |
| Detail (Standard) | Field Event | onBeforeUpdate | Type dropdown | Field |
| Detail (Standard) | Blueprint Event | beforeTransition | Type dropdown | None |
| Detail (Standard) | Mandatory Fields Form Event | onBeforeMandatoryFormSave, onMandatoryFormLoad | Type dropdown | None |
| Detail (Standard) | Tag Event | onTagChanged | Type dropdown | None |
| Detail (Standard) | Subform Event | onRowAdd, onCellChange, onRowDelete, beforeRowDelete, beforeRowUpdate | Type dropdown | None (targeted via `getSubform()` in code) |
| Detail (Standard) | Notes Related List | onBeforeAdd, onBeforeUpdate | Type dropdown | None |
| Detail (Standard) | Button Event | onClick | Buttons page | None |
| Detail (Canvas) | Page Event | onLoad | Type dropdown | None |
| Detail (Canvas) | Field Event | onBeforeUpdate | Type dropdown | Field |
| Detail (Canvas) | Mandatory Fields Form Event | onBeforeMandatoryFormSave, onMandatoryFormLoad | Type dropdown | None |
| Detail (Canvas) | Blueprint Event | beforeTransition | Type dropdown | None |
| Detail (Canvas) | Tag Event | onTagChanged | Type dropdown | None |
| Detail (Canvas) | Canvas Button Event | onClick | Canvas element designer | None |
| Detail (Canvas) | Icon Event | onClick | Canvas element designer | None |
| Detail (Canvas) | Text Event | onClick | Canvas element designer | None |
| Detail (Canvas) | Subform Event | onRowAdd, onCellChange, onRowDelete, beforeRowDelete, beforeRowUpdate | Type dropdown | None (targeted via `getSubform()` in code) |
| Detail (Canvas) | Notes Related List | onBeforeAdd, onBeforeUpdate | Type dropdown | None |
| Detail (Canvas) | Button Event | onClick | Buttons page | None |
| Create/Clone/Edit (Canvas) | Page Event | onLoad, onChange, onSave | Type dropdown | None |
| Create/Clone/Edit (Canvas) | Field Event | onChange, onType | Type dropdown | Field |
| Create/Clone/Edit (Canvas) | Mandatory Fields Form Event | onMandatoryFormLoad | Type dropdown | None |
| Create/Clone/Edit (Canvas) | Canvas Button Event | onClick | Canvas element designer | None |
| Create/Clone/Edit (Canvas) | Icon Event | onClick | Canvas element designer | None |
| Create/Clone/Edit (Canvas) | Text Event | onClick | Canvas element designer | None |
| Create/Clone/Edit (Canvas) | Subform Event | onRowAdd, onCellChange, onRowDelete, beforeRowDelete | Type dropdown | None (targeted via `getSubform()` in code) |
| Create/Clone/Edit (Canvas) | Button Event | onClick | Buttons page | None |
| Wizard Create/Edit | Wizard Event | onLoad, onChange, onBeforeSave, onTransition, onBeforeTransition | Type dropdown | None (Wizard itself is chosen in Page Details, before Type) |
| Wizard Create/Edit | Field Event | onChange, onType | Type dropdown | Field |
| Wizard Create/Edit | Subform Event | onRowAdd, onCellChange, onRowDelete, beforeRowDelete | Type dropdown | None (targeted via `getSubform()` in code) |
| Wizard Create/Edit | Button Event | onClick | Buttons page | None |
| List (Standard) | Page Event | onCustomViewLoad, onBeforeCustomViewChange | Type dropdown | None |
| List (Standard) | Button Event | onClick | Buttons page | None |
| List (Canvas) | Page Event | onLoad, onBeforeCustomViewChange | Type dropdown | None |
| List (Canvas) | Canvas Button Event | onClick | Canvas element designer | None |
| List (Canvas) | Icon Event | onClick | Canvas element designer | None |
| List (Canvas) | Text Event | onClick | Canvas element designer | None |
| List (Canvas) | Button Event | onClick | Buttons page | None |
| Quick Create popup | Page Event | onLoad, onChange, onSave | Type dropdown | None |
| Quick Create popup | Field Event | onChange, onType | Type dropdown | Field |

- `Configured via` distinguishes how the row's Type is actually reached: `Type dropdown` (standard `Setup → Developer Hub → Client Script → +New Script` dialog), `Buttons page` (custom Button Event scripts can only be created from the module's Buttons page), or `Canvas element designer` (Canvas Button/Icon/Text Event scripts can only be created from `Setup → Customization → Canvas → <element> → Actions → Client Script`).
- `Extra selector after Type` names the one further field shown after choosing Type, inside Event Details — only `Field` qualifies; everything else is `None` (Subform is a code-level target, and Wizard is chosen earlier, in Page Details).

UI_ONLY_ACTIONS:
- All Type-dropdown-configured rows: `Setup → Developer Hub → Client Script → +New Script → Category = Module → Page → Module → Layout (+ Wizard, if Page = Wizard) → Event Details: Type → Event (+ Field, if Type = Field Event) → Next → IDE → Save and Close`. Note: No API equivalent — UI-only.
- Button Event rows: create only from `Setup → Customization → Modules and Fields → <Module> → Links and Buttons → Buttons → Create/select button → action = Client Script`. Note: No API equivalent — UI-only.
- Canvas Button/Icon/Text Event rows: create only from `Setup → Customization → Canvas → <canvas> → select element (Button/Icon/Text) → Actions → Client Script`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- Canvas Button Event, Icon Event, and Text Event are 3 distinct Types (not 1 combined "Canvas Button/Icon/Text" type) — treating them as one risks binding the script to the wrong canvas element category.
- List-page custom-view events are still Type = **Page Event** — describing them as a separate "Custom View Event" type will send a user looking for a Type value that doesn't exist in the dropdown.
- Button Event and Canvas Button/Icon/Text Event are **not reachable from the standard Type dropdown at all** — a response that says "Type: Button Event" without naming the Buttons-page (or Canvas-designer) entry point recreates the exact confusion this file exists to prevent.
- Category = Commands has no Type/Event concept — do not state a Type for Commands-category scripts.
- SOURCE_CONFLICT — `clientscript-faqs.dou.md` FAQ #10/#31's supported-pages list omits **List Page (Canvas)** entirely. This matrix treats List Page (Canvas) as valid, per `clientscript-events.dou.md` section 8 and `eventdict-list-canvas.dou.md`. Do not edit the FAQ file to "fix" this — it's flagged here only.
- `List (Canvas) | Button Event` is confirmed only via `eventdict-list-canvas.dou.md` (the official events doc's page for this section does not explicitly enumerate it) — event-dictionary files are authoritative per this skill's convention.
- Wizard `Field Event` and Create/Clone/Edit (Canvas) `Field Event` exclude `onBeforeUpdate` (multi-select lookup) — that hook appears only in the legacy source prose, not in the corresponding event-dictionary file; treat the event-dictionary as authoritative (SOURCE_CONFLICT, see those files' own CRITICAL_FAILURE_MODES).
