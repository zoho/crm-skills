FILE_PURPOSE: Read when choosing a Query Source / Type — Module, COQL, Zoho CRM REST API, REST API, External Database, Cloud Database — and configuring the SQL-source Advanced settings.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/queries/query-types.html, queries-overview.dou.md
TRIGGER_KEYWORDS: CRM Module, COQL, Zoho CRM REST API source, REST API source, External Database, Cloud Database, SSL, Trusted Domains, Read Only, Connection Timeout

TECHNICAL_CONSTRAINTS:
- Six Source families — two pre-defined CRM (**Module**, **COQL**), one pre-defined utility (**Zoho CRM REST API**, metadata only, current-user auth), three custom (**REST API**, **External Database** = MySQL / MicrosoftSQL / PostgreSQL, **Cloud Database** = Amazon RDS / Google Cloud Platform / Microsoft Azure).
- **Module** source: pick one module + up to 2 related-module lookups + up to 50 fields; supports Subforms; criteria modes `None` / `Criteria` / `Record ID`; single `Order by` axis ascending or descending.
- **COQL** source: SELECT-style body authored inline; cross-module lookup traversal supported via dotted notation; full COQL grammar lives in the v8 COQL endpoint reference (`Get-Records-through-COQL-Query`).
- **Zoho CRM REST API** source: built-in, no Connection / OAuth needed; targets metadata endpoints (`/settings/fields`, `/settings/layouts`, `/users`, profiles, pipelines, related-list settings, etc.); supports `GET`, `POST`, `PUT`, `DELETE`, `PATCH`; **cannot** invoke external hosts; module / COQL paths are discouraged here for record reads — use Module / COQL sources for better performance.
- **REST API** custom source: enter base URL, default headers, default parameters, **Connection** (created in `Setup → Developer Hub → Connections` for auth); host must be in **Trusted Domains** unless it is an IP literal.
- **External Database** / **Cloud Database** source: enter Name, Host, User Name, Password, Database Name, Schema, optional Port; SQL is authored against the connected store; per-org cap 5 SQL sources.
- Advanced Configuration (SQL sources only) — four knobs: **Use SSL**, **Time Zone**, **Connection Timeout** (seconds), **Read Only**.
- `Use SSL` encrypts and validates server certificate + hostname; **hostname verification works only with DNS names** — IP-literal hosts establish an encrypted but unverified connection.
- Adding a host to **Trusted Domains** bypasses both hostname and certificate validation on that host — admin-managed; treat each entry as an explicit security exception.
- **`Use SSL` cannot be modified after the source is successfully created** — set the SSL flag (and any Trusted-Domains-bypass dependency) correctly on first save; changing it later requires re-creating the source.
- `Read Only` **is** editable post-creation; when enabled the source rejects `INSERT` / `UPDATE` / `DELETE` and accepts `SELECT` only.
- Time-zone behaviour: read converts source-stored timestamps into the consumer user's timezone; write uses the supplied ISO 8601 zone, falling back to the consumer user's zone, falling back to source-side zone. Date-only values are never converted. Timestamps in columns typed `timestamp with time zone` (or equivalent) bypass conversion.
- Users with Developer Permissions can access every SQL source in the org — superuser-credentialed sources expose privileged data to any developer.
- Source / Type **is changeable** on an existing Query via `Configuration → Change` — switching wipes the type-specific configuration block, and the Schema / Variables must be re-validated.

REQUIRED_PARAMETERS:
- Module type: `{ Module, Related_Module[]?: ≤2, Fields[]: ≤50, Criteria | Record_ID | None, Order_by?, Order_direction? }`.
- COQL type: `{ select_query: string }` — body matches the v8 COQL grammar (API-named columns, dotted lookups, parenthesised criteria).
- Zoho CRM REST API type: `{ method: GET|POST|PUT|DELETE|PATCH, path: '/{api_version}/...', headers?, params?, body? }`.
- REST API custom type: `{ method, endpoint, headers?, params?, body?, connection_link_name }`; base URL inherited from the Source.
- SQL source create form: `{ Name, Host, User_Name, Password, Database_Name, Schema?, Port?, Advanced: { Use_SSL?, Time_Zone?, Connection_Timeout_seconds?, Read_Only? } }`.
- See [queries-limits.dou.md](./queries-limits.dou.md) for SELECT / INSERT / UPDATE / DELETE grammar caps that apply to SQL sources.

UI_ONLY_ACTIONS:
- Add a SQL source: `Setup → Developer Hub → Queries → Sources tab → Create Source → choose MySQL / MicrosoftSQL / PostgreSQL / Amazon RDS / Google Cloud Platform / Microsoft Azure → fill credentials + Advanced → Validate and Save`. Note: No API equivalent — UI-only.
- Add a REST API source: `Setup → Developer Hub → Queries → Sources tab → Add Source → REST API → Name + Base URL + default Headers / Params → Connection (existing or new) → Save`. Note: No API equivalent.
- Add a host to Trusted Domains so SQL / REST sources can resolve it: `Setup → Developer Space → Trusted Domains`. Note: bypass is per-host; audit regularly.
- Switch Source / Type on an existing Query: open the Query → `Configuration → Change` → pick new type. Note: prior type-specific config is wiped — confirm before saving.

CRITICAL_FAILURE_MODES:
- `Zoho CRM REST API` source pointed at an external host (`https://api.example.com/...`): silently rejected — the source is metadata-only against the current org; use a `REST API` custom source instead.
- Module type `Fields` populated by display label instead of API name in the Schema editor: Path entries break on locale change — keep Path keyed on API name. (label-vs-api-name)
- Module type with more than 2 related modules selected: extra picks are ignored silently — cap is hard at 2.
- COQL body addressing a module / field by display label (`"Last Name"`, `"Deal"`): `INVALID_QUERY` from the server — use API names (`Last_Name`, `Deals`). (label-vs-api-name)
- COQL body uses `SELECT *`: rejected — must enumerate columns (see [queries-limits.dou.md](./queries-limits.dou.md)).
- SQL source created with superuser credentials: every Developer-permissioned user in the org can author queries against that source — restrict the DB account to least privilege before saving.
- SSL enabled while Host is an IP literal: connection encrypts but hostname is not verified, MITM detection is reduced — replace with DNS name and re-validate.
- `Use SSL` flag set incorrectly on first save (off when it should be on, or on with a Trusted-Domains bypass that was not intended): **cannot be amended in place** — the source must be deleted and re-created; all dependent Queries re-point or rebuild.
- Host added to Trusted Domains as a one-off and never reviewed: stale exception persists indefinitely — audit `Setup → Developer Space → Trusted Domains` regularly.
- Time-zone column typed as `timestamp` (no tz) in the source DB while caller expects org-default zone: query returns ambiguous timestamps — switch source-side column to `timestamp with time zone`, or set source `Time Zone` to match the DB session's zone.
- `Connection Timeout` left at the platform default for a slow on-prem DB: queries `ApiError` mid-execution — raise timeout per source after measuring real RTT.
- `Read Only` cleared accidentally on a production-mirror source: developer queries now mutate prod data — flip back to read-only and audit recent INSERT / UPDATE / DELETE through DB logs.
- REST API source's Connection's OAuth refresh-token expired: queries return 401 with no Workbench-side warning — admin re-authorizes under `Setup → Developer Hub → Connections`.
- `Zoho CRM REST API` source used to fetch large record lists: documented as performance-suboptimal — switch to Module or COQL for record retrieval.
- Source / Type changed mid-edit then Save: per-type configuration cleared — rebuild from scratch, do not assume retention.
- COQL body authored with sub-queries: SQL-source caps apply (see [queries-limits.dou.md](./queries-limits.dou.md)) — sub-queries are not supported anywhere.
- SQL source `Schema` field left blank for PostgreSQL: queries resolve against the role's `search_path` default — pin the schema name explicitly to avoid table-not-found surprises.
- REST API source missing the host from Trusted Domains: every execution rejects with "host not trusted" — add the host once before saving the source.
- Cloud-DB source with read-only privileges granted at the DB but `Read Only` flag left off in CRM: writes are blocked by the DB anyway, but error surfaces only after the Workbench attempts INSERT — set the `Read Only` flag in CRM to surface the constraint upstream.
