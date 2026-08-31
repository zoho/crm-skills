FILE_PURPOSE: Read when nesting `SELECT` statements inside a COQL WHERE clause as an alternative to JOINs — subquery operators, execution sequence, the 100-row-per-subquery cap, and the 5-subqueries-per-parent cap.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/api/v8/COQL-subquery.html
TRIGGER_KEYWORDS: COQL subquery, nested SELECT, IN subquery, BETWEEN subquery, subquery sequence, parent query, outer query

TECHNICAL_CONSTRAINTS:
- A subquery is a nested SELECT inside a parent ("outer") query's WHERE clause; result rows feed the outer query at evaluation time.
- Subqueries are valid **only** inside the WHERE clause — never in SELECT, FROM, GROUP BY, ORDER BY, or aggregate columns.
- A single parent query accepts **at most 5 subqueries** (including nested-inside-subquery uses).
- A subquery returns **at most 100 rows**, with two distinct overflow behaviours by composition:
  - Subquery **without** an explicit LIMIT and underlying selection > 100 rows: silently truncated to the first 100 (per source's Subquery-vs-JOIN scenario where 400 matching accounts → only the first 100 are used → only 350 contact rows returned). No error raised.
  - Subquery **with** an explicit LIMIT > 100: `LIMIT_EXCEEDED` 400 ("The subquery retrieves more records than the allowed limit") per source error catalog.
  - For > 100 matching rows in either case, switch to a JOIN (see [coql-joins.dou.md](./coql-joins.dou.md)).
- Each subquery's SELECT column count is exactly 1 — multi-column subqueries are rejected with `INVALID_QUERY` 400.
- Supported subquery operators split into two groups:
  - **Multi-value operators**: `IN`, `NOT IN` — accept the full subquery result set as operands.
  - **Single-value operators**: `=`, `!=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `NOT BETWEEN` — require each operand subquery to return exactly one row.
- `BETWEEN` / `NOT BETWEEN` with subquery operands: each side (lower bound + upper bound) is evaluated independently; either side that returns more than one row fails the query.
- BETWEEN operands accept mixed subquery + literal pairs: e.g. `between (select Created_Time from Leads where id is not null Limit 1) and '2024-09-25T23:59:59+05:30'`.
- **Subquery sequence** — every subquery is assigned a zero-based execution sequence: independent subqueries execute first in declaration order; dependent subqueries wait for their dependency's sequence to complete and execute after.
- A subquery itself accepts a nested subquery; the inner subquery executes first and is assigned an earlier sequence number than the outer subquery that depends on it.
- Subqueries are JOIN-substitutes only when the lookup-inner-field appears **only in WHERE**. If the inner field is also needed in SELECT / ORDER BY / GROUP BY, fall back to a JOIN.
- Choice between subquery and JOIN for matching-row counts > 100: source explicitly recommends JOIN over subquery (subquery hits the 100-row cap and silently drops the remainder).
- A subquery references a lookup target module **once per WHERE clause** (e.g. `Account_Name in (select id from Accounts where ...)`) — replacing repeated dotted-traversals in the WHERE.
- A subquery's `LIMIT` clause is optional; when omitted, the 100-row cap still applies (the cap is implicit, not driven by LIMIT).
- Subquery WHERE clauses follow the same per-field-type comparator matrix as the outer query (see [coql-execute.dou.md](./coql-execute.dou.md)).
- A subquery's `SELECT` field must be a real field on the inner module — alias names from the outer query are out of scope inside the subquery.

REQUIRED_PARAMETERS:
- Subquery syntax skeleton: `<outer_field> <operator> (select <single_column> from <module> where <criteria> [LIMIT <offset>, <limit>])`.
- IN-subquery example: `select Lead_Source, Email from Leads where Contacts in (select id from Contacts where Email='patricia@mail.com')`.
- BETWEEN with two subquery operands: `select Last_Name from Leads where Created_Time between (select Created_Time from Leads where id is not null Limit 1) and (select Created_Time from Leads where id is not null limit 200,1)`.
- Nested-subquery example (parent → outer subquery → inner subquery): `select id from Vendors where id in (select id from Vendors where Vendor_Name like 'V%')` embedded inside `Vendor_Name in (...)` on the parent.
- Single-column constraint — every subquery's SELECT must contain exactly one field; never multi-select inside a subquery.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- `INVALID_QUERY` 400 — subquery placed in an unsupported clause (SELECT / FROM / GROUP BY / ORDER BY / aggregate). Resolution: move the subquery into WHERE.
- `INVALID_QUERY` 400 — subquery's SELECT contains multiple columns. Resolution: split into separate subqueries, each with one SELECT column.
- `INVALID_QUERY` 400 — single-value operator (`=`, `!=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `NOT BETWEEN`) paired with a subquery returning more than one row. Resolution: add `LIMIT 1` to the subquery or switch to `IN` / `NOT IN`.
- `LIMIT_EXCEEDED` 400 — more than 5 subqueries in a single parent query (counting nested subqueries). Resolution: consolidate or split across multiple API calls.
- `LIMIT_EXCEEDED` 400 — single subquery's LIMIT exceeds 100. Resolution: cap each subquery at 100; if more rows are required, switch to a JOIN.
- Subquery silently truncates at row 100 when the underlying selection has more matching rows AND no explicit LIMIT is set: outer query's row set is incomplete with no warning — pre-check the inner SELECT's `count` first, or switch to JOIN per the source's "use JOIN over subquery for > 100 records" guidance. Concrete source scenario: 400 accounts matching `Account_Name like 'A%'` with 1600 linked contacts → subquery returns 350 (first-100-accounts subset); JOIN equivalent returns all 1600.
- Author uses a subquery to filter on a lookup-inner-field that is also required in the SELECT projection: subquery semantics only filter — to project the inner field, supplement with the dotted traversal `<lookup>.<inner>` in SELECT and let the WHERE keep the subquery.
- Subquery sequence misunderstood — assuming declaration order is execution order when one subquery depends on another: independent subqueries fire first (in declaration order), then dependents — debug by mapping every `(<inner-subquery>)` reference to its enclosing subquery before predicting sequence.
- BETWEEN with one literal + one subquery operand whose subquery returns multiple rows: query rejected — restrict the subquery to exactly one row with `LIMIT 1`.
- Subquery used as the only filter on a high-cardinality lookup (`Account_Name in (select id from Accounts where Account_Name like 'A%')` against 400+ matching accounts): outer query returns only the rows linked to the first 100 accounts, silently dropping the rest — switch to JOIN (`Account_Name.Account_Name like 'A%'`) for full coverage.
- Same lookup field referenced both via dotted traversal in WHERE and via a subquery against the same target module: produces redundant work and inflates the JOIN count toward the 5-Base-JOIN cap — pick one expression form per (lookup, target) pair.
- Subquery's `from` module differs from the lookup field's target module: outer `IN` returns no rows (silent) — confirm the inner module matches the lookup target.
- Subquery returns zero rows under single-value `=` / `!=`: outer comparison resolves to false for every row → empty result set — branch on the inner subquery's expected cardinality before composing.
- Author uses BETWEEN's two-subquery form to express "between the first and last record" without sort-stable ORDER BY in the inner subqueries: row order is by `id` ASC default — supply explicit `ORDER BY` inside each operand subquery when the bounds depend on a custom axis.
- Nested-subquery dependency chain longer than two levels: source documents two-level dependency examples — deeper chains' execution order is undefined per source silence.
- `IN` subquery operand list exceeds 100 distinct values after expansion: hits the `in` / `not in` 100-value cap (see [coql-execute.dou.md](./coql-execute.dou.md)) — chunk values across multiple queries.
