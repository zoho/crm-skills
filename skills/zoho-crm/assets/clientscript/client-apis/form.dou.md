FILE_PURPOSE: Read when bulk-reading or bulk-writing all fields (including subforms and lookups) on a Create / Edit / Quick-Create / Clone form via the Form object from `ZDK.Page.getForm()`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Form
TRIGGER_KEYWORDS: ZDK.Page.getForm, Form.setValues, Form.getValues, lookup id name, Subform_1, Email_Opt_Out, bulk field write

TECHNICAL_CONSTRAINTS:
- The Form object is obtained via `ZDK.Page.getForm()`. Source does not document constructor / multi-form accessors.
- `setValues(values)` accepts an Object keyed by **field API name** (verbatim: `'Custom_Field1'`, `'Account_Name'`, `'Email_Opt_Out'`, `'Subform_1'` in source example). Display labels (`"Last Name"` with a space) are not accepted. (label-vs-api-name)
- **Lookup fields take a `{ id, name }` Object** — source example: `'Account_Name': { id: "5164254000000366162", name: "John Doe" }`. Plain strings will not resolve the lookup.
- **Boolean fields take a literal `true` / `false`** — source example: `'Email_Opt_Out': true`.
- **Subform fields take an Array of row Objects keyed by subform-field API name** — source example: `'Subform_1': [{ 'Email_1': 'henry@zylker.com', 'Website1': 'www.henryzyker.com' }]`.
- `getValues() {Object}` returns the entire form payload as an Object keyed by field API name, with subform rows nested as Arrays of Objects. Source example output mixes top-level subform-row keys (`'Subform_1': [{...}]`) **and** flattened sibling keys (`"Email_1": "henry@zylker.com"`) at the top level.

REQUIRED_PARAMETERS:
- `ZDK.Page.getForm()` — no params; returns the current page's Form object.
- `setValues(values)` — `values: Object` keyed by field API name. Required structure per field type:
  - Text / Number / Boolean → primitive.
  - Lookup → `{ id: String, name: String }`.
  - Subform → `Array<Object>` (each row keyed by subform-field API name).
- `getValues() {Object}` — no params; returns the form's current values Object.

UI_ONLY_ACTIONS:
- Defining which fields render on a form (layout, section order, mandatory rules, validation rules) is a Setup → Customization → Modules and Fields → <Module> → Layouts / Validation Rules action. `setValues` writes only to fields that the active layout exposes. (layout-binding)

CRITICAL_FAILURE_MODES:
- **`setValues` keys must be field API names, not display labels** — `setValues({ "Last Name": "..." })` silently no-ops; correct form is `setValues({ Last_Name: "..." })`. (label-vs-api-name)
- **Lookup writes require `{ id, name }`** — `setValues({ Account_Name: "John Doe" })` does not resolve the account; required shape is `{ id: "<record_id>", name: "John Doe" }`. (label-vs-api-name)
- **Subform writes replace the visible row set with the provided Array** — partial-row patching (without including unchanged rows) drops the omitted rows.
- **Fields hidden by the active layout / profile silently no-op** — writing to a field that the current layout does not expose returns no error but does not persist on save. (layout-binding)
- **`getValues()` reflects only fields rendered on the form** — fields suppressed by the active layout are not in the output, so a downstream comparison against the full module schema falsely reports missing values. (layout-binding)
- **The output shape ambiguity (nested-vs-flat subform keys) above must be resolved before consumers iterate** — naive `Object.keys(form.getValues())` will see both `Subform_1` and `Email_1` and may double-process the subform-row data.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `setValues` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `getValues` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
