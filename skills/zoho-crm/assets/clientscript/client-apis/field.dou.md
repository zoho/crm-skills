FILE_PURPOSE: Read when reading / writing a record's top-level Field via the `Field` object returned by `ZDK.Page.getField(api_name)` — covers value I/O, validation, styling, and lookup/picklist criteria.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Field
TRIGGER_KEYWORDS: Field, getValue, setValue, setCriteria, getPicklistOptions, mask, showError, setMandatory, setReadOnly, addStyle

TECHNICAL_CONSTRAINTS:
- Obtained via `ZDK.Page.getField(api_name)`. The arg is the field API name (not display label).
- **Detail-page write restrictions**: `setValue` works on Detail (Canvas/Standard) **only inside Mandatory Form**. Direct field writes elsewhere on Detail are silently dropped.
- **`showError` on Canvas Detail** is supported **only in Ajax edit and Mandatory form** (source explicit).
- **`setCriteria` on Detail page** supports **only lookup fields** (source explicit) — picklist / date-range criteria are Create / Edit / Clone-page features.
- **Lookup `setCriteria` operators**: `starts_with`, `equals`. The `id` field also supports `in`. Max 5 criteria per setCriteria call.
- **Picklist `setCriteria` operators**: `starts_with`, `equals`, `ends_with`, `contains`, `not_equals`, `in`. Max 5 criteria per call.
- **Date `setCriteria`**: only the `between` operator, single criterion: `(value:between:YYYY-MM-DD,YYYY-MM-DD)`.
- **`mask({character, length, reverse})`** — `character` is the mask char (e.g. `'*'`, `'#'`), `length` is mask-prefix count, `reverse=true` masks suffix instead of prefix.
- **`getValue` / `setValue` shape varies by field type**:
    · Scalar fields → String / Number / Boolean.
    · Checkbox → `true | false`.
    · Lookup → `{ id, name }`.
    · Subform → array of objects, each `{ <subform_field_api_name>: <value>, ... }`.
- **`addStyle` config**: `backgroundColor`, `foregroundColor`, `borderColor` accept hex strings (`'#FF0000'`); `fontWeight` accepts `'bold'`, numeric strings (`'100'`), or `'inherit'`.

REQUIRED_PARAMETERS:
- `getApiName() → String` — no args; returns the field API name.
- `mask({character, length, reverse})` — example: `mask({character:'*', length:4, reverse:false})` → `****rt@zohomail.com`.
- `showError(message)` — `message` String; renders inline error on the field input.
- `setValue(value)` — `value` ∈ String | Number | Boolean | Object (Object for Lookup `{id, name}` or Subform array).
- `getValue() → String | Number | Boolean | Object` — returns current value in field-type-appropriate shape.
- `setMandatory(value)` — `value` Boolean.
- `setMaxLength(value)` — `value` Number.
- `setReadOnly(value)` — `value` Boolean.
- `setVisibility(value)` — `value` Boolean. `true` shows, `false` hides.
- `addStyle(style_config)` — see config shape above.
- `addInfo(message)` — `message` String; adds an info icon with message.
- `addTooltip(message)` — `message` String; adds a tooltip.
- `setCriteria(criteria, config?)` — `criteria` is the criteria string in `((Field:operator:Value))` syntax; `config.filterOnSearch` Boolean (per source example).
- `getPicklistOptions() → array` — returns `[{ display_value, actual_value, id?, filtered? }, ...]`. Output includes a `-None-` entry first; subsequent entries carry `id` and `filtered` booleans.

UI_ONLY_ACTIONS:
- Field API name lookup: `Setup → Customization → Modules and Fields → <Module> → <Field> → Edit → API Name`. Note: No API-only equivalent for renaming — UI-only.

CRITICAL_FAILURE_MODES:
- **`setValue` on Detail surfaces is silent no-op outside Mandatory Form** — Canvas / Standard Detail field writes drop unless in Mandatory Form. Use Mandatory Form fields, or Web API Update Record + `$Client.refresh()`. (detail-setvalue-restricted)
- **`showError` on Canvas Detail is restricted to Ajax-edit + Mandatory-form contexts** — calling outside these contexts silently no-ops. (canvas-detail-showerror-restricted)
- **`setCriteria` on Detail supports only lookup fields** — calling on picklist / date on Detail silently no-ops. (detail-setcriteria-lookup-only)
- **Lookup `setCriteria` operator set is tiny** (`starts_with`, `equals`; `in` only on `id`) — using `contains` / `ends_with` against a lookup field silently rejects.
- **Picklist `setCriteria` syntax** uses `actual_value` as the key (or `id` for in-operator); using `display_value` silently fails to match.
- **`setValue` before `showError` on the same field** — `setValue` triggers a field re-render that wipes any error state applied by `showError`. Always call `setValue` first (to set or clear the value), then call `showError` on the already-rendered field. Reversing the order causes `showError` to render and then be immediately wiped. (setvalue-showerror-order)
- **`setValue` for Lookup requires `{id, name}` shape** — passing just the name string silently fails to bind the relation. (lookup-shape)
- **`setValue` for Subform replaces all rows** — pass the full row array; partial updates require `getValue() → mutate → setValue`.
- **`api_name` is the field API name, not display label** — `getField('Last_Name')` works, `'Last Name'` does not. (label-vs-api-name)
- **`mask` is display-only** — does not change `getValue()` output; do not use as a security control.
- **`getPicklistOptions` returns the `-None-` placeholder** as the first entry — iteration code must skip it. (none-placeholder)
- **`addStyle` colour values must be hex strings** — named colours / rgb() syntax not documented.
- **`setMaxLength` does not validate existing value** — if current value > new max, no auto-truncation documented.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getApiName` | all page types | all page types | all page types |
| `mask` | Detail | Detail | — |
| `showError` | Create/Edit/Clone | Detail, Create/Edit/Clone | Create/Edit |
| `setValue` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `getValue` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setMandatory` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `setMaxLength` | Create/Edit/Clone, Detail | Detail, Create/Edit/Clone | Create/Edit |
| `setReadOnly` | Create/Edit/Clone, Detail | Detail, Create/Edit/Clone | Create/Edit |
| `setVisibility` | Detail, Create/Edit/Clone | Create/Edit/Clone, Detail | Create/Edit |
| `addStyle` | Detail | Detail | — |
| `addInfo` | Detail, Create/Edit/Clone | Create/Edit/Clone, Detail | Create/Edit |
| `addTooltip` | Detail, Create/Edit/Clone | Create/Edit/Clone, Detail | Create/Edit |
| `setCriteria` | Detail, Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `getPicklistOptions` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
