FILE_PURPOSE: Read when picking event names and argument signatures for a Client Script on Quick Create Popup — canonical wire signature for the lean inline-create surface.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/event-dictionary/module_quick_create
TRIGGER_KEYWORDS: onLoad, onChange, onSave, onType, quick_create, popup, Interceptor

TECHNICAL_CONSTRAINTS:
- Page-type scope — Quick Create Popup (the inline create dialog launched from list pages, related lists, lookup fields, etc.).
- Only Page and Field event families exist — **no** Subform, Button, Blueprint, Mandatory Form, Tag, or Notes events on Quick Create.
- Interceptor event — Page `onSave`. `return false` blocks the record-save.

REQUIRED_PARAMETERS:
- **Page events** (Type: Page Event):
    · `onLoad()` — fires when the Quick Create popup loads. No args.
    · `onChange(field_name)` — `field_name` = API name of the field that was changed.
    · `onSave()` — **Interceptor**. Fires after Save / Save and New click, before persistence. `return false` cancels save.
- **Field events** (Type: Field Event):
    · `onChange(value)` — `value` = current value in the field. Fires on blur / focus-out after edit.
    · `onType(value)` — `value` = current value. Fires per keystroke.
- Source does **not** enumerate Quick-Create-specific supported field types — assume the parent module's field set unless verified otherwise.

UI_ONLY_ACTIONS:
- Configure Quick Create layout (which fields appear in the popup): `Setup → Customization → Modules and Fields → <Module> → Layouts → <layout> → Quick Create View`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **SOURCE_CONFLICT — FAQ #11 says Quick Create is unsupported** (`../clientscript-faqs.dou.md`), but this event-dictionary page exists and enumerates 5 events. Treat the event-dictionary as authoritative; FAQ entry is stale.
- **No Subform events** — Quick Create cannot intercept row add / delete / cell change even when the underlying layout includes subforms. (subform-event-absent)
- **No Custom Button events** — Quick Create does not surface custom buttons; `onClick` listeners do not fire.
- **No Blueprint / Mandatory Form events** — Quick Create saves bypass blueprint-state hooks and mandatory-form pop-ups that fire on full Detail / Create pages. (cross-surface-gap)
- **`onSave` `return false` cancels save only synchronously** — async return values do not halt the save.
- **Field-type coverage not stated in source** — Multi-select Picklist / Lookup behaviour on Quick Create not verified; test before relying.
- **Per-layout binding** — Quick Create script bound to one layout does not fire on Quick Create of other layouts. (layout-binding)
- **Mobile silent absence** — Quick Create is not in the mobile-supported page list (`../clientscript-mobile.dou.md`); Quick Create scripts no-op on mobile.
