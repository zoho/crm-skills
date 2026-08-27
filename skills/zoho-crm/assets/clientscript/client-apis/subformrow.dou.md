FILE_PURPOSE: Read when reading or updating a single Subform row in place via the `SubformRow` object returned by `Subform.getRow(index)`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/SubformRow
TRIGGER_KEYWORDS: SubformRow, getValues, setValues, getCell, setReadOnly, row, index

TECHNICAL_CONSTRAINTS:
- Obtained via `ZDK.Page.getSubform(api_name).getRow(index)` where `index` is 0-based.
- **`setValues(values)` updates the single row** — `values` is an Object (not Array — contrast with Subform-level `setValues` which is Array).
- **`getValues()` returns a single Object** shaped `{ <field_api_name>: <value>, ... }` (source example shows the same shape that `Subform.getRow(1).getValues()` returns).
- **`getCell(value)` returns a `SubformCell`** — the example passes a String field API name (`'Name'`), though the source signature parameter is labelled `value`.
- **`setReadOnly(value)`** sets read-only on the entire row.

REQUIRED_PARAMETERS:
- `getValues() → Array` — source signature says `{Array}` but example output `{'Name': 'Zylker', 'Age': '20', ...}` is an Object.
- `setValues(values)` — `values` Object; keys are field API names.
- `getCell(value) → SubformCell` — see signature-vs-example flag above.
- `setReadOnly(value)` — `value` Boolean.

UI_ONLY_ACTIONS:
- *(none in source)* — `SubformRow` is a read/write handle, not a UI configuration surface.

CRITICAL_FAILURE_MODES:
- **`setValues` shape differs from Subform-level `setValues`** — `SubformRow.setValues` takes an **Object**; `Subform.setValues` takes an **Array of objects**. Passing an array to row-level silently fails. (shape-shift-vs-parent)
- **`getCell` signature ambiguity** — see flag above; passing the wrong shape silently returns no cell. (signature-ambiguity)
- **`getValues` return-type ambiguity** — signature vs example mismatch; iteration code that assumes `Array` may silently fail. (return-type-ambiguity)
- **Row handle becomes stale after `Subform.deleteRow` / `Subform.clear`** — subsequent `getValues()` on a stale row may return undefined or wrong data.
- **`setReadOnly(true)` on a row affects all cells in the row** — per-cell override requires `SubformCell.setReadOnly`. (granularity)
- **No `delete()` on SubformRow** — row deletion goes through parent `Subform.deleteRow(index)`. (granularity)

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getValues` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setValues` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `getCell` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setReadOnly` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
