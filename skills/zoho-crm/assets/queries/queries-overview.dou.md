FILE_PURPOSE: Read when scoping a Zoho CRM Query — Workbench, the five Query components (Source, Query, Variables, Schema, Serializer), and the Setup entry point.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/queries/, https://www.zoho.com/crm/developer/docs/queries/faqs.html
TRIGGER_KEYWORDS: Queries, Query Workbench, Developer Hub, Sources, Schema, Serializer, query variables, crmAPIResponse, Manage Schema

TECHNICAL_CONSTRAINTS:
- Authoring surface is the Query Workbench — a single Setup window that holds Source selector + configuration + variables + schema + serializer + execution panel. No API documented for create / update / delete of a Query.
- A Query has five components: **Source** (data provider), **Query** (configuration), **Variables** (runtime placeholders), **Schema** (response field map), **Serializer** (JavaScript response-rewrite hook).
- Source decides execution mode: CRM Module → CRM record fetch; COQL → SQL-like CRM query; Zoho CRM REST API → metadata endpoints under current user's session; REST API custom source → external HTTP; database / cloud-database source → direct SQL (see [queries-types.dou.md](./queries-types.dou.md)).
- `Zoho CRM REST API` source uses the logged-in user's session for auth — no extra OAuth or Connection config; external APIs **cannot** be invoked through this source.
- Schema is auto-generated on first execution; editable via `Manage Schema` (Path, CRM Field Type, Label) on the Query's three-dot menu.
- Schema return type is **Map** (single record / key-value) or **Table** (multi-record) — chosen implicitly by query shape; Canvas single-field associations require Map.
- Variables use the syntax `{{Variable_Name}}` — case-sensitive token replacement at runtime; supported in COQL bodies, REST endpoints, parameters, headers, request bodies, and Module criteria values.
- Query Variables are runtime-bound (per execution); distinct from org-wide CRM Variables which are static.
- Serializer is JavaScript invoked on the raw response; receives `result` and returns the rewritten payload — used for shape changes, lookup → `{id,name,module}` expansion, `href` injection for clickable cells, and `crmAPIResponse` envelope unwrapping when a REST-API-enabled Function backs the Query.
- Each Query is org-scoped; sandbox vs production are independent — re-create per environment.
- See [queries-types.dou.md](./queries-types.dou.md) for source / type combinations, [queries-associating.dou.md](./queries-associating.dou.md) for runtime placements, [queries-limits.dou.md](./queries-limits.dou.md) for caps.

REQUIRED_PARAMETERS:
- Query create-pop-up fields: **Query Name** (display), **API Name** (slug used by associations and Deluge `zoho.crm.invokeQuery` callers), **Source / Type**, type-specific configuration block (Module + Fields + Related Module for Module type; COQL body for COQL; HTTP verb + endpoint + headers + params + body for REST API types).
- Module query caps: max **2 related-module lookups** in `Related Module` drop-down, max **50 fields** in `Fields` drop-down.
- Criteria modes: `None`, `Criteria` (field-comparator expression with AND / OR groups; values literal or `{{Variable}}`), `Record ID` (single-record filter; variable-bindable).
- Advanced sort: `Order by` field + ascending / descending; single sort axis only.
- Variable declaration: `{{Variable_Name}}` inside any string-typed config slot (COQL body, REST URL, header, parameter, body, criteria value).
- See [queries-limits.dou.md](./queries-limits.dou.md) for COQL / SQL grammar caps.

UI_ONLY_ACTIONS:
- Open the Workbench: `Setup → Developer Hub → Queries`. Note: No API equivalent — UI-only.
- Create a Query: `Setup → Developer Hub → Queries → Create Query → fill Name + API Name → Next → choose Source → configure → Execute Query → Save`. Note: No API equivalent.
- Edit response schema: `Setup → Developer Hub → Queries → hover Query → three-dot icon → Manage Schema → edit Path / CRM Field Type / Label → Save`. Note: No API equivalent.
- Inspect runtime placements: `Setup → Developer Hub → Queries → three-dot icon → View Associations` lists every Canvas / Kiosk / custom related list bound to the Query. Note: No API equivalent.
- Add a Source: `Setup → Developer Hub → Queries → Sources tab → Add Source` (REST API or SQL); host must be on **Trusted Domains** when not an IP literal — see [queries-types.dou.md](./queries-types.dou.md) for the four Advanced-Configuration knobs.

CRITICAL_FAILURE_MODES:
- Query API Name renamed after Canvas / Kiosk / related-list associations exist: every association breaks silently — keep API Name stable; rename via duplicate-and-rebind. (label-vs-api-name)
- Variable token mis-cased in caller (`{{record_id}}` while the Query declared `{{Record_ID}}`): runtime substitution drops to empty string — token names are case-sensitive verbatim.
- COQL / Module query body referencing a CRM field by its display label (`"Last Name"`) instead of API name (`Last_Name`): runtime returns `INVALID_QUERY` / empty rows. (label-vs-api-name)
- Schema not regenerated after the source's response shape changes: associated Canvas / Kiosk component renders blank cells — re-execute the Query and re-save schema after every upstream change.
- Schema edited to a `CRM Field Type` that does not match the actual JSON value type (e.g. labelled `int` while server returns string): consumer rendering fails or coerces silently — keep type and Path in sync with the real response payload.
- Serializer JavaScript throwing an unhandled exception: Query execution returns the raw response without serialization and downstream consumer sees the un-shaped payload — wrap risky code in try / catch and `return result` as the fallback.
- Serializer reads `crmAPIResponse` directly without checking for its presence: function-backed Queries return the envelope, native sources do not — branch on `typeof crmAPIResponse !== 'undefined'`.
- Query author confuses `Zoho CRM REST API` (built-in metadata source) with a custom REST API Source: trying to call `https://api.example.com` through the built-in source fails — switch to a custom `REST API` Source (see [queries-types.dou.md](./queries-types.dou.md)).
- Variable declared in the body but not mapped at the consumer (Canvas / Kiosk variable mapping skipped): runtime resolves to empty string and downstream criteria misfire — every declared `{{var}}` must be mapped at every association point.
- `View Associations` shows a stale binding for a Query that was deleted-and-recreated under the same API Name: each association must be re-saved after delete-and-recreate; auto-rebind is not guaranteed.
- Schema return type mismatched to placement: Table-shape returned to a Canvas single-field slot → rendering error; Map-shape returned to a List View Canvas → only first record renders (see [queries-associating.dou.md](./queries-associating.dou.md)).
- Source / Type changed mid-edit without re-validating the Schema and Variables: residual Path entries point at a JSON shape that no longer exists — re-execute and re-save Schema after every Source change.
- Trusted Domains bypass enabled for an SSL-required SQL host because the user passed an IP: SSL hostname verification is silently skipped and the connection downgrades to "encrypted but unverified" — prefer DNS names; add to Trusted Domains only when no alternative exists (see [queries-types.dou.md](./queries-types.dou.md)).
- Query backed by a REST-API-enabled Function expects automation to fire under the caller's profile: the Function runs under its own configured user — record visibility differs from the Query consumer's. (automation-interaction)
- Writing back through a Query that targets a CRM Module Source: not supported — CRM Module / COQL / Zoho CRM REST API sources are read-only at the Query layer; mutations require the v8 CRM API directly.
- Connection-backed REST API Source whose underlying OAuth token expires: every binding 401s with no Workbench-side health indicator — re-authorize the Connection under `Setup → Developer Hub → Connections` and re-execute associations.
- Query deleted from the Workbench without first opening `View Associations`: every Canvas / Kiosk / Custom-Related-List binding is orphaned with no automatic notification — always audit `three-dot icon → View Associations` before delete (documented in `queries/index.html` → View Associations of a Query).
