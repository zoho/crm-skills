FILE_PURPOSE: Read when configuring a Subform field definition (cross-row attributes) via the `SubformField` object returned by `Subform.getField(api_name)` — covers criteria, mandatory, read-only, info, visibility.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/SubformField
TRIGGER_KEYWORDS: SubformField, setCriteria, setReadOnly, setMandatory, addInfo, setVisibility, lookup, picklist, dynamic

TECHNICAL_CONSTRAINTS:
- Obtained via `ZDK.Page.getSubform(api_name).getField(api_name)`. The handle represents the **field definition** across all subform rows — not a single cell.
- **Detail / Canvas-detail surfaces support `setCriteria` only on lookup fields** (source explicit).
- **Lookup `setCriteria` operators**: `starts_with`, `equals`. `id` field also supports `in`. Max 5 criteria per call.
- **Picklist `setCriteria` operators**: `starts_with`, `equals`, `ends_with`, `contains`, `not_equals`, `in`. Max 5 criteria per call.
- **Date `setCriteria`**: only `between`, single criterion: `(value:between:YYYY-MM-DD,YYYY-MM-DD)`.
- **Dynamic criteria binding**: `setCriteria` accepts handlebars-style template tokens `{{<Subform>.<Field>}}` to reference other subform-cell values. Example: `setCriteria("((Last_Name:equals:{{CFSubform.Single_Line_1}}))", { filterOnSearch:true })`.
- **`config.filterOnSearch`** Boolean — per source example on lookup criteria.
- **No `setValue` / `getValue` / `mask` / `addStyle` / `addTooltip` on SubformField** — those are cell-level (`SubformCell`) or row-level (`SubformRow`) operations.

REQUIRED_PARAMETERS:
- `getApiName() → String` — no args; returns the subform-field API name.
- `setCriteria(criteria, config?)` — `criteria` String in `((Field:operator:Value))` syntax; `config` Object (e.g. `{ filterOnSearch: true }`).
- `setReadOnly(value)` — `value` Boolean. Applies cross-row to all cells of this field.
- `setMandatory(value)` — `value` Boolean.
- `addInfo(message)` — `message` String; renders info icon on field header.
- `setVisibility(value)` — `value` Boolean. `false` hides the column.

UI_ONLY_ACTIONS:
- Subform field API name lookup: `Setup → Customization → Modules and Fields → <Module> → <Subform> → <Field> → Edit → API Name`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **`setCriteria` on Detail / Canvas-detail supports only lookup** — calling on picklist / date silently no-ops on Detail surfaces. (detail-setcriteria-lookup-only)
- **Dynamic-criteria token `{{<Subform>.<Field>}}` is evaluated per-row at filter time** — the `<Subform>` segment must match the subform's API name and `<Field>` must be a sibling cell API name. Typos silently produce empty filter results. (dynamic-criteria-binding)
- **Lookup operator set is small** (`starts_with`, `equals`, `in` for id) — `contains` / `ends_with` silently rejected on lookup.
- **`setReadOnly` / `setMandatory` / `setVisibility` apply cross-row** — to toggle per-row, use `SubformRow.setReadOnly` (row scope) or `SubformCell.setReadOnly` (single cell). (granularity)
- **`api_name` is field API name**, not display label. (label-vs-api-name)
- **No `setValue` on SubformField** — bulk row writes go through `Subform.setValues` / `insertRows`; per-cell writes via `SubformCell.setValue`. (no-bulk-field-write)
- **No `addStyle` / `mask` / `addTooltip`** on SubformField (contrast with Field) — styling at the subform-field level is not exposed. (decoration-gap)
- **`addInfo` icon placement is on the field header, not per cell** — per-cell info messages require `SubformCell.showError` or external Widget rendering. (info-placement)

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getApiName` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setCriteria` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setReadOnly` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setMandatory` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `addInfo` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setVisibility` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
