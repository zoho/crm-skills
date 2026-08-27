# Queries Subskill (Workbench — UI-Only)

> **UI-only** — no API to create, edit, or delete a Query; all authoring at `Setup → Developer Hub → Queries`. For programmatic queries, use [COQL](./coql.md). DOU nodes are authoritative — see [DOU Reference Nodes](#dou-reference-nodes).

**Queries** in Zoho CRM is a saved-query builder. You configure a data source, author the query body, define `{{Variable_Name}}` placeholders, map a response schema, and bind the result to a **Canvas view, Kiosk, or Custom Related List**. The query runs at render time — it cannot be invoked directly via a raw REST call against an arbitrary SQL string.

---

## Execution Instructions

1. Read the DOU nodes for Query associations, variable mapping, and DML constraints.
2. All authoring is done in the CRM Workbench UI (`Setup → Developer Hub → Queries`) — there is no API to create or edit a Query programmatically.
3. Provide the numbered UI creation and association steps.
4. Include the source type, query body, `{{Variable_Name}}` declarations, and association configuration.
5. If the source type is COQL, also open [coql.md](./coql.md).
- **Validation**: every `{{Variable}}` is declared in the query body and mapped at each association point; Schema return type (Map vs Table) matches the placement type.

## Critical Gotchas

### Variable token mismatch returns over-broad result with no error

Queries use `{{Variable_Name}}` tokens in their COQL body, criteria, or endpoint. When invoking from Deluge via `zoho.crm.invokeQuery`, the caller's variable map must use the **exact same key names** — case-sensitive. A mismatched or missing key resolves to an empty string; the query still executes and returns a result set broader than intended.

```deluge
// Workbench COQL body: SELECT id, Last_Name FROM Leads WHERE Lead_Status = '{{Status}}'
// Wrong — token name casing mismatch
args = {"status": "Open"};
// Right — matches the {{Status}} declaration exactly
args = {"Status": "Open"};
result = zoho.crm.invokeQuery("myQueryApiName", args);
```

**Rule**: Validate variable names against `Setup → Developer Hub → Queries → {query} → Variables` (match the `{{Variable_Name}}` tokens in the query body exactly, including case) before invoking from Deluge.

## When to Use Queries

| Goal | Use |
|------|-----|
| Display data in a Canvas record / list view | **Queries** → bind to Canvas |
| Drive a Kiosk screen or decision step with CRM data | **Queries** → bind to Kiosk |
| Populate a Custom Related List on a record | **Queries** → bind to Custom Related List |
| Query CRM data from code, Deluge, or an external API | **COQL** (`POST /crm/v8/coql`) — see [coql.md](./coql.md) |
| Query an external MySQL / PostgreSQL / cloud DB from a CRM placement | **Queries** with an External / Cloud Database source |

> For COQL vs Queries comparison, see [coql.md](./coql.md).

## How to Create a Query (UI Steps)

1. Go to `Setup → Developer Hub → Queries`.
2. Click **Create Query** → enter **Query Name** and **API Name**. The API Name is the key used by Deluge callers and Canvas/Kiosk associations — **keep it stable after creation; renaming breaks all associations**.
3. Click **Next** → choose a **Source** (see source descriptions below).
4. Configure the source body. Use `{{Variable_Name}}` tokens anywhere in the body, endpoint, headers, or criteria for runtime-bound values.
5. Click **Execute Query** to test → inspect the response shape.
6. Click **Save**.
7. Associate the saved Query with a UI placement (see [queries-associating.dou.md](../assets/queries/queries-associating.dou.md)):
   - **Canvas**: `Setup → Customization → Modules and Fields → {Module} → Canvas → {View} → Queries panel → Associate Query → map {{Variables}} to CRM fields`
   - **Kiosk**: `Setup → Customization → Kiosk → {Kiosk} → Edit → Screen → Get data via Queries → map {{Variables}}`
   - **Custom Related List**: open a record → three-dot menu → `Add Related List → Queries → map {{Variables}} to merge fields`

> **Variable mapping**: every `{{Variable_Name}}` declared in the query body must be explicitly mapped at **each** association point. Unmapped variables resolve to an empty string at runtime.

## Source Types

| Source | What it queries | SQL / COQL authored in |
|--------|----------------|------------------------|
| **Module** | CRM module records (up to 2 related lookups, up to 50 fields) | UI dropdowns — no SQL written |
| **COQL** | CRM module records via COQL SELECT body | Inline text editor (see [coql.md](./coql.md) for syntax) |
| **Zoho CRM REST API** | CRM metadata endpoints (`/settings/fields`, `/users`, etc.) | URL + method + params (UI) |
| **REST API** | Any external HTTP endpoint (requires a saved Connection) | URL + method + headers + body (UI) |
| **External Database** | MySQL, MicrosoftSQL, PostgreSQL | SQL body in UI (see SQL Limits below) |
| **Cloud Database** | Amazon RDS, Google Cloud SQL, Microsoft Azure SQL | SQL body in UI (see SQL Limits below) |

## SQL Constructs (External / Cloud Database Sources Only)

> SQL is only written when the Query source is **External Database** or **Cloud Database**. For CRM module data, use the **Module** or **COQL** source types instead — no SQL is written for those. For supported constructs and limits, see [SQL limits](https://www.zoho.com/crm/developer/docs/queries/sql-limits.html).

## Pagination (External / Cloud Database Sources Only)

> Applies to SQL sources only. CRM Module and COQL sources return one result set per render; pagination is controlled by the COQL LIMIT clause or Module source criteria.

Use `LIMIT` and `OFFSET` to paginate:
- `LIMIT 100 OFFSET 0` — first page
- `LIMIT 100 OFFSET 100` — second page
- Maximum `LIMIT` per query: **100 rows** (hard cap — values above 100 are silently clamped to 100)
- MicrosoftSQL: use `OFFSET n ROWS FETCH NEXT m ROWS ONLY` instead of `LIMIT`

## Limitations

- **UI-only authoring** — no API exists to create, update, or delete a Query programmatically
- **CRM Module and COQL sources are read-only** — no INSERT, UPDATE, DELETE through them
- **External / Cloud Database sources** support writes only when the source's **Read Only** flag is off
- **SQL sources hard-cap at 100 rows** per execution (LIMIT > 100 is silently clamped); `SELECT *` is rejected; sub-queries are not supported; max 5 JOINs, 50 columns, 50 WHERE/GROUP BY/ORDER BY conditions
- Module names, field names, and `{{Variable_Name}}` tokens must use **API names** (case-sensitive), not display labels
- **API Name changes break all associations** — Canvas, Kiosk, and Custom Related List bindings silently orphan; keep the API Name stable after deployment
- Each Query is org-scoped; sandbox and production environments are independent — re-create per environment
- For programmatic CRM data queries, use **COQL** ([coql.md](./coql.md)) — not this Workbench feature

## DOU Reference Nodes

Distilled Operational Understanding nodes for the Queries primitive — read the relevant file before authoring or invoking a native CRM Query.

| Task | Read This File |
|---|---|
| Scope a Query — Workbench, the five components (Source, Query, Variables, Schema, Serializer), Map vs Table return type, Setup entry | [queries-overview.dou.md](../assets/queries/queries-overview.dou.md) |
| Pick a Source / Type (Module, COQL, Zoho CRM REST API, REST API, External DB, Cloud DB) and configure SSL / Time Zone / Connection Timeout / Read Only | [queries-types.dou.md](../assets/queries/queries-types.dou.md) |
| Associate a Query with Canvas (Record / List), Kiosk (Screen / Decision), or Custom Related List — variable mapping and View Associations audit | [queries-associating.dou.md](../assets/queries/queries-associating.dou.md) |
| Gate a SQL-source Query by edition / source caps, SELECT / DML grammar rules, supported SQL functions, and the ISO 8601 contract | [queries-limits.dou.md](../assets/queries/queries-limits.dou.md) |
