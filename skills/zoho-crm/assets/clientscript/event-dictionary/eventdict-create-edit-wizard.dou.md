FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on Wizard Create / Edit Page — canonical wire signature for transition-based multi-screen flows.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_create_edit_wizard
TRIGGER_KEYWORDS: onLoad, onChange, onTransition, onBeforeTransition, onBeforeSave, onType, beforeRowDelete, source_screen, target_screen

TECHNICAL_CONSTRAINTS:
- Page-type scope — Wizard Create Page and Edit Page (one event-dictionary covers both). The hook family is "Wizard Event", not "Page Event".
- Interceptor events: Wizard `onBeforeTransition`, `onBeforeSave`, Subform `beforeRowDelete`.
- Wizard transitions move the user between screens within the configured wizard; transition events do not fire for in-screen field edits.
- Custom Button binding configured only from the Buttons page.

REQUIRED_PARAMETERS:
- **Wizard events** (Type: Wizard Event):
    · `onLoad()` — fires when the Client-Script-configured wizard loads. No args.
    · `onChange(field_name)` — `field_name` = API name of the modified field. Supported field types: Single Line, Multi-Line, Email, Phone, Pick List, Date, Number, Currency, Decimal, Percent, Long Integer, Checkbox, URL, Lookup, Owner Lookup, Multi-select Picklist.
    · `onTransition(screen)` — fires after a screen transition completes. `screen` = `{ Name, API Name }` of the target screen.
    · `onBeforeTransition(source_screen, target_screen)` — **Interceptor**. Fires before a transition. Args: `source_screen` = `{ Name, API }`; `target_screen` = `{ Name, API }`. `return false` cancels.
    · `onBeforeSave()` — **Interceptor**. Fires on Save click. `return false` cancels save.
- **Field events** (Type: Field Event):
    · `onChange(value)` — `value` = current value. Fires on blur. Supported field types: same as Wizard-onChange list above (incl. Multi-select Picklist).
    · `onType(value)` — `value` = current value. Fires per keystroke.
- **Subform events** (Type: Subform Event):
    · `onRowAdd(row_data, index)`, `onCellChange(field_name, value, index)`, `onRowDelete(row_data, index)` — non-interceptor.
    · `beforeRowDelete(row_data, index)` — fires after delete-icon click, before row removal; add `return false` to cancel. **Note**: source description matches Interceptor semantics but does NOT carry the explicit `Interceptor` label here (legacy doc behaviour preserved).
- **Button event** (Type: Button Event): `onClick(context)` — `context` returns `{ Module API Name, ID }`.

UI_ONLY_ACTIONS:
- Wizard authoring (screens, transitions, layouts per screen): `Setup → Customization → Wizards → +New Wizard → screens → transitions → assign profiles`. Note: No API equivalent — UI-only.
- Bind a Client Script to a specific wizard: `Setup → Developer Hub → Client Script → +New → Page = Create Page (Wizard) | Edit Page (Wizard) → Wizard = <wizard_name>`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **SOURCE_CONFLICT — Field `onBeforeUpdate`**: legacy `client-script-events.html` documents `onBeforeUpdate` (Field) for Wizard, but this event-dictionary lists only `onChange` and `onType` under Field. Treat event-dictionary as authoritative; the legacy `onBeforeUpdate` hook may not fire on Wizard. (event-absent-in-wire-signature)
- **No Subform `beforeRowUpdate` on Wizard** — only `beforeRowDelete`; row-edit interception unavailable.
- **No Mandatory Form / Blueprint / Tag / Notes events on Wizard** — those surfaces fire only on Detail pages.
- **No Canvas-element events** — Wizard uses standard layouts, not Canvas; Canvas Button / Icon / Text events do not apply.
- **`onBeforeTransition` and `onBeforeSave` cancel only synchronously** — async `return false` after a Promise does not halt the gesture. (async-cancel)
- **`source_screen` / `target_screen` are screen objects, not field maps** — they identify which screens, not which field values changed. Use `getForm().getValues()` separately to read field state.
- **`onTransition` fires after the move** — to block, hook `onBeforeTransition`; trying to revert state from `onTransition` produces user-visible flicker. (listener-order)
- **Per-layout / per-wizard binding** — script bound to one wizard does not fire on other wizards of the same module. (layout-binding)
- **`field_name` arg is API name, not display label** — `case "Last_Name"` works, `case "Last Name"` does not. (label-vs-api-name)
- **Wizard is supported on mobile** (`../clientscript-mobile.dou.md`) — same event coverage modulo Field types and 10 s timeout.
