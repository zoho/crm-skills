FILE_PURPOSE: Read when modelling a field-validation / auto-population Client Script using onChange events — Date_of_Birth → Age → Category cascade, uppercase enforcement, and the page-event-vs-field-event consolidation pattern.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/client-script-insurance.html
TRIGGER_KEYWORDS: ZDK.Page.getField, age_field.showError, setValue, Date_of_Birth, Policyholder, onChange field, onChange page, field_name

TECHNICAL_CONSTRAINTS:
- Sample module — `Policyholder` (custom module); custom fields used in samples: `Date_of_Birth`, `Age`, `Category`, `Name` (first name), `Last_Name`.
- All three sample scripts attach to the Create page of the `Policyholder` module via field events on `Date_of_Birth`, `Name`, and `Last_Name`.
- The consolidated single-script version uses Page `onChange` with `switch (field_name)` to handle all three field updates inside one script.
- Page `onChange` runs on every field change on the page; Field `onChange` runs only when the specific field is updated.

REQUIRED_PARAMETERS:
- Per-script binding: Module = `Policyholder`, Page = Create page, Event Family = Field `onChange` (Date_of_Birth | Name | Last_Name) OR Page `onChange` (consolidated).
- ZDK call surface used in samples:
    · `ZDK.Page.getField("<API_Name>")` — handle for `Age`, `Category`, `Name`, `Last_Name`, `Date_of_Birth`.
    · `<field>.getValue()` — read current field value.
    · `<field>.setValue(<v>)` — write field value (used for `Age`, `Category`, uppercased `Name` / `Last_Name`).
    · `<field>.showError("<message>")` — surface a validation error inline against the field.
- Injected `value` argument carries the new field value inside Field `onChange`; the consolidated Page `onChange` reads `field_name` to branch.
- Sample logic — compute age from `value` (DOB string) with month / day adjustment, then `age > 80` ⇒ `showError`; `60 < age ≤ 80` ⇒ Category `Senior Citizen`; otherwise Category `Citizen`.
- Uppercasing — `first_name.setValue(value.toUpperCase())` inside Field `onChange` on `Name`; same pattern on `Last_Name`.

UI_ONLY_ACTIONS:
- Create the three scripts: `Setup → Developer Hub → Client Script → +New Script → Module = Policyholder → Page = Create Page → Layout → Event Type = Field → Field = Date_of_Birth | Name | Last_Name → Field Event = onChange → Next → IDE → Save and Close → Enable`. Note: No API equivalent — UI-only.
- Alternative consolidated flow: configure one script with Event Type = Page, Page Event = onChange; branch on `field_name` inside the IDE. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- Quoting a display label in `ZDK.Page.getField("…")` (e.g. `"Date of Birth"` instead of `Date_of_Birth`) silently returns no field; always use API names. (label-vs-api-name)
- The sample uses `Name` as the first-name API name — module-specific renames must update the script accordingly; copy-pasting the sample to a module whose first-name field is `First_Name` silently no-ops.
- Page `onChange` re-runs on every field change — placing heavy logic (age recomputation) inside an unconditional branch wastes execution time; gate inside a `field_name === '<API>'` check.
- `value` argument inside Field `onChange` is the raw new value — for `Date_of_Birth` it is a date string, not a Date object; constructing `new Date(value)` is required before arithmetic.
- `showError` raises an inline error but does NOT block the user from clicking Save — to block save, add an `onSave` Page Event with `return false` (see [clientscript-events.dou.md](./clientscript-events.dou.md)).
- Layout binding — these scripts run only for the layout selected at creation; multi-layout `Policyholder` deployments need one script copy per layout. (layout-binding)
