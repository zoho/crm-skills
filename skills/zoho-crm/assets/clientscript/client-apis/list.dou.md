FILE_PURPOSE: Read when scripting the List View — freeze columns, mask a field, sort by field, read / select / clear selected records, or style records / fields conditionally via the List object from `ZDK.Page.getList()`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/List
TRIGGER_KEYWORDS: ZDK.Page.getList, List.freezeColumns, List.maskField, List.sortByField, List.getRecords, List.selectRecords, List.selectRecordsByID, List.clearSelection, List.style, list view

TECHNICAL_CONSTRAINTS:
- The List object is obtained via `ZDK.Page.getList()`. Source does not document multi-list accessors.
- `freezeColumns(option)` — `option: Boolean` — `true` freezes the view and disables column modification; `false` unfreezes.
- `maskField(field_name, config)` — masks a field's rendered value across all rows. Source config keys: `length: Number` (chars to mask), `character: Char` (mask character), `reverse: Boolean` (mask from the right). Source example: `maskField("Email", { length: 8, character: '#', reverse: true })`.
- `sortByField(field_name, option)` — `option: String` — one of the literal tokens `'asc' | 'desc' | 'unsort'`.
- `getRecords()` — returns the list's records. Each record carries a `$selected` property indicating whether the row is currently selected (source: "$selected property denoted if respective records is selected or not").
- `selectRecords(criteria)` — `criteria: String <optional>` — COQL-style criteria expression. Source example: `"((Last_Name:equals:Burns)and(First_Name:starts_with:M))"`. **Only fields rendered in the list are available for criteria** (source verbatim: "Fields that are in the list are only available for criteria").
- `selectRecordsByID(ids)` — `ids: Array<String>` — array of record id strings. Source example: `["111111000000000812", "111111000000000834", "111111000000000845"]`.
- `clearSelection()` — clears the current selection set.
- `style(style_config, criteria)` — applies conditional styling. `style_config.record` Object supports key `backgroundColor`. `style_config.field` Object keyed by field API name supports `backgroundColor`, `fontWeight`, `foregroundColor`. `criteria: String` — same COQL-style expression as `selectRecords`. To remove styling, pass empty Objects: `style({ record: {}, field: {} }, "<criteria>")`.

REQUIRED_PARAMETERS:
- `ZDK.Page.getList()` — no params.
- `freezeColumns(option)` — `option: Boolean`.
- `maskField(field_name, config)` — `field_name: String` (field API name); `config: Object` with `{ length: Number, character: Char, reverse: Boolean }`.
- `sortByField(field_name, option)` — `field_name: String` (field API name); `option: String` in `{'asc','desc','unsort'}`.
- `getRecords()` — no params.
- `selectRecords(criteria?)` — `criteria: String` (optional).
- `selectRecordsByID(ids)` — `ids: Array<String>`.
- `clearSelection()` — no params.
- `style(style_config, criteria)` — `style_config: Object` (with optional `.record` and `.field` sub-Objects); `criteria: String`.

UI_ONLY_ACTIONS:
- Defining which fields appear in the List View (column set) is a Setup → Customization → Modules and Fields → <Module> → Custom Views action. `selectRecords` / `style` criteria can only reference columns that the active Custom View includes (list-bound). (layout-binding)
- Defining Custom Views themselves (the saved filter that determines which records load) is also Setup-only.

CRITICAL_FAILURE_MODES:
- **`maskField` / `sortByField` / `selectRecords` field names must be API names** — passing display labels (`"Email Address"` instead of `"Email"`) silently no-ops. (label-vs-api-name)
- **`selectRecords` / `style` criteria can only reference fields rendered in the current Custom View** — referencing a field absent from the column set returns no records / styles nothing, with no error. (layout-binding)
- **`sortByField(field_name, 'asc'|'desc'|'unsort')` — any other token silently no-ops** — there is no documented error path for an unsupported sort option.
- **`style` with empty Objects (`{record:{}, field:{}}`) is the documented removal idiom** — omitting the criteria removes styling globally; including a stale criteria removes it only from matching rows.
- **`maskField` is a render-only mask** — the underlying record value remains unmasked; downstream `getRecords()` / `getValue()` calls return the real value. Do not rely on `maskField` for security / HIPAA redaction. (HIPAA-redaction)
- **`getRecords()` `$selected` is a snapshot** — subsequent UI clicks change selection but the previously returned array is not updated; re-call `getRecords()` after user interaction.
- **`selectRecordsByID(ids)` silently ignores ids not present in the current page of records** — Custom-View pagination / row-virtualization may make some ids unreachable.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `freezeColumns` | List | — | — |
| `maskField` | List | List | — |
| `sortByField` | List | List | — |
| `getRecords` | List | List | — |
| `selectRecords` | List | List | — |
| `selectRecordsByID` | List | List | — |
| `clearSelection` | List | List | — |
| `style` | List | List | — |
