## FILE_PURPOSE
Read when invoking the `POST /coql` endpoint — scopes, headers, per-field-type comparator matrix, aggregate / alias / CVID / external-ID / metadata samples, and the full COQL error code list.

## SOURCE_DOC
https://www.zoho.com/crm/developer/docs/api/v8/Get-Records-through-COQL-Query.html

## TRIGGER_KEYWORDS
POST /coql, ZohoCRM.coql.READ, include_meta, like wildcard, CVID, what_id, External_Id, consent_lookup, INVALID_QUERY, LIMIT_EXCEEDED, What_Id->

## TECHNICAL_CONSTRAINTS
- Endpoint — `POST {api-domain}/crm/{version}/coql`. HTTP method is **POST** (the verb refers to "posting" the query body, not writing records). Body shape: `{ "select_query": "<query>" }`.
- Authorization header — `Authorization: Zoho-oauthtoken <token>`.
- Mandatory scope — `ZohoCRM.coql.READ` **AND** `ZohoCRM.modules.{operation_type}` OR `ZohoCRM.modules.{module_name}.{operation_type}`. `operation_type` ∈ `{ALL, READ}` (ALL = full data access, READ = get module data).
- Metadata retrieval (`include_meta` key in the body) additionally requires `ZohoCRM.settings.fields.READ` — calls without it raise `OAUTH_SCOPE_MISMATCH` 401.
- Supported base modules: `leads`, `accounts`, `contacts`, `users`, `deals`, `campaigns`, `tasks`, `cases`, `events`, `calls`, `solutions`, `products`, `vendors`, `pricebooks`, `quotes`, `salesorders`, `purchaseorders`, `invoices`, and `custom` (custom modules).
- Per-field-type comparator matrix (mandatory — use only these per field type):
  - Text: `=`, `!=`, `like`, `not like`, `in`, `not in`, `is null`, `is not null`.
  - Picklist: `=`, `!=` only —  `in`, `not in`, `like`, `not like` appear in the source comparator table but are rejected by the COQL engine at runtime. Apply exclusion logic client-side.
  - Lookup, Multi-module lookup / `what_id`, Roles & Profiles, Alias: `=`, `!=`, `in`, `not in`, `is null`, `is not null`.
  - Date, DateTime, Number: `=`, `!=`, `>=`, `>`, `<=`, `<`, `between`, `not between`, `in`, `not in`, `is null`, `is not null`.
  - Boolean (raw field): `=` (source explicitly lists only `=`).
  - Rollup Summary: `=`, `!=`, `>=`, `>`, `<=`, `<`, `between`, `not between`, `in`, `not in`, `is null`, `is not null`. From V7, Date / DateTime return types return values in their native formats.
- **Formula field** comparators vary by return type (separate table on source):
  - Formula returning Decimal / Date / DateTime / Number: `=`, `!=`, `>=`, `>`, `<=`, `<`, `between`, `not between`, `in`, `not in`, `is null`, `is not null`.
  - Formula returning String (text): `=`, `!=`, `like`, `not like`, `in`, `not in`, `is null`, `is not null`.
  - Formula returning Boolean: `is null`, `is not null`, `equals`.
- Encrypted-field rules — numeric encrypted fields support only `=`, `!=`, `is null`, `is not null`; non-numeric encrypted fields support only `is null` and `is not null`. Encrypted fields are valid in both SELECT and WHERE.
- `like` wildcard grammar — `%tech` = ends-with, `tech%` = starts-with, `%tech%` = contains. `not like` only behaves correctly when `%` is at BOTH ends (`not like "%tech%"` = does-not-contain); single-sided `%` with `not like` does NOT work.
- `in` / `not in` accept up to 100 values per comparator in the SELECT-column criterion.
- Aggregate functions (`SUM`, `MAX`, `MIN`, `AVG`, `COUNT`) — case-sensitive; only valid on numeric data types (`integer`, `decimal`, `currency`, `bigint`, formula fields returning those). `COUNT` additionally supports `number`, `lookup`, `picklist`. `GROUP BY` is mandatory when aggregate and non-aggregate fields appear together in SELECT.
- `Full_Name` is a read-only concatenation of `First_Name` + `Last_Name`, available only in Leads and Contacts.
- Module API name disambiguation — when a module API name collides with a field API name in a path, prefix the module reference with `!` (e.g. `!Leads.Owner.role.id`).
- Multi-module lookup (`what_id`) — supported only for `Tasks`, `Calls`, `Events`; query the associated record via `What_Id->{Module}.{field}` path syntax.
- Multi-Module Lookup module name query (separate from `What_Id` traversal) — to discover the module each record is associated with for an MML field (e.g. `Appointment_For` on the Appointments module), query the field directly in SELECT.
- Lookup field WHERE-filter compares against the target record's `id` (not its display name): `where Owner = '554023000000235011'` — pre-fetch the target record id before composing the filter.
- Record Image / Profile Image — the `Record_Image` field IS queryable in COQL (returns the image ID, which feeds the GET Files API); this is an exception to the Limitations page's blanket "Image upload field is not supported."
- Subform data — query via the subform's own module API name (subforms are independent modules).
- Multi-select lookup fields (MxN) — query via the auto-generated **linking module**, not the parent module's field.
- Custom View querying — `FROM {module_API_name}#{CVID}`. Unsupported CV types: `Shared By Me`, `Co-owner`, `Shared To Me`.
- Territory fields — supported in SELECT only; field API name is `Territories` for Accounts / Contacts / Leads and `Territory` for Deals.
- V7+ lookup display names — available for Lookup and User Lookup fields in SELECT; **not** available for Consent Lookup or Multi-Module Lookup (MML). Users-module display field is `last_name`.
- Consent Lookup requires GDPR enabled on the module; the auto-created field has data type `consent_lookup` and is discovered via Field Metadata API.
- Roles & Profiles fields available from the owner lookup — role: `id`, `name`, `reporting_to`, `share_data_with_peers`, `description`. Profile: `id`, `name`, `created_by`, `modified_by`, `description`, `created_time`, `modified_time`.
- `include_meta` request key — value type is `JSON array`; supported element value is `fields` (string). Returns field metadata for SELECT-column fields.
- Tuple is not supported in COQL.

### Deluge Usage
Calling COQL from a Deluge Function via `invokeurl`:

1. **Workbench WHERE-clause runtime requirement** — The Queries Workbench COQL source type requires a WHERE clause at runtime even though the COQL grammar marks WHERE as optional. If no real filter is needed, use `is not null` on a key field: `WHERE (id is not null)`. The standalone `POST /crm/v8/coql` API does not enforce this restriction.
2. **`is not null` vs `= null`** — Use `is null` / `is not null` for null checks; `= null` or `!= null` raises SYNTAX_ERROR 400.
3. **Body map construction** — Build the request body as a Deluge Map variable first; inline map literals in `parameters` cause Improper Statement Error:
```deluge
bodyMap = Map();
bodyMap.put("select_query", "SELECT id, Last_Name FROM Leads WHERE Lead_Status = 'New' LIMIT 0, 200");
response = invokeurl
[
    url: "https://www.zohoapis.com/crm/v8/coql"
    type: POST
    parameters: bodyMap.toString()
    connection: "crm_connection"
];
records = response.get("data");
```
4. **Pagination from Deluge** — Capture `response.get("info").get("more_records")` (boolean); increment the LIMIT offset by `per_page` per iteration and `break` when `more_records` is false or the data list is empty.

## REQUIRED_PARAMETERS
- Request body — `{ "select_query": "<COQL SELECT statement>" }`. The `select_query` key is mandatory and the only top-level key.
- Optional metadata key — `"include_meta": ["fields"]` (requires `ZohoCRM.settings.fields.READ`).
- Header — `Authorization: Zoho-oauthtoken <token>`.
- Pagination cursor — when paging beyond a single response, capture `info.more_records` and bump `LIMIT <offset>, <limit>` accordingly.

## UI_ONLY_ACTIONS
*(none in source)*

## CRITICAL_FAILURE_MODES
- `SYNTAX_ERROR` 400 — query missing proper criteria, base table, or WHERE clause. Resolution: form a query with all three.
- `SYNTAX_ERROR` 400 — query missing `FROM`. Resolution: supply a `FROM <module>` clause.
- `SYNTAX_ERROR` 400 — non-SELECT statement (`update Leads set ...`). Resolution: COQL is read-only; use the v8 Records API for writes.
- `SYNTAX_ERROR` 400 — `Parsing is happening for so long for the given query` (unbalanced parens / over-complex). Resolution: re-bracket the WHERE; simplify.
- `LIMIT_EXCEEDED` 400 — LIMIT or SELECT column count breached. Canonical caps (per Overview + Limitations pages, which agree): max 2000 records per call, max 500 SELECT fields. The error message text on this page reads `maximum limit of 200 and 500` / `fetch only a maximum of 200 records and 50 fields`;
- `LIMIT_EXCEEDED` 400 — more than two joins in a single SELECT chain depth (`A.B.C`). Resolution: cap relation chain at depth 2; for more, switch to the Bulk Read API or split queries.
- `LIMIT_EXCEEDED` 400 — `Max records limit exceeded` past 1,00,000 records per criteria. Resolution: paginate with id-continuation criteria or use Bulk Read API.
- `LIMIT_EXCEEDED` 400 — more than 100 values in an `in` / `not in` comparator. Resolution: chunk the value set across multiple queries.
- `LIMIT_EXCEEDED` 400 — ORDER BY fields > 10; GROUP BY fields > 4; aggregate fields > 5. Resolution: cut to the cap.
- `INVALID_QUERY` 400 — invalid column name (typo / display-label use). Resolution: use API name. (`label-vs-api-name`)
- Picklist field filtered with `!=`, `NOT IN`, `IN`, `LIKE`, or `NOT LIKE` in WHERE (e.g. `Stage NOT IN ('Closed Won','Closed Lost')`): rejected at runtime — Picklist only supports `=`, `!=` in WHERE despite the comparator matrix listing broader operators. Apply exclusion logic client-side after fetching with `=`, `!=` or without a stage filter.
- `INVALID_QUERY` 400 — unsupported data type in SELECT (e.g. multi-select lookup used directly instead of via linking module). Resolution: switch to the linking module per the MxN rule.
- `INVALID_QUERY` 400 — value type mismatch (`No_of_Employees = 'adfkahfd'`). Resolution: pass values of the correct type for each field.
- `INVALID_QUERY` 400 — invalid operator for field type. Resolution: consult the per-type comparator matrix above.
- `INVALID_QUERY` 400 — `include_meta` value or datatype invalid. Resolution: value must be `fields`; datatype must be JSON array of text.
- `INVALID_QUERY` 400 — Territory fields used outside SELECT. Resolution: restrict territory fields to SELECT.
- `INVALID_QUERY` 400 — invalid CVID. Resolution: fetch a valid CVID via the Custom Views Metadata API.
- `INVALID_ALIAS` 400 — empty-string alias. Resolution: supply a non-empty alias.
- `OAUTH_SCOPE_MISMATCH` 401 — user lacks the required module scope or `ZohoCRM.settings.fields.READ` when `include_meta` is set. Resolution: have admin grant the scope.
- `DUPLICATE_DATA` 400/401 — duplicate SELECT columns, duplicate aggregate fields, or duplicate fields in ORDER BY / GROUP BY. Resolution: deduplicate.
- `DUPLICATE_ALIAS` 400 — same alias bound to multiple SELECT columns. Resolution: alias each column uniquely.
- `INTERNAL_ERROR` 500 — server-side exception. Resolution: retry; escalate to support if persistent.
- `INVALID_REQUEST_METHOD` 400 — non-POST verb on `/coql`. Resolution: POST only.
- `not like` used with `%` on only one side (`not like "%tech"`): silently does not filter — wrap with `%` on both ends for not-contains, or pivot to `=` / `!=` for exact match.
- Notes-module fetch by non-admin user: source states "Only admin users can fetch the records from the Notes module" — failure mode (error code vs empty response) is not specified. `OAUTH_SCOPE_MISMATCH` / `INVALID_QUERY` / empty `data[]`. Gate Notes queries behind an admin permission check at author-time regardless.
- Querying a lookup field without including the linked module's display field: response carries only the `id` — to fetch the display value, also include `<lookup>.<display_field>` in SELECT.
- Consent Lookup queried in an org where GDPR is not enabled: `data_type: consent_lookup` field does not exist on the module — verify GDPR setup before query author-time.
- `What_Id` used on a module outside `{Tasks, Calls, Events}`: feature does not apply elsewhere — fall back to direct lookup traversal.
- Multi-module lookup display name read from the response: source documents display-name unavailability for MML and Consent Lookup; only `id` is returned — separate metadata fetch required.
