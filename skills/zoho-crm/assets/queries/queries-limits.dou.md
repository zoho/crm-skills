FILE_PURPOSE: Read when authoring a SQL Source query against External / Cloud Database — edition caps, SELECT / INSERT / UPDATE / DELETE grammar caps, supported SQL functions, and the ISO 8601 date contract.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/queries/sql-limits.html
TRIGGER_KEYWORDS: SQL Limits, SELECT, INSERT, UPDATE, DELETE, LIMIT, OFFSET, ISO8601, sub-query, JOIN, GROUP BY, HAVING, edition caps

TECHNICAL_CONSTRAINTS:
- Edition-wise Query cap (per org): **Professional 100**, **Enterprise 250**, **Ultimate 500** Queries total across all Sources / Types.
- Source caps: **REST API sources** — 200 (Enterprise + Ultimate); **SQL sources** (External DB + Cloud DB combined) — 5 (Enterprise + Ultimate).
- `SELECT` allowed on **read-only and writable** sources; `INSERT` / `UPDATE` / `DELETE` allowed **only** on writable sources (Read Only flag off — see [queries-types.dou.md](./queries-types.dou.md)).
- `SELECT *` is **rejected** — explicit column list mandatory; column-count cap **50**.
- `LIMIT` is **mandatory on every SELECT** — if omitted, server applies a default of **100**; the maximum value caller can pass is also **100** (read cap is hard-bounded at 100 rows per execution).
- `OFFSET` paired with `LIMIT` is the documented pagination idiom; MicrosoftSQL uses `OFFSET n ROWS FETCH NEXT m ROWS ONLY` instead.
- Joins capped at **5** per query — count includes `INNER`, `LEFT`, `RIGHT`, `FULL`.
- `GROUP BY`, `ORDER BY`, `WHERE`, `HAVING` each cap at **50** items / conditions.
- **Sub-queries are not supported** in any SELECT / INSERT / UPDATE / DELETE — flatten via joins or stage with multiple Queries.
- Supported data types are **basic only**: numbers, strings, dates, timestamps. **JSON, XML, arrays** in columns are unsupported — rejected or coerced to strings.
- All date / timestamp literals must be **ISO 8601** — `2025-07-15T10:00:00` (with offset when applicable); other formats reject.
- `INSERT` and `UPDATE` must list columns explicitly — implicit column ordering is not accepted.
- Supported SQL functions (whitelist): `SUM()`, `COUNT()`, `AVG()`, `MIN()`, `MAX()`, `LOWER()`, `UPPER()`. Other DB-native functions execute only if they are syntactic identifiers the server treats as expressions.
- Non-conforming queries return a documented error message — surface it to the consumer rather than retrying.
- Per [queries-types.dou.md](./queries-types.dou.md), SQL queries execute under the configured source credentials, **not** the consumer user — Developer-permissioned users share that privilege.

REQUIRED_PARAMETERS:
- SELECT shape: `SELECT col1, col2, ... FROM table [JOIN ...] [WHERE ...] [GROUP BY ...] [HAVING ...] [ORDER BY ...] [OFFSET n] LIMIT m;` — LIMIT ≤ 100.
- INSERT shape: `INSERT INTO {table}(col1, col2, ...) VALUES (val1, val2, ...);` — explicit columns.
- UPDATE shape: `UPDATE {table} SET col1 = val1, ... WHERE col_a = val_a AND col_b = val_b;` — non-empty WHERE.
- DELETE shape: `DELETE FROM {table} WHERE col_a = val_a AND col_b = val_b;` — non-empty WHERE.
- Sample executable queries (PostgreSQL / MySQL form): canonical SELECT with `INNER JOIN`, `WHERE … BETWEEN`, `GROUP BY`, `HAVING`, `ORDER BY`, `OFFSET … LIMIT` (see source).
- Variables in any clause: `{{Variable_Name}}` — case-sensitive, resolved at execution by the consumer's variable mapping (see [queries-associating.dou.md](./queries-associating.dou.md)).

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- `SELECT *` authored anywhere: server rejects with explicit error — enumerate columns up to 50.
- LIMIT omitted: server silently caps to 100 rows; caller assumes full set and downstream consumer renders truncated data — always set explicit LIMIT.
- LIMIT > 100 passed: server clamps to 100 — paginate via OFFSET / FETCH NEXT for larger windows.
- Sub-query authored inside `WHERE col IN (SELECT ...)`: rejected — re-express as JOIN or stage with a prior Screen Query (Kiosk).
- Date literal `2025/07/15 10:00:00` or `15-Jul-2025`: rejected — convert to ISO 8601 (`2025-07-15T10:00:00`).
- Column typed `JSON` in source schema: query returns rejection or stringified blob — pre-flatten in the source DB view, do not rely on Queries to parse JSON.
- INSERT / UPDATE on a source whose `Read Only` flag is on: rejected — flip `Read Only` off intentionally (see [queries-types.dou.md](./queries-types.dou.md)) and audit.
- INSERT without explicit column list: rejected — list every column to be written.
- UPDATE / DELETE issued without a WHERE clause: behaviour is not documented in `sql-limits.html` and varies per source DB — always scope mutations with explicit predicates rather than relying on platform-side guardrails.
- 6th JOIN added during refactor: query rejects — collapse two joins via a DB-side view or split into staged Queries.
- 51st condition added to WHERE / GROUP BY / ORDER BY / HAVING: rejected — split the predicate or pre-aggregate in a source-side view.
- Use of `UNION`, `WITH` (CTEs), window functions: not in the documented supported set — verify per source before relying; assume rejection.
- Use of DB-native functions outside the seven-function whitelist (`SUM / COUNT / AVG / MIN / MAX / LOWER / UPPER`) without verification: rejection risk varies by source; test before deploy.
- COUNT(*) used in SELECT against a Module / COQL source (not SQL): unsupported there — these caps apply to **SQL sources only** (External DB + Cloud DB).
- ISO 8601 literal without timezone where the target column is `timestamp with time zone`: server interprets as the source `Time Zone` setting — pass full ISO 8601 with `Z` or `±HH:MM` to be explicit.
- Edition cap reached (Pro 100 / Ent 250 / Ult 500): Create-Query button silently rejects — audit `Setup → Developer Hub → Queries` to free a slot, or upgrade.
- SQL-source cap of 5 reached: New Source button rejects — consolidate environments or remove unused sources.
- REST-API-source cap of 200 reached: same rejection path — audit Sources.
- Boolean / bit columns assumed supported: source's response coerces to 0 / 1 — handle in Serializer rather than depending on a boolean primitive.
- Array column unboxed by hand inside a Serializer: rejected at execution before Serializer fires — flatten in a view at the DB.
- COUNT() applied to a non-selected column: column whitelisting cap still consumes a slot — the function call counts toward the 50-column cap as a select item.
- Hot retry loop on a rejected query: each retry counts toward DB connection budget — fix the grammar before re-executing.
- Sub-query masked as a JOIN to a derived table: still rejected by the parser — only direct tables (with optional alias) are accepted in FROM / JOIN slots.
- Mixing INSERT / UPDATE / DELETE inside a single Query body: each Query body executes one statement — split into separate Queries.
- Trailing semicolon vs no semicolon inconsistency across source DBs: PostgreSQL / MySQL tolerate both; MicrosoftSQL strict modes can reject — normalize per source.
