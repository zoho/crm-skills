FILE_PURPOSE: Read when associating a Query with a Canvas (Record / List), Kiosk (Screen / Decision), or Custom Related List — variable mapping, Map vs Table return type, and the View Associations audit.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/queries/associating-a-query.html, queries-overview.dou.md
TRIGGER_KEYWORDS: Canvas, Kiosk, Custom Related List, Associate Query, Variable mapping, Map type, Table type, View Associations, Add Related List, Decision component

TECHNICAL_CONSTRAINTS:
- A saved Query can be bound to exactly four placement surfaces: **Canvas Record Detail View**, **Canvas List View**, **Kiosk Screen**, **Kiosk Decision**, and **Custom Related List**. (Canvas Record + Canvas List are both Canvas — the binder UI differs.)
- Every association is a separate object — deleting the Query orphans every binding; `View Associations` (Query three-dot menu) is the only audit surface.
- Each association passes its own **Variable Mapping** — every `{{Variable}}` declared in the Query body must be mapped to a CRM field, merge token, or earlier-screen output at every binding point; unmapped variables resolve to empty string at runtime.
- Schema return type drives placement compatibility: **Map** for single-record / key-value (Canvas single-field bindings, Workflow field assignment); **Table** for multi-record (List View Canvas, Kiosk Screen multi-row, Custom Related List).
- Canvas single-field association rejects Table-shaped responses — only Map shapes resolve to a single value.
- List View Canvas requires Table-shape — Map shapes render only the first record.
- Kiosk Decision can only consume a Query whose data was fetched in an **earlier** Screen of the same Kiosk — direct fetch from the Decision step is not supported.
- Custom Related List binding lives on the record's three-dot menu (`Add Related List → Queries`); list is per-record-view and re-executes on every record open with the merge-field-mapped variables.
- Serializer is the recommended hook for lookup expansion in Custom Related Lists — return `{ id, name, module }` objects to render clickable cell links, and `{ label, href }` objects to render external URLs (see [queries-overview.dou.md](./queries-overview.dou.md)).
- Filter-by-Record-ID (Module type's `Record ID` criteria mode) returns the single record directly; using Record ID inside a `Criteria` clause returns a one-element array — placement consumers must handle the array shape.
- Variable mapping at the association is per-binding — the same Query bound to two Canvases can map the same `{{Variable}}` to different merge fields.
- `View Associations` enumerates every binding but does not show variable-mapping details — open each binding to inspect.
- Re-saving a Query that has live associations does not force re-mapping — variables added after the fact remain unmapped until each association is re-opened and re-saved.

REQUIRED_PARAMETERS:
- Canvas association: `{ Association_Name, Source, Query, Display_Type, Variable_Mappings: Record<varName, crm_field> }`.
- Kiosk Screen association: `{ Query, Fields[], Record_Preference: 'single' | 'multiple', Identifiers? (when multiple) }`.
- Kiosk Decision association: `{ Query (must reference earlier-screen data), Criteria }`.
- Custom Related List association: `{ Related_List_Name, Query, Variable_Mappings: Record<varName, merge_field> }`.
- For Module-type Query bound by record context: choose `Record ID` (criteria mode) for one-shot single-record fetch, or place `{{Record_ID}}` inside `Criteria` to fetch related records as an array.

UI_ONLY_ACTIONS:
- Associate with Canvas Record Detail: `Setup → Customization → Modules and Fields → {Module} → Canvas → Detail View → Canvas editor → Queries (left panel database icon) → Associate Query → fill Name + Source + Query + Display Type + Variable Mappings → Done`. Note: No API equivalent — UI-only.
- Associate with Canvas List View: `Setup → Customization → Modules and Fields → {Module} → Canvas → List View → New / Edit canvas template → Associate Query → fill Variable Mappings → Done`. Note: No API equivalent.
- Associate with Kiosk Screen: `Setup → Customization → Kiosk → {Kiosk} → Edit → + → Screen → Get data via Queries → New Query (or pick existing) → choose Fields + single/multiple + identifiers → Save`. Note: No API equivalent.
- Associate with Kiosk Decision: `Setup → Customization → Kiosk → {Kiosk} → + → Decision → Add conditions based on → Queries → choose Query → define Criteria → Done`. Note: Decision can only consume Queries fetched by an earlier Screen.
- Associate with Custom Related List: open a record in the target module → record three-dot menu → `Add Related List → Queries → pick Query → name list → map merge fields to {{Variables}} → Done → Save`. Note: No API equivalent.
- Audit placements: `Setup → Developer Hub → Queries → hover Query → three-dot icon → View Associations`. Note: No API equivalent.

CRITICAL_FAILURE_MODES:
- Table-shaped Query bound to a Canvas single-field slot: rendering error or unexpected behaviour — convert to Map (e.g. wrap with a Serializer that returns the first record) or rebuild the Query with a single-record criteria.
- Map-shaped Query bound to a List View Canvas: only the first record renders — convert to Table by removing single-record criteria or returning an array from the Serializer.
- Kiosk Decision references a Query whose data was not fetched in an earlier Screen: Decision evaluates against an empty payload and routes incorrectly — pre-fetch in a Screen step.
- Variable declared in the Query but not mapped at an association: substitution resolves to empty string; downstream criteria silently filter wrong records — re-open each binding after every Query edit to confirm every `{{Variable}}` has a mapping target.
- Variable mapping renamed in the CRM field but not re-saved at the association: stale field reference returns null — re-bind on every merge-field rename.
- `Record ID` filter mode chosen but caller still wraps the result as `result[0]` because they tested with `Criteria` first: shape differs between the two modes — branch on mode, do not assume array.
- Custom Related List bound to a Query that references a Subform field by display label: list renders blank cells — use Subform-field API names. (label-vs-api-name)
- Canvas List View Query missing `LIMIT` in COQL body relies on the default 100 (see [queries-limits.dou.md](./queries-limits.dou.md)): user expects "all records" but sees 100 — set explicit LIMIT and paginate in the consumer.
- Custom Related List rebound to a new Query API Name without updating the variable mapping: new Query's variables differ — re-open and re-map.
- `View Associations` not consulted before deleting a Query: every binding silently breaks — audit before delete.
- Kiosk Screen Query returning a Table when a single record is expected: identifier configuration becomes mandatory — set the identifier field, or constrain the Query to return a Map.
- Map vs Table type assumed to be settable explicitly on the Schema editor: type is implicit in the response shape — adjust by criteria / Serializer, not by Schema metadata.
- Same Query bound to two Canvases on the same Module: each carries an independent variable mapping — editing one mapping does not propagate to the other.
- Association Name reused across two Canvases on the same record: editor enforces uniqueness within a Canvas template but not cross-template — adopt a naming convention to avoid confusion.
- Canvas / Kiosk Display Type changed after Variable Mappings were filled: mappings sometimes reset — re-verify after every Display Type switch.
- Query renamed (display name only, not API Name): existing associations remain valid; API Name is the binding key. (label-vs-api-name)
- Query bound to a placement under the Profile of an admin then tested by an end-user whose Profile lacks read access on the underlying Module / Source: the association loads but rows are filtered to zero — verify with a representative profile.
- Custom Related List binding on a record whose module field used for the merge-mapping (e.g. `Shipping Code`) is null: query executes with empty `{{Variable}}` and returns wrong results — gate the related-list visibility on the field being non-null, or branch inside the Serializer.
