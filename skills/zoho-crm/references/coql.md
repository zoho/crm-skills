# COQL — CRM Object Query Language

> DOU nodes are the authoritative source for syntax, comparators, JOINs, subqueries, limitations, and error codes — see [DOU Reference Nodes](#dou-reference-nodes) below.

**COQL** (CRM Object Query Language) allows SQL-like queries to fetch records from Zoho CRM modules using module and field API names. Supports cross-module retrieval via lookup dot notation, subqueries, aggregations, and pagination.

**COQL is read-only** — only `SELECT` is supported, no writes.

---

## When to Use COQL

| Use case | Notes |
|---|---|
| Programmatic / code-driven data retrieval | REST API call, Deluge `invokeurl`, external scripts |
| Complex multi-field filter conditions | Up to 25 WHERE criteria |
| Cross-module field retrieval (JOINs) | Dot notation: `Account_Name.Industry` |
| Aggregations (COUNT, SUM, AVG, MIN, MAX) | With GROUP BY |
| Custom view filtering | `FROM {module}#{CVID}` |

## COQL vs Queries (Native SQL API)

> **Choosing between them**: COQL is for programmatic/code use. Queries is a UI-only Workbench tool for binding data to Canvas, Kiosk, or Custom Related Lists. See [queries.md](./queries.md#when-to-use-queries) for full comparison.

| | COQL | Queries (Native SQL) |
|--|------|---------------------|
| Endpoint | `POST /crm/{version}/coql` | `POST /crm/{version}/query` |
| Authoring | Code / API / Deluge `invokeurl` | CRM UI — `Setup → Developer Hub → Queries` |
| Syntax | COQL (SQL-like, CRM-specific) | Standard SQL |
| Related fields | Dot notation (`Account_Name.Industry`) | Explicit JOIN syntax |
| Max records/call | **2,000** | 200 |
| Max records/criteria | 1,00,000 (pagination) | 1,00,000 |
| Scope | `ZohoCRM.coql.READ` | `ZohoCRM.modules.READ` |
| Invoke from Deluge | `invokeurl` to `POST /crm/{version}/coql` | `zoho.crm.invokeQuery(apiName, variableMap)` |

## Endpoint

```
POST https://www.zohoapis.com/crm/{version}/coql
```

**Required scope:** `ZohoCRM.coql.READ` AND `ZohoCRM.modules.{module}.READ` (or `.ALL`)

**Header:** `Authorization: Zoho-oauthtoken <access_token>`

**Request body:**
```json
{
  "select_query": "select Last_Name, Email from Leads where Lead_Status = 'New' limit 0, 200"
}
```

**Response:**
```json
{
  "data": [
    { "Last_Name": "Smith", "Email": "smith@example.com" }
  ],
  "info": {
    "count": 1,
    "more_records": true
  }
}
```

> **Note:** Although you are fetching data, the HTTP method is **POST** because you are posting the query body.

- Optional body key `"include_meta": ["fields"]` — returns field metadata for SELECT columns
- Requires `ZohoCRM.settings.fields.READ`; omitting it → `OAUTH_SCOPE_MISMATCH` 401
- → [coql-execute.dou.md](../assets/coql/coql-execute.dou.md)

## SELECT Query Syntax

```
SELECT <field> [, ...] FROM <module_api_name>[#{CVID}]
  [WHERE <criteria>] [GROUP BY <fields>]
  [ORDER BY <fields> ASC|DESC] [LIMIT <offset>, <count>]
```

- LIMIT: default 200 / max 2000; **offset-first** — `LIMIT 0, 200` fetches rows 1–200
- WHERE: max 25 criteria; 3+ must be bracketed — valid: `(A and (B and C))` / `((A and B) and C)` / `A and (B and C)` / `(A and B) and C`; fully unbracketed → `SYNTAX_ERROR`
- Null: `is null` / `is not null` only — `= null` → `SYNTAX_ERROR`
- `FROM {module}#{CVID}` — filter by Custom View; unsupported CVs: `Shared By Me`, `Co-owner`, `Shared To Me`
- Aggregate function names (`SUM` `MAX` `MIN` `AVG` `COUNT`) are **case-sensitive**; all other keywords case-insensitive
- `GROUP BY` mandatory when aggregate and non-aggregate fields coexist in SELECT
- Reserved words in SELECT must be single-quoted: `'Dynamic'`
- All names must be **API names** — never display labels
- Alias (`AS`) valid in SELECT and ORDER BY only; echoed as response JSON key
- API credits: LIMIT 1–200 = 1 cr, 201–1000 = 2 cr, 1001–2000 = 3 cr
- Default ORDER BY is ascending by `id` — not `Created_Time`; supply explicit ORDER BY for chronological results
- → Full grammar details + pagination pattern: [coql-overview.dou.md](../assets/coql/coql-overview.dou.md)

## Field Type Comparators

| Field type | WHERE comparators |
|---|---|
| Text | `=` `!=` `like` `not like` `in` `not in` `is null` `is not null` |
| Picklist | `=` `!=` **only** — `in`/`not in`/`like` rejected at runtime; apply exclusion client-side |
| Lookup / MML / Roles & Profiles | `=` `!=` `in` `not in` `is null` `is not null` |
| Date / DateTime / Number | `=` `!=` `>=` `>` `<=` `<` `between` `not between` `in` `not in` `is null` `is not null` |
| Boolean | `=` only |
| Rollup Summary | same as Date/DateTime/Number |
| Formula → Decimal/Date/DateTime/Number | same as Date/DateTime/Number |
| Formula → String | same as Text |
| Formula → Boolean | `is null` `is not null` `equals` |
| Encrypted numeric | `=` `!=` `is null` `is not null` |
| Encrypted non-numeric | `is null` `is not null` only |

> `not like "%tech%"` (both ends) = not-contains; single-sided `%` with `not like` silently misbehaves.

→ Comparator matrix source + encrypted field rules: [coql-execute.dou.md](../assets/coql/coql-execute.dou.md)

## Lookup Fields & the `.` Operator

**Syntax:** `<lookup_field>.<target_field_api_name>` e.g. `Account_Name.Account_Name`

| SELECT expression | Response |
|---|---|
| `Account_Name` | `{ id, name }` of linked record |
| `Account_Name.Account_Name` | string value of that field |

| Usage location | JOIN type | Cap |
|---|---|---|
| WHERE / ORDER BY / GROUP BY / aggregate | Base JOIN | max **5** per query |
| SELECT only | SELECT column JOIN | max **15** per query |

- Two lookups → same module in WHERE = **2** Base JOINs; in SELECT only = **1** SELECT column JOIN
- Nested: first hop (`lookup1.lookup2`) always Base; second hop classification follows its clause
- Chain depth max **2**: `A.B.C` valid; `A.B.C.D` → `LIMIT_EXCEEDED`
- Module/field name collision: prefix module with `!` — `!Leads.Owner.role.id`
- Dotted paths in SELECT must be **unquoted** — `Account_Name.Account_Name` ✓; `'Account_Name.Account_Name'` returns the literal string for every row. Exception: aliased form `'Account_Name.Account_Name' AS 'Account Name'` is valid. 
- `->` operator: `What_Id->Accounts.Account_Name` — **Tasks / Calls / Events ONLY**; `Who_Id` is NOT filterable in WHERE
- → Full JOIN classification, nested JOIN rules, failure modes: [coql-joins.dou.md](../assets/coql/coql-joins.dou.md)

## Subqueries

- Valid in **WHERE only** — not SELECT / GROUP BY / ORDER BY / aggregate
- Max **5** subqueries per parent query
- Max **100 rows** per subquery — **silently truncates without error**; switch to JOIN if inner set > 100
- Exactly **1** SELECT column inside each subquery
- Multi-value operators: `IN`, `NOT IN` — accept up to 100 inner rows
- Single-value operators (`=` `!=` `<` `>` `<=` `>=` `BETWEEN` `NOT BETWEEN`) — subquery must return exactly **1** row
- Prefer JOIN when the inner field is also needed in SELECT / ORDER BY / GROUP BY
- → Subquery sequence, execution order, failure modes: [coql-subquery.dou.md](../assets/coql/coql-subquery.dou.md)

## MxN Fields & Subforms

- **MxN (Multi-Select Lookup)**: cannot reference the parent field directly — query via the auto-generated **linking module**; direct reference → `INVALID_QUERY: unsupported data type` (Kaizen #125)
- **Subform**: subforms are independent modules — query via the subform's **own module API name**; `.` traversal from parent is unsupported (Kaizen #124)
- → MxN linking-module rule, subform module name lookup: [coql-execute.dou.md](../assets/coql/coql-execute.dou.md)
- → Unsupported field types in WHERE: [coql-limitations.dou.md](../assets/coql/coql-limitations.dou.md)

## Hard Limits

- Max **2,000** records per call (LIMIT cap)
- Max **25** WHERE criteria
- Max **500** SELECT fields
- Max **5** Base JOINs per query
- Max **15** SELECT Column JOINs per query
- Max **5** subqueries per parent query
- Max **100** values in `in` / `not in` operator
- Total records per unique criteria (via pagination): **1,00,000**
- Max **10** ORDER BY fields
- Max **4** GROUP BY fields
- Max **5** aggregate columns per query
- Max **5** dynamic formula fields in SELECT
- Dot-traversal chain depth max **2** (`A.B.C.D` → `LIMIT_EXCEEDED`)
- → Full caps + unsupported field types: [coql-limitations.dou.md](../assets/coql/coql-limitations.dou.md)

## Validation Checklist

Before delivering a COQL query, verify:

- [ ] Module API name in `FROM` is correct (not display label)
- [ ] All field names in `SELECT` and `WHERE` use API names
- [ ] Both OAuth scopes included: `ZohoCRM.coql.READ` AND `ZohoCRM.modules.{module}.READ`
- [ ] `is null` / `is not null` used for null checks (not `= null` or `!= null`)
- [ ] Picklist fields in WHERE use only `=` or `!=` (not `in`, `not in`, `like`)
- [ ] For Queries Workbench COQL source: WHERE clause is present (required at runtime even when grammar marks it optional)
- [ ] Lookup fields in WHERE compare against linked record **`id`**, not display name (pre-fetch the id)
- [ ] MxN field → query via linking module, not parent field
- [ ] Subform → query via subform's own module API name, not parent `.` traversal
- [ ] `not like` uses `%` at **both** ends for not-contains; single-sided `%` silently misbehaves

## Critical Gotcha

### Dual OAuth scopes — both required

`ZohoCRM.coql.READ` alone → `OAUTH_SCOPE_MISMATCH` 401. Both of the following are required:
- `ZohoCRM.coql.READ`
- `ZohoCRM.modules.{module}.READ` (or `ZohoCRM.modules.ALL.READ`)

### `Who_Id` not filterable in WHERE

- `Who_Id` in WHERE → `SYNTAX_ERROR` / `INVALID_QUERY`; `->` applies to `What_Id` only (Tasks/Calls/Events)
- Alternative: `zoho.crm.getRelatedRecords` per parent record
→ [coql-joins.dou.md](../assets/coql/coql-joins.dou.md)

### Notes module — admin only

- Non-admin requests return empty / unauthorised with no error
- Gate behind an admin permission check
→ [coql-execute.dou.md](../assets/coql/coql-execute.dou.md)

## DOU Reference Nodes

| Task | Read This File |
|---|---|
| Understand COQL scope — syntax, modules, field API names, SELECT / FROM / WHERE / ORDER BY / LIMIT, pagination | [coql-overview.dou.md](../assets/coql/coql-overview.dou.md) |
| Execute a COQL query — endpoint, request/response shape, authentication, error codes | [coql-execute.dou.md](../assets/coql/coql-execute.dou.md) |
| COQL from Deluge (invokeurl body map, Workbench WHERE requirement) | [#deluge-usage](../assets/coql/coql-execute.dou.md#deluge-usage) |
| Traverse related-module fields via dot notation (implicit JOINs through lookup fields) | [coql-joins.dou.md](../assets/coql/coql-joins.dou.md) |
| Use nested subqueries in COQL | [coql-subquery.dou.md](../assets/coql/coql-subquery.dou.md) |
| Know COQL limits — record caps, unsupported constructs, field type restrictions | [coql-limitations.dou.md](../assets/coql/coql-limitations.dou.md) |
| Subform data access + MxN via linking module | [coql-execute.dou.md](../assets/coql/coql-execute.dou.md) |
