FILE_PURPOSE: Read when reading or writing a single cell inside a Subform row via the `SubformCell` object returned by `SubformRow.getCell(field)`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/SubformCell
TRIGGER_KEYWORDS: SubformCell, getValue, setValue, setReadOnly, showError, cell, value

TECHNICAL_CONSTRAINTS:
- Obtained via `ZDK.Page.getSubform(api_name).getRow(index).getCell(field)`.
- **`setValue(value)`** accepts `String | Number | Boolean | Object`. The Object shape mirrors Field.setValue semantics (e.g. Lookup → `{id, name}`).
- **`showError(message)`** renders inline error on the cell input (e.g. "List Price cannot be zero").
- **`setReadOnly(value)`** sets read-only at the cell level — finer-grained than `SubformRow.setReadOnly`.

REQUIRED_PARAMETERS:
- `getValue() → String | Object` — source-listed return types; shape depends on cell's field type.
- `setValue(value)` — `value` ∈ String | Number | Boolean | Object.
- `setReadOnly(value)` — `value` Boolean.
- `showError(message)` — `message` String.

UI_ONLY_ACTIONS:
- *(none in source)* — `SubformCell` is a leaf data handle, not a UI configuration surface.

CRITICAL_FAILURE_MODES:
- **`setValue` shape must match cell's field type** — passing a String to a Lookup cell silently fails; pass `{id, name}`. (cell-value-shape)
- **`setValue` on read-only cell silently no-ops** — call `setReadOnly(false)` first if mutation needed. (readonly-mutation)
- **`showError` may share Field's Detail-surface restrictions** (Ajax-edit / Mandatory-form only) — source does not state the restriction explicitly for SubformCell.
- **No `getApiName()` on SubformCell** — cell handles do not expose which field they're on (caller must remember). To inspect, fetch the SubformField via `Subform.getField(api_name)`. (no-introspection)
- **Cell handle goes stale after row delete / subform clear / setValues replace** — refetch via `getRow(i).getCell(api)` after parent mutations.
- **No `mask` / `addStyle` / `addTooltip` on SubformCell** — those decorations are Field-level only; SubformCell only exposes `getValue` / `setValue` / `setReadOnly` / `showError`. (decoration-gap)

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getValue` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setValue` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setReadOnly` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `showError` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
