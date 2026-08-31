FILE_PURPOSE: Read when traversing related modules in a COQL `select_query` via the `.` lookup operator — Base JOIN vs SELECT-column JOIN classification and nested-JOIN behaviour.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/api/v8/COQL-Joins.html
TRIGGER_KEYWORDS: COQL JOIN, Base JOIN, SELECT column JOIN, lookup field, dot operator, nested join, Account_Name.Parent_Account, -> operator, What_Id->

TECHNICAL_CONSTRAINTS:
- COQL has no `JOIN` keyword. Joins are expressed by traversing a lookup field via the `.` (dot) operator (e.g. `Account_Name.Account_Name` traverses the `Account_Name` lookup on Contacts into the Accounts module).
- A lookup field traversal is classified into one of two JOIN kinds based on **where** it appears in the query:
  - **Base JOIN** — lookup traversal appears in `WHERE`, `ORDER BY`, `GROUP BY`, or inside an aggregate column. Example: `select id from Contacts where Owner.role is not null` (`Owner.role` is a Base JOIN).
  - **SELECT column JOIN** — lookup traversal appears **only** in the SELECT column list and nowhere else. Example: `select Owner.profile, Created_By.role from Contacts where id is not null`.
- Two distinct lookup fields pointing to the **same** target module are counted as **two separate JOINs** in Base JOIN classification (e.g. `Owner.role` + `Created_By.profile` both target Users → two Base JOINs).
- The same disjoint-lookups rule does **not** apply to SELECT column JOINs — COQL optimises and collapses multiple SELECT-only traversals into the same target module into a single JOIN. Example: `Owner.profile` + `Created_By.role` both targeting Users in SELECT only = one SELECT column JOIN.
- Nested JOINs (`lookup_field_1.lookup_field_2.field`) decompose as follows:
  - The first hop (`lookup_field_1.lookup_field_2`) is always a Base JOIN.
  - The second hop (`lookup_field_2.field`) is a Base JOIN if used in WHERE / ORDER BY / GROUP BY / aggregate, or a SELECT column JOIN if used only in the SELECT column.
- JOIN counts are capped by the Limitations page (see [coql-limitations.dou.md](./coql-limitations.dou.md)): max 5 Base JOINs per query, max 15 SELECT column JOINs per query.
- Relation chain *depth* is capped separately at 2 (`A.B.C` has chain depth 2) — see [coql-execute.dou.md](./coql-execute.dou.md) `LIMIT_EXCEEDED` failure mode ("more than two joins") and [coql-limitations.dou.md](./coql-limitations.dou.md) for the explicit cap.
- Response payload for a lookup traversal — bare `Account_Name` returns `{id, name}` of the linked record; `Account_Name.Account_Name` returns the linked record's `Account_Name` field value (string).
- Lookup traversal in SELECT requires the linked field's API name; without it, only the linked record's `id` returns (see [coql-execute.dou.md](./coql-execute.dou.md)).
- The User lookup target's display field is `last_name` (not `name`) — `Owner.last_name` returns the owner's last name string.
- Roles & Profiles sub-traversal: `Owner.role.id` / `Owner.role.name` / `Owner.profile.id` / `Owner.profile.name` are the documented sub-fields off a user lookup's role / profile.
- Multi-Module Lookup (`What_Id`) traversal uses the `->` operator to disambiguate the target module: `What_Id->Accounts.Account_Name` (Tasks / Calls / Events only).
- Self-referential lookups are supported and traversable — e.g. `Parent_Account` on Accounts points to Accounts; `Account_Name.Parent_Account.Account_Name` (Contacts → Accounts → Accounts) is a valid two-relation chain.
- Source-documented silent behaviour for chains > 2 relations: per the Limitations page, "If you use more than two relations in a select query, system validates only the last two relations" — i.e. the parser does NOT error on depth-3+ chains; it silently drops validation of all but the last two. This contradicts the Get-Records error catalog's `LIMIT_EXCEEDED` for "more than two joins." 

REQUIRED_PARAMETERS:
- Lookup-traversal syntax in SELECT: `<lookup_field_api_name>.<target_field_api_name>` (e.g. `Account_Name.Account_Name`).
- Nested traversal syntax: `<lookup_1>.<lookup_2>.<field>` (max chain depth 2 — i.e. at most three dot-segments including the base field).
- Base-JOIN-in-WHERE example: `select id from Contacts where Owner.role is not null`.
- SELECT-column-JOIN example: `select Owner.profile, Created_By.role from Contacts where id is not null`.
- Two-hop projection example: `select Last_Name, Account_Name.Parent_Account, Account_Name.Parent_Account.Account_Name from Contacts where Last_Name is not null and Account_Name.Parent_Account.Account_Name is not null`.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- Chain depth > 2 in a single traversal (e.g. `A.B.C.D`): `LIMIT_EXCEEDED` 400 (`The query has more than two joins`) — collapse via intermediate query or subquery (see [coql-subquery.dou.md](./coql-subquery.dou.md)).
- Total Base JOIN count exceeds 5 per query (multiple lookup fields used in WHERE / ORDER BY / GROUP BY / aggregate, including same-target same-field duplicates which count separately): `LIMIT_EXCEEDED` 400 — consolidate or split the query.
- Total SELECT column JOIN count exceeds 15 per query: `LIMIT_EXCEEDED` 400 — partition the projection across multiple queries.
- Two lookup fields pointing to the same target module in WHERE (e.g. `Owner.role` + `Created_By.profile`) misjudged as one JOIN: each counts toward the Base JOIN cap of 5 — audit the per-clause join count, not the per-module count.
- Lookup field returned in SELECT without a `.` traversal: response carries only `{id, name}` of the linked record — caller wanting other linked fields must restate the lookup with the desired path.
- Author confuses Base JOIN vs SELECT column JOIN classification when a lookup appears in **both** SELECT and WHERE: the WHERE usage promotes the field to a Base JOIN, consuming the Base JOIN budget — count joins per (lookup-field, target-module) pair, scoped to the most-restrictive clause it appears in.
- Mixed-module same-target lookups optimised in SELECT but not in WHERE: SELECT shows one logical JOIN, WHERE shows two — caller's mental model breaks when the same query body shifts a lookup between SELECT and WHERE without re-counting.
- Nested traversal where the second hop's target is itself a lookup that the caller assumes is auto-resolved to its display name: only Lookup / User Lookup return display names (per [coql-execute.dou.md](./coql-execute.dou.md)); Consent Lookup and MML return only `id`.
- Query author relies on the same `.`-path appearing twice in SELECT to deduplicate as one JOIN: SELECT-column-JOIN collapsing only applies when both traversals target the **same module** — different-target same-syntax does not collapse.
- Owner / Created_By / Modified_By join cap exhaustion when querying many user-side attributes: each distinct `<user-lookup>.<field>` in WHERE is its own Base JOIN — pre-fetch user metadata via Users module and avoid join inflation.
- WHERE-only Base JOIN to a module the user lacks read access to: source Limitations only states scope is required for the **base** module; behaviour when only a JOINed-to module's scope is missing is undocumented.
- Author writes `<lookup_field>` alone in SELECT expecting all linked fields to inline: only `{id, name}` returns — every linked field needed in the response requires its own `<lookup>.<field>` path entry.
- Dotted traversal across an inactive / archived lookup target module: COQL returns nulls for the inner field path with no error — verify both modules are active before composing the join.
- Same lookup field traversed in both SELECT and ORDER BY of the same query: counts as one Base JOIN (ORDER BY usage promotes it from SELECT-column to Base) — budget against the Base cap, not the SELECT-column cap.
- Lookup field traversal where the lookup is itself stored as `null` on a parent row: the traversed path returns `null` rather than excluding the row (no implicit inner-join semantics) — filter `<lookup> is not null` in WHERE to drop null-parent rows.
- Author conflates module API name with field API name in a dotted path (`Leads.Owner.role.id` where `Leads` collides with a field): query rejected — prefix the module reference with `!` (`!Leads.Owner.role.id`).
- Aggregate function over a dotted-traversal field (`SUM(Account_Name.Annual_Revenue)`): the lookup becomes a Base JOIN and the aggregate target must be a numeric type per [coql-execute.dou.md](./coql-execute.dou.md) — both constraints apply simultaneously.
- Single-quoted dotted traversal path in SELECT without an alias (`SELECT 'Account_Name.Owner' FROM Contacts`): COQL interprets the quoted value as a string literal rather than a field path — the response returns the literal string `"Account_Name.Owner"` for every row, or the request fails with a gateway-level 502. Dotted traversal paths in SELECT must be **unquoted** unless they form part of an aliased projection (`'Account_Name.Owner' AS 'owner'`). Always follow the unquoted form shown in the SELECT-column-JOIN examples above.
- `Who_Id` (the Name / Contact polymorphic field on Tasks, Calls, and Events) is not filterable in COQL WHERE under any form — `->` traversal raises `SYNTAX_ERROR`, and `IN (subquery)` raises `INVALID_QUERY: subquery return more than one values which is incompatible for the operator`. The `->` operator is documented only for `What_Id`; do not assume symmetric support for `Who_Id`. Use `zoho.crm.getRelatedRecords` per parent record as the alternative when Activities must be filtered by a linked Contact's attributes.
