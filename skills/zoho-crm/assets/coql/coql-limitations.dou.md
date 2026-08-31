FILE_PURPOSE: Read when sizing or validating a COQL query against per-call hard caps — record / clause / JOIN / subquery / aggregate counts, unsupported field types in WHERE, and module-level access restrictions.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/api/v8/COQL-Limitations.html
TRIGGER_KEYWORDS: COQL limits, max records, max joins, max subqueries, unsupported field, Territory in WHERE, Notes admin, multi-select lookup criteria, subform

TECHNICAL_CONSTRAINTS:
- **Record pagination ceiling** — at most 1,00,000 records can be returned across paginated calls per unique criteria. For larger sets, switch to the Bulk Read API.
- **Per-call LIMIT cap** — max 2000 records per single API call; default 200 (see [coql-overview.dou.md](./coql-overview.dou.md)).
- **SELECT column cap** — max 500 fields in the SELECT clause per query.
- **WHERE criteria cap** — max 25 criteria in WHERE per query.
- **ORDER BY cap** — max 10 fields.
- **GROUP BY cap** — max 4 fields.
- **Aggregate function cap** — max 5 aggregate columns per query.
- **Dynamic formula field cap** — max 5 dynamic formula fields in SELECT per query.
- **`IN` / `NOT IN` value cap** — max 100 values per comparator.
- **Subquery caps** — max 5 subqueries per parent query; max 100 records per subquery; subqueries valid only in WHERE; single SELECT column inside the subquery (see [coql-subquery.dou.md](./coql-subquery.dou.md)).
- **JOIN caps** — max 5 Base JOINs per query; max 15 SELECT-column JOINs per query (see [coql-joins.dou.md](./coql-joins.dou.md)).
- **Relation-chain depth cap** — max 2 relations per single dotted traversal (`A.B.C` is depth 2; `A.B.C.D` exceeds the cap).
- **Silent partial-validation for > 2 relations** — source literally states: "If you use more than two relations in a select query, system validates only the last two relations." This contradicts the Get-Records error catalog which raises `LIMIT_EXCEEDED` for "more than two joins."
- **Notes module** — only admin users can query the Notes module via COQL. Non-admin requests return empty / forbidden.
- **Unsupported field types in WHERE / criteria** — Territory fields (Accounts/Contacts/Leads `Territories`, Deals `Territory`), Multi-Select Lookup, Multi-line text fields (`Description`, `Terms and Conditions`, `Comments`), Line Items, Participants, File Upload, Attachments, Image Upload, Tuple.
- **Territory fields** — usable only in SELECT, never in WHERE / ORDER BY / GROUP BY.
- **Multi-line text fields** in `{Description, Terms and Conditions, Comments}` — cannot be used in criteria; safe in SELECT only.
- **Multi-Select Lookup (MxN)** — direct field reference in WHERE is unsupported; query via the linking module instead (see [coql-execute.dou.md](./coql-execute.dou.md)).
- **Subform** — query via the subform module's own API name (subforms are independent modules); cannot be traversed via `.` from the parent module.
- **`Tuple` data type** — unsupported across the COQL surface.
- **Image Upload vs Record Image** — generic Image Upload fields are unsupported; the special `Record_Image` (profile image) field IS queryable in COQL and returns the image ID (see [coql-execute.dou.md](./coql-execute.dou.md)).
- **External ID lookup** — supported (per Get-Records source); query via `External_Id_Field_API_Name` directly.
- Picklist WHERE comparator runtime cap: `=`, `!=` are the only operator reliably accepted by the COQL engine for Picklist fields. The Limitations page (listing only `=`) matches production behavior; the Get-Records comparator matrix listing `in`, `not in`, `like`, `not like` for Picklist is stale. Use only `=` for Picklist WHERE filters; handle exclusion logic client-side.
- **Encrypted fields** — restricted comparator set (see [coql-execute.dou.md](./coql-execute.dou.md)).
- **API credit consumption per call** — `LIMIT 1`–`200` = 1 credit, `LIMIT 201`–`1000` = 2 credits, `LIMIT 1001`–`2000` = 3 credits.

REQUIRED_PARAMETERS:
- Pagination beyond 1,00,000 — paginate within the cap, then issue a new query with continuation criteria `(<prior criteria>) and id > <last_id_returned>`; otherwise switch to Bulk Read API.
- Per-clause budget audit — sum (SELECT fields ≤ 500), (WHERE criteria ≤ 25), (ORDER BY ≤ 10), (GROUP BY ≤ 4), (aggregates ≤ 5), (dynamic formula ≤ 5), (`IN` values ≤ 100), (subqueries ≤ 5, each ≤ 100 rows / 1 SELECT col), (Base JOINs ≤ 5), (SELECT-col JOINs ≤ 15), (relation chain depth ≤ 2) before submitting.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- Query pulls > 1,00,000 records under one criteria via repeated paging: `LIMIT_EXCEEDED` 400 (`Max records limit exceeded`) — switch to Bulk Read API or rotate criteria.
- LIMIT > 2000 in a single call: `LIMIT_EXCEEDED` 400 — cap at 2000 per Overview + Limitations (agreed). The Get-Records error string reads `200` / `50 fields`; treat that error text as stale, not as a separate cap 
- WHERE includes Territory field as a filter: query returns `INVALID_QUERY` 400 — restrict territory fields to SELECT only.
- WHERE includes Multi-Select Lookup field directly: `INVALID_QUERY` 400 — query via the linking module.
- WHERE includes `Description` / `Terms and Conditions` / `Comments` (multi-line text): `INVALID_QUERY` 400 — restrict to SELECT only.
- WHERE includes a line item, Participant, File Upload, Attachment, or Image Upload field: `INVALID_QUERY` 400 — these data types are not queryable in COQL criteria.
- Non-admin user issues a query against the Notes module: silently returns empty / unauthorised — gate Notes queries behind an admin permission check before composing.
- 6th subquery added to a parent query: `LIMIT_EXCEEDED` 400 — split across multiple API calls.
- 16th SELECT-column JOIN or 6th Base JOIN added to a query: `LIMIT_EXCEEDED` 400 — partition the projection / filter.
- `IN`-list of 101 values in a single WHERE comparator: `LIMIT_EXCEEDED` 400 — chunk values into batches of ≤ 100.
- 11th ORDER BY field / 5th GROUP BY field / 6th aggregate column / 6th dynamic formula in SELECT: `LIMIT_EXCEEDED` 400 — trim to the per-clause budget.
- 26th WHERE criterion or 501st SELECT field: `LIMIT_EXCEEDED` 400 — split across multiple queries.
- Single dotted traversal of depth 3 (`A.B.C.D`): `LIMIT_EXCEEDED` 400 (`more than two joins`) — flatten via intermediate query or subquery.
- Subform queried via parent-module dot traversal (`Parent_Module.Subform_Field.Inner_Field`): unsupported — query the subform's own module API name directly.
- Author treats Tuple field as queryable: feature unavailable — Tuple is not supported in any COQL clause.
- Pre-V7 client assumes Lookup display names auto-return: only V7+ surfaces display names for Lookup / User Lookup; older API versions return only `{id, name}` (see [coql-execute.dou.md](./coql-execute.dou.md)).
- Author depends on Consent Lookup display name returning: never surfaced (only `id`) — separate Field Metadata fetch required.
- Credit-budget exhaustion under sustained `LIMIT 2000` paging: each call costs 3 credits — model 3 × page_count against the org's per-day credit budget.
- Caller relies on `more_records: false` to declare completion at exactly 1,00,000 records: per source, the cap is per unique criteria — `more_records` returns `false` both when the dataset ends and when the cap is hit. Distinguish dataset end vs cap hit via cumulative row count check against 1,00,000.
