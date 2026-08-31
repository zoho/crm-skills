FILE_PURPOSE: Read when manipulating a Subform as a whole via the `Subform` object returned by `ZDK.Page.getSubform(api_name)` — covers row-level bulk I/O, row insert / delete / clear, and subform-level mandatory / info.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Subform
TRIGGER_KEYWORDS: Subform, setValues, getValues, insertRows, deleteRow, clear, getRow, getField, setMandatory

TECHNICAL_CONSTRAINTS:
- Obtained via `ZDK.Page.getSubform(api_name)`. Returns a `Subform` handle on the named subform.
- **`setValues(values)` replaces the entire subform contents** with the provided array of row objects. Each row is a `{ <field_api_name>: <value>, ... }` map.
- **`insertRows(values, index?)`** — `values` is an array of row objects. If `index` provided, rows are inserted at that index; if omitted, rows append.
- **`deleteRow(index)`** removes a single row at the given 0-based index.
- **`clear()`** removes all rows.
- **`getRow(index) → SubformRow`** — 0-based index; see [subformrow.dou.md](./subformrow.dou.md).
- **`getField(api_name) → SubformField`** — returns the SubformField definition (not a per-row cell); see [subformfield.dou.md](./subformfield.dou.md) for the field-level operations.
- **Row indexing is 0-based** (source examples show `getRow(0)` / `getRow(1)` for first / second).

REQUIRED_PARAMETERS:
- `getApiName() → String` — no args; returns subform API name.
- `getField(api_name) → SubformField` — `api_name` String.
- `setValues(values)` — `values` Array of objects. Each object's keys are field API names, values are the field values.
- `getValues() → Array` — returns `[{ <api_name>: <value>, ... }, ...]`.
- `getRow(index) → SubformRow` — `index` Number, 0-based.
- `insertRows(values, index?)` — `values` Array of row objects; `index` Number (optional, append if omitted).
- `deleteRow(index)` — `index` Number.
- `clear()` — no args.
- `setMandatory(value)` — `value` Boolean.
- `addInfo(message)` — `message` String.

UI_ONLY_ACTIONS:
- Subform layout & field definitions configured via `Setup → Customization → Modules and Fields → <Module> → <Subform> → Edit`. Note: No API equivalent for subform layout authoring — UI-only.

CRITICAL_FAILURE_MODES:
- **`setValues` is a full replace, not a merge** — to append, use `insertRows` (or `getValues` + concat + `setValues`). (subform-replace-semantics)
- **Row keys are field API names**, not display labels — `'Name_1'` works, `'Name'` (display) does not. (label-vs-api-name)
- **`getRow(index)` out-of-bounds returns silently** (no error documented) — guard with `getValues().length`.
- **`insertRows` with no `index` appends** — passing `null` or `undefined` for `index` may behave differently from omitting.
- **`deleteRow(index)` shifts subsequent indices** — iterating + deleting requires reverse iteration or index-recalculation.
- **Subform `setValues` cannot exceed the subform-row hard cap** — CRM enforces a per-subform row cap separately.
- **No bulk `updateRow(index, partial)`** — partial-row updates require `getRow(index).setValues({...})` (SubformRow API) or `getRow(index).getCell(api).setValue(val)` (SubformCell API).
- **No `getRows() → SubformRow[]`** documented at the Subform level — use `getValues()` for bulk read or loop `getRow(i)` for handles.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getApiName` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `getField` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `setValues` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `getValues` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `getRow` | Create/Edit/Clone, Detail | Create/Edit/Clone, Detail | Create/Edit |
| `insertRows` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `deleteRow` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `clear` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `setMandatory` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `addInfo` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
