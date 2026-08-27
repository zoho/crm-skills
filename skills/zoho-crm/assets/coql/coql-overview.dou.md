FILE_PURPOSE: Read when composing a COQL `select_query` body — SELECT / FROM / WHERE / GROUP BY / ORDER BY / LIMIT grammar, alias rules, pagination beyond 100K, and API-credit cost.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/api/v8/COQL-Overview.html
TRIGGER_KEYWORDS: COQL, select_query, SELECT, WHERE, ORDER BY, LIMIT OFFSET, GROUP BY, alias AS, pagination, API credits

TECHNICAL_CONSTRAINTS:
- COQL is the SQL-like read-only query language for CRM modules and fields; it uses module + field **API names** verbatim as table / column names (never display labels).
- Only `SELECT` statements are accepted — `UPDATE` / `INSERT` / `DELETE` issued through the COQL endpoint return `SYNTAX_ERROR` HTTP 400.
- Supported clause set: `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT offset, limit`. The two LIMIT operands are written `LIMIT <offset>, <limit>` — offset first, limit second.
- `LIMIT` default value is 200; max value is 2000 per single API call.
- Default sort is ascending by record `id` when `ORDER BY` is omitted.
- COQL keywords are case-insensitive (`SELECT` ≡ `select`) **except** aggregate function names (`SUM`, `MAX`, `MIN`, `AVG`, `COUNT`) which are case-sensitive.
- SQL reserved words and field API names containing special characters must be enclosed in single quotes inside the query string (e.g. `select Last_Name, 'Dynamic' from Contacts ...`).
- `SELECT` accepts up to 500 field API names per query.
- `WHERE` accepts up to 25 criteria; for three criteria A,B,C the source documents four valid bracketing forms: `(A and (B and C))`, `((A and B) and C)`, `A and (B and C)`, `(A and B) and C`. Fully-unbracketed `A and B and C` is rejected as ambiguous.
- Alias support uses `AS` (case-insensitive) and is valid **only** in the SELECT column list and the `order_by` clause — alias values appear as the corresponding response keys.
- `GROUP BY` and aggregate functions: `SUM`, `MAX`, `MIN`, `AVG`, `COUNT`. `GROUP BY` is mandatory whenever aggregate and non-aggregate fields appear together in `SELECT`.
- Pagination beyond the 1,00,000-record per-unique-criteria ceiling requires chaining queries: capture the last record's `Created_Time` and `id` from the previous page, then add `Created_Time > '<last>' and id > <last_id>` to the next query's WHERE.
- Pagination per unique criteria caps at 1,00,000 records across multiple API calls — for larger sets, switch to the Bulk Read API (not the COQL endpoint).
- API credit cost per call scales with `LIMIT`: `1`–`200` = 1 credit; `201`–`1000` = 2 credits; `1001`–`2000` = 3 credits.
- Request body shape is exactly `{ "select_query": "<query string>" }` — single JSON key, mandatory, value is the COQL SELECT statement as one string.
- Response envelope is `{ "data": [...], "info": { "count": <n>, "more_records": <bool> } }`; `more_records: true` signals further pages exist under the same criteria.
- Aliases are echoed back as the corresponding JSON keys in the `data[]` response objects; without an alias, the key is the field API name.
- `null` literals are supplied via `is null` / `is not null` only — `= null` is invalid syntax (source documents `is null` / `is not null` as the only null comparators).

REQUIRED_PARAMETERS:
- Query string skeleton: `SELECT <field_api_name>[, ...] FROM <module_api_name> [WHERE <criteria>] [GROUP BY <fields>] [ORDER BY <fields> ASC|DESC] [LIMIT <offset>, <limit>]`.
- Field API names: discover via the Field Metadata API or `Setup → Developer Hub → APIs and SDKs → API Names → {module}`.
- Aliased projection example: `select 'Account_Name' AS 'Account id', 'Account_Name.Account_Name' as 'Account Name' from Contacts where (Account_Name.Parent_Account.Account_Name = 'King') limit 1`.
- Pagination-beyond-100K continuation criteria: `((<other criteria>) and id > <last_record_id>)` (adjust against the actual ORDER BY axis if custom-sorted).
- Cross-module field traversal uses the `.` operator on lookup fields (e.g. `Account_Name.Account_Name`) — see the JOINs DOU node for join-count caps.

UI_ONLY_ACTIONS:
- Look up field API names by module: `Setup → Developer Hub → APIs and SDKs → API Names → {module}`. Note: equivalent to the Field Metadata REST API.

CRITICAL_FAILURE_MODES:
- **Queries Workbench COQL source enforces a WHERE clause at runtime even though the grammar documents it as optional** — a query with no WHERE is rejected. Always include at least one `is not null` criterion when there is no real filter condition (e.g. `WHERE (Account_Name is not null)`). The standalone `POST /crm/v8/coql` endpoint does not enforce this; the restriction is Workbench-specific.
- `= null` or `!= null` written instead of `is null` / `is not null`: `SYNTAX_ERROR` 400 — the only valid null-comparison forms are `is null` and `is not null`.
- Query references a field by display label (`"Last Name"`) instead of API name (`Last_Name`): returns `INVALID_QUERY` 400 with `invalid column name`. (`label-vs-api-name`)
- `LIMIT 0, 2500` or any `limit` value > 2000: `LIMIT_EXCEEDED` 400 — split across pages of ≤ 2000.
- Aggregate function in lowercase (`sum`, `count`): query parses but does not execute as aggregate — aggregate function names are case-sensitive per source `Notes`.
- `WHERE` with three or more criteria written without surrounding brackets (`A and B and C`): parser ambiguity → `SYNTAX_ERROR` 400 (`Parsing is happening for so long for the given query`) — always nest as `(A and (B and C))` or `((A and B) and C)`.
- `SELECT` column count exceeds 500: `LIMIT_EXCEEDED` 400 (`maximum limit of 200 and 500`) — partition into multiple queries.
- Issuing `UPDATE` / `INSERT` / `DELETE` through the `/coql` endpoint: `SYNTAX_ERROR` 400 (`The request contains a query other than select`). COQL is read-only; writes require the v8 Records API (see parent skill Top-5 gotcha on `trigger`-map suppression for the write path).
- Pagination past 1,00,000 records under the same WHERE without adding the `id > <last_id>` continuation criteria: `LIMIT_EXCEEDED` 400 (`Max records limit exceeded`) — either add continuation criteria or move to Bulk Read API.
- Alias supplied as an empty string (`'Account_Name' AS ""`): `INVALID_ALIAS` 400 — alias must be a non-empty string per source.
- Alias used outside SELECT / `order_by` (e.g. in WHERE): query parser rejects — alias scope is restricted to SELECT and ORDER BY per source.
- Custom-view-based query targeting `Shared By Me` / `Co-owner` / `Shared To Me`: those CVs are unsupported in COQL (see Get-Records DOU) — pick a supported view ID.
- Aggregate function duplicated in SELECT (`COUNT(De1), COUNT(De1)`): `DUPLICATE_DATA` 401 — deduplicate aggregate columns.
- COQL caller assumes default ORDER BY is by `Created_Time`: source documents default as ascending by `id` only — supply explicit `ORDER BY` when chronological order is required.
- `select_query` JSON body missing the `select_query` key (any other key name): the request fails JSON-schema validation — the only accepted top-level key is `select_query`.
- API-credit consumption planning that assumes 1 credit per call regardless of LIMIT: a single `LIMIT 0, 2000` call costs 3 credits — model credit cost against the LIMIT brackets above.
- SQL reserved word used unquoted in SELECT (e.g. `select Dynamic from Contacts`): parser rejects — wrap in single quotes (`'Dynamic'`).
- `= null` written instead of `is null`: `SYNTAX_ERROR` 400 — the only null-comparison form is `is null` / `is not null`.
- LIMIT operands transposed (caller writes `LIMIT <count>, <offset>` per MySQL convention instead of COQL's `LIMIT <offset>, <count>`): row set is empty or skips wrong window with no error — COQL parses the first integer as offset, second as count.
