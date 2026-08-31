# Deluge Subskill

> DOU nodes are authoritative — see [DOU Reference Nodes](#dou-reference-nodes) below.

Deluge (Data Enriched Language for the Universal Grid Environment) is Zoho's **server-side scripting language** used in Zoho CRM for custom functions, workflow actions, blueprint transitions, scheduled functions, and integrations.

> Source: https://www.zoho.com/deluge/help/

---

## Execution Instructions

1. Load the DOU node for the relevant built-in or method — DOU signatures override anything in this file. If the needed DOU node is not listed in [DOU Reference Nodes](#dou-reference-nodes), you MUST open [deluge-index.md](../assets/functions/deluge/deluge-index.md) before generating code — do not use recalled knowledge for built-in signatures.
2. Use this file for: architecture defaults, cross-cutting gotchas, data-query routing table, and cross-primitive wiring table.
3. If this file and a DOU node conflict, **DOU wins**. Verify return type and parameters match DOU exactly.
4. Output the complete Deluge function code.
5. For all HTTP calls, always use `invokeurl` with a named Connection — do NOT use `invokeapi` unless the user explicitly requests it (see [connections.md](./connections.md) for Connection setup).
6. Verify syntax against the **Known Syntax Gotchas** section in this file before presenting.
7. If the function makes external API calls to Zoho CRM REST endpoints, also cross-reference [api.md](./api.md) for the correct endpoint, parameters, and response schema.

**Architecture defaults** (apply unless the user explicitly requests otherwise):
- External-facing entrypoints: use Standalone Function with REST + OAuth scope — avoid `apikey` (lower scope control).
- Cross-module data reads with filtering/aggregation: use COQL via `invokeurl` — not multiple per-record REST calls with in-memory post-processing.

## Validation Checklist

Before delivering the code, verify:

- [ ] Method signature matches DOU node (not inline example from this file)
- [ ] Parameter count and types match DOU exactly
- [ ] Return type matches the Quick Reference table in [functions-overview.dou.md](../assets/functions/functions-overview.dou.md) for the chosen category (`standalone` → `string` only; `validation_rule` → `map`; `automation`/`schedule`/`salessignals` → `void`)
- [ ] Namespace prefix matches function category (button., automation., schedule., etc.)
- [ ] All field/module API names verified (not display labels)
- [ ] Connection link names are actual, not placeholder names
- [ ] No deprecated methods (check Deprecations section of [SKILL.md](../SKILL.md))
- [ ] Verified against **Known Syntax Gotchas** preamble rules and 1–7 inline below
- [ ] For `today()` gotcha: check [now-today.dou.md](../assets/functions/deluge/built-in-functions/date-time/now-today.dou.md)
- [ ] For merge-variable trim gotcha: check [trim.dou.md](../assets/functions/deluge/built-in-functions/text/trim.dou.md)
- [ ] None of the Critical Gotchas below are present in the code
- [ ] If COQL is generated: `Who_Id` not used in COQL WHERE; `->` traversal operator applied only to fields with documented support (`What_Id` on Tasks/Calls/Events)

## Critical Gotchas

### `{"trigger":[]}` in a Function write silently suppresses ALL automation

Passing an empty `trigger` array to `zoho.crm.v8.updateRecord` / `zoho.crm.v8.createRecord` / `zoho.crm.v8.upsert` suppresses workflows, blueprints, approvals, and orchestration — with no warning. Many CRM bugs trace back to a copy-pasted `"trigger":[]` from an example.

```deluge
// To suppress only some automation, pass the explicit subset:
updateMap = Map();
updateMap.put("Last_Name", "Smith");
optionalMap = Map();
optionalMap.put("trigger", {"workflow"});
response = zoho.crm.v8.updateRecord("Leads", recordId, updateMap, optionalMap);
```

**Rule**: Pass an empty trigger list only when intentionally suppressing **all** automation. To run selected automations, build the Deluge list/collection literal explicitly, for example `optionalMap.put("trigger", {"workflow"});`.

### Workflow Function updating its trigger record loops until the daily-credit cap

A Workflow Function that calls `zoho.crm.v8.updateRecord` on the same record that triggered it re-fires the same workflow rule. The loop continues until either the daily Function-execution credit is exhausted or the record-update history quota is hit. By that point, the chain returns 429 silently into any upstream workflow that called it.

**Rule**: Either (a) guard the update behind a `last modified by` check that excludes the Function's own service user, or (b) maintain a custom boolean flag field (e.g. `Loop_Guard__c`) that the Function flips and the workflow rule checks.

## Function Signatures by Category

> For all 7 category boilerplate signatures, return types, argument-mapping rule, and brace format: read [functions-categories.dou.md](../assets/functions/functions-categories.dou.md).

- Every arg declared in a Deluge signature must be mapped to a CRM merge variable (e.g. `${Deals.Id}`) at the trigger's UI surface — unmapped args resolve to `null` at runtime with no error.
- `standalone.*` must always declare `string` return type — editor rejects `map`/`list`/`int`; use `.toString()` to return structured data.
- `validation_rule.*` message key max 100 characters — silently truncated or ignored if exceeded.

---

## Data Query from Deluge

| Need | Method | Details |
|------|--------|---------|
| Fetch records by ID or paginated list | `zoho.crm.v8.getRecords` / `getRecordById` | DOU: [get-records.dou.md](../assets/functions/deluge/integrations/zoho-crm/get-records.dou.md) (getRecords) / [get-record-by-id.dou.md](../assets/functions/deluge/integrations/zoho-crm/get-record-by-id.dou.md) (getRecordById); `getRecordById` invalid ID → `{"status":"failure"}` with no `code` key |
| Search records by field criteria | `zoho.crm.v8.searchRecords` | Single: `(<field>:<op>:<val>)`; compound: `((<f>:<op>:<v>) and (<f>:<op>:<v>))`; operators: `equals`, `starts_with`, `not_equal`; `not_equal` omits null-field records; max 10 criteria |
| Advanced queries (JOINs, aggregations, `>`, `<`, `between`) | COQL via `invokeurl` to `POST /crm/v8/coql` | DOU: [coql-execute.dou.md](../assets/coql/coql-execute.dou.md#deluge-usage) |
| Saved query bound to Canvas / Kiosk / Related List | `zoho.crm.invokeQuery(apiName, variableMap)` | See [queries.md](./queries.md) |
| Sub-records (Tasks, Notes, Activities) for a parent | `zoho.crm.v8.getRelatedRecords` + filter in Deluge | `Who_Id` cannot be filtered in COQL WHERE — use two-step pattern |

**Signatures and parameter order:**

| Method | Signature |
|---|---|
| `zoho.crm.v8.createRecord` | `(module, record_details, options_map, connection)` |
| `zoho.crm.v8.updateRecord` | `(module, record_id, record_value, options_map, connection)` |
| `zoho.crm.v8.upsert` | `(module, values, duplicate_check, connection)` — dup check: `{"duplicate_check_fields":{"Email"}}` |
| `zoho.crm.v8.getRecordById` | `(module, record_id, query_value, connection)` — `query_value` requires `"fields"` key |
| `zoho.crm.v8.getRecords` | `(module, query_value, page, per_page, connection)` — `page` before `per_page`; `"fields"` required in `query_value` |
| `zoho.crm.v8.searchRecords` | `(module, criteria, page, per_page, search_value, connection)` — criteria: `(<field>:<op>:<val>)` or `((<f>:<op>:<v>) and (<f>:<op>:<v>))` |

Skip an optional param by passing `null` as a placeholder when a later param is needed.

## Cross-Primitive Integration Patterns

| Integration | From | To | How |
|---|---|---|---|
| Trigger UI logic on button click | **Button** | Deluge (Function) | → Custom Button calls Function via `Setup → Developer Hub → Links & Buttons → Create Button → Action: Call a Function` |
| Validate field before save | **Validation Rule** | Deluge (Function) | → See [functions-categories.dou.md#validation-rule](../assets/functions/functions-categories.dou.md#validation-rule); returns `{status, message}` |
| Enrich record with external data | **Deluge** | External API | → Use `invokeUrl` + [connections.md](./connections.md) for OAuth. See [functions-patterns.dou.md#pattern-2-external-api-and-store-result](../assets/functions/functions-patterns.dou.md#pattern-2-external-api-and-store-result) |
| Display custom UI on page | **Deluge** + **Widget** | Deluge | → Build Deluge Function as backend; embed [Widget](./widgets.md) on page; call Function from Widget via ZDK |
| Populate page field via UI logic | **Deluge** + **ClientScript** | Deluge | → Call Deluge Function from [ClientScript](./clientscript.md) via `ZDK.Apps.CRM.Functions.execute()` |
| Build REST API endpoint | **Deluge (Standalone)** | External caller | → Expose via [api.md](./api.md) REST endpoint; external caller uses OAuth 2.0 |
| Query data in Canvas/Kiosk view | **Queries Workbench** | Deluge | → Build saved [Query](./queries.md); invoke from Deluge via `zoho.crm.invokeQuery()` |

## Known Syntax Gotchas (Verified from Debugging)
<!-- Cross-cutting: affect all generated Deluge code; checked against every output -->

**Deluge differs from most languages:**
- List literal: `{"a", "b"}` — NOT `["a", "b"]`
- Map constructor: `Map()` — NOT `{}` (which creates a list, not a map)
- Loop: `for each item in list { }` — no `for`/`while` exists in Deluge
- Ternary: `if(cond, trueVal, falseVal)` — NOT `cond ? a : b`

### 1. Statements must be on a single line

Deluge does **not** support line continuation. Every statement — including `info`, assignments, and method-chain calls — must fit on one line ending with `;`.

```deluge
// WRONG — causes "Improper Statement Error" on the continuation line
coql_q = "select id from Deals "
       + "where Amount > 10";

// CORRECT
coql_q = "select id from Deals where Amount > 10";
```

### 2. Non-ASCII characters in string literals cause parse errors


Deluge only supports ASCII source code. Unicode characters (em dash `—`, ellipsis `…`, box-drawing `═`, middot `·`, etc.) inside **string literals** trigger an `Improper Statement Error` on the **following** line, which makes the root cause non-obvious.

```deluge
// WRONG — Unicode in string literal
info "Processing…";                  // ellipsis U+2026
info "Revenue — summary";            // em dash U+2014
f_val = "—";                         // em dash as default value

// CORRECT — ASCII replacements
info "Processing...";
info "Revenue - summary";
f_val = "-";
```

> Unicode is fine inside **comments** (`// …`) — only string literals are affected.

### 3. `connection:` in invokeurl requires a bare literal, not a variable


The `connection:` field in `invokeurl` blocks has type **CONNECTION LINKNAME** — it must be a bare literal string, not a variable holding the name.

```deluge
// WRONG — passing a variable causes type mismatch error:
// "value of 'connections' does not match required data type 'CONNECTION LINKNAME'"
conn = "my_connection";
resp = invokeurl
[
    url:        "https://api.example.com/data"
    type:       GET
    connection: conn
];

// CORRECT — use the literal link name directly
resp = invokeurl
[
    url:        "https://api.example.com/data"
    type:       GET
    connection: "my_connection"
];
```

> This restriction applies **only** to `invokeurl`. The `connections` parameter in `zoho.crm.*` built-ins (e.g. `zoho.crm.getRecordById`) accepts a regular STRING variable.

### 4. Opening `{` must be on same line as function signature

Allman style (brace on next line) is rejected by the Deluge editor with "Improper code format" — applies to all 7 function categories.

### 5. Omitting `options_map` silently skips Workflow Rules

Omitting `options_map` from `createRecord`/`updateRecord` silently skips Workflow Rules (approvals, blueprints, orchestration still run). To enable: `optionMap.put("trigger", {"workflow"});`

### 6. Map literal in `invokeurl parameters:` causes parse error

`{"key":val}` in `invokeurl parameters:` → Improper Statement Error; build as variable first. `headers:` allows inline map literals.

### 7. `ifnull` is a standalone function, not a method chain

`NOT expr.ifNull(fallback)` — use `ifnull(expr, fallback)`. Raises "Number of Arguments mismatches for ifnull expecting 2" at runtime.

## Limitations

- No file system access
- Limited loop iterations (avoid infinite loops, CRM has execution time limits)
- `invokeUrl` calls are synchronous and subject to timeout
- Cannot directly call ClientScript or Widget code
- Category timeout limits (hard, non-configurable): Button / Validation Rule / Related List / REST API → 10 s; Automation → 30 s; Schedule → 15 min

## DOU Reference Nodes

> **Partial index — core and automation nodes only.** For data types, operators, variables, trig/log/hyperbolic/niche number built-ins, OpenURL, and XML tasks — open [deluge-index.md](../assets/functions/deluge/deluge-index.md) before generating code. Do not use recalled knowledge for built-in signatures.

### Function Category Templates

| Task | Read This File |
|---|---|
| All 7 category signatures + return types | [#canonical-examples](../assets/functions/functions-categories.dou.md#canonical-examples) |
| Button | [#button](../assets/functions/functions-categories.dou.md#button) |
| Automation | [#automation](../assets/functions/functions-categories.dou.md#automation) |
| Schedule | [#schedule](../assets/functions/functions-categories.dou.md#schedule) |
| Related List | [#related-list](../assets/functions/functions-categories.dou.md#related-list) |
| Standalone (toString, invokeFunction) | [#standalone](../assets/functions/functions-categories.dou.md#standalone) |
| Sales Signals | [#sales-signals](../assets/functions/functions-categories.dou.md#sales-signals) |
| Validation Rule (crmAPIRequest + Map return) | [#validation-rule](../assets/functions/functions-categories.dou.md#validation-rule) |

### Common Patterns

| Task | Read This File |
|---|---|
| Read-then-write | [#pattern-1-read-then-write](../assets/functions/functions-patterns.dou.md#pattern-1-read-then-write) |
| Call external API and store result | [#pattern-2-external-api-and-store-result](../assets/functions/functions-patterns.dou.md#pattern-2-external-api-and-store-result) |
| Guard clause / early exit | [#pattern-3-conditional-guard-clause](../assets/functions/functions-patterns.dou.md#pattern-3-conditional-guard-clause) |
| Loop over search results and update | [#pattern-4-loop-over-search-results-and-update](../assets/functions/functions-patterns.dou.md#pattern-4-loop-over-search-results-and-update) |
| Bulk create with explicit trigger | [#pattern-5-bulk-create-with-trigger-automation](../assets/functions/functions-patterns.dou.md#pattern-5-bulk-create-with-trigger-automation) |
| Two-step cross-module retrieval (Who_Id) | [#pattern-6-two-step-cross-module-retrieval](../assets/functions/functions-patterns.dou.md#pattern-6-two-step-cross-module-retrieval) |

### Deluge Tasks — Conditions

| Task | Read This File |
|---|---|
| Write conditional statements (if / else if / else) | [conditional-statements.dou.md](../assets/functions/deluge/deluge-tasks/conditions/conditional-statements.dou.md) |
| Write criteria-based conditional statements | [criteria-conditional-statements.dou.md](../assets/functions/deluge/deluge-tasks/conditions/criteria-conditional-statements.dou.md) |

### Deluge Tasks — Misc

| Task | Read This File |
|---|---|
| Break out of a loop | [break.dou.md](../assets/functions/deluge/deluge-tasks/misc/break.dou.md) |
| Call a function from within Deluge | [call-function.dou.md](../assets/functions/deluge/deluge-tasks/misc/call-function.dou.md) |
| Continue to the next loop iteration | [continue.dou.md](../assets/functions/deluge/deluge-tasks/misc/continue.dou.md) |
| Return a value from a function | [return.dou.md](../assets/functions/deluge/deluge-tasks/misc/return.dou.md) |
| Send an email from Deluge | [send-mail.dou.md](../assets/functions/deluge/deluge-tasks/misc/send-mail.dou.md) |
| Set a variable | [set-variable.dou.md](../assets/functions/deluge/deluge-tasks/misc/set-variable.dou.md) |
| Handle exceptions with try-catch | [try-catch.dou.md](../assets/functions/deluge/deluge-tasks/misc/try-catch.dou.md) |

### File Functions

| Task | Read This File |
|---|---|
| Compress files | [compress.dou.md](../assets/functions/deluge/file-functions/compress.dou.md) |
| Convert a file to PDF | [convert-to-pdf.dou.md](../assets/functions/deluge/file-functions/convert-to-pdf.dou.md) |
| Extract a compressed file | [extract.dou.md](../assets/functions/deluge/file-functions/extract.dou.md) |
| Get file content | [get-file-content.dou.md](../assets/functions/deluge/file-functions/get-file-content.dou.md) |
| Get file name | [get-file-name.dou.md](../assets/functions/deluge/file-functions/get-file-name.dou.md) |
| Get file size | [get-file-size.dou.md](../assets/functions/deluge/file-functions/get-file-size.dou.md) |
| Get file type | [get-file-type.dou.md](../assets/functions/deluge/file-functions/get-file-type.dou.md) |
| Check if a value is a file | [is-file.dou.md](../assets/functions/deluge/file-functions/is-file.dou.md) |
| Set charset on a file | [set-charset.dou.md](../assets/functions/deluge/file-functions/set-charset.dou.md) |
| Set file name | [set-file-name.dou.md](../assets/functions/deluge/file-functions/set-file-name.dou.md) |
| Set file password | [set-file-password.dou.md](../assets/functions/deluge/file-functions/set-file-password.dou.md) |
| Set file type | [set-file-type.dou.md](../assets/functions/deluge/file-functions/set-file-type.dou.md) |
| Convert a value to a file | [to-file.dou.md](../assets/functions/deluge/file-functions/to-file.dou.md) |

### Integrations

| Task | Read This File |
|---|---|
| Use a named Connection in invokeUrl | [connections.dou.md](../assets/functions/deluge/integrations/connections.dou.md) |
| Transfer files via FTP / SFTP | [ftp-sftp-tasks.dou.md](../assets/functions/deluge/integrations/ftp-sftp-tasks.dou.md) |
| Call an API using the invokeApi task | [invokeapi-task.dou.md](../assets/functions/deluge/integrations/invokeapi-task.dou.md) |
| Call an external URL using the invokeUrl task | [invokeurl-task.dou.md](../assets/functions/deluge/integrations/invokeurl-task.dou.md) |

### Integrations — Zoho CRM Tasks

| Task | Read This File |
|---|---|
| Attach a file to a CRM record | [attach-file.dou.md](../assets/functions/deluge/integrations/zoho-crm/attach-file.dou.md) |
| Bulk create CRM records | [bulk-create-records.dou.md](../assets/functions/deluge/integrations/zoho-crm/bulk-create-records.dou.md) |
| Bulk update CRM records | [bulk-update-records.dou.md](../assets/functions/deluge/integrations/zoho-crm/bulk-update-records.dou.md) |
| Convert a Lead to a Contact | [convert-lead.dou.md](../assets/functions/deluge/integrations/zoho-crm/convert-lead.dou.md) |
| Create a CRM record | [create-record.dou.md](../assets/functions/deluge/integrations/zoho-crm/create-record.dou.md) |
| Get CRM field metadata | [get-fields.dou.md](../assets/functions/deluge/integrations/zoho-crm/get-fields.dou.md) |
| Get a CRM record by ID | [get-record-by-id.dou.md](../assets/functions/deluge/integrations/zoho-crm/get-record-by-id.dou.md) |
| Get CRM records (list) | [get-records.dou.md](../assets/functions/deluge/integrations/zoho-crm/get-records.dou.md) |
| Get related records from a CRM module | [get-related-records.dou.md](../assets/functions/deluge/integrations/zoho-crm/get-related-records.dou.md) |
| Search CRM records | [search-records.dou.md](../assets/functions/deluge/integrations/zoho-crm/search-records.dou.md) |
| Update a CRM record | [update-record.dou.md](../assets/functions/deluge/integrations/zoho-crm/update-record.dou.md) |
| Update a related record | [update-related-record.dou.md](../assets/functions/deluge/integrations/zoho-crm/update-related-record.dou.md) |
| Upsert a CRM record | [upsert-record.dou.md](../assets/functions/deluge/integrations/zoho-crm/upsert-record.dou.md) |


### Function Lifecycle and Best Practices

| Task | Read This File |
|---|---|
| Understanding CRM Functions architecture — categories, trigger types, execution lifecycle, and return type semantics per category | [functions-overview.dou.md](../assets/functions/functions-overview.dou.md) |
| Designing production-quality CRM Functions — idempotency, credential hygiene, performance, logging discipline, and naming conventions | [functions-best-practices.dou.md](../assets/functions/functions-best-practices.dou.md) |
| Building multi-function pipelines, migrating Workflow Rules to Functions, or implementing bulk-record pagination and chunking | [functions-strategies.dou.md](../assets/functions/functions-strategies.dou.md) |

### Deluge Errors

| Task | Read This File |
|---|---|
| Deluge error message reference — save errors, runtime errors, and built-in function type errors | [errors.dou.md](../assets/functions/deluge/errors.dou.md) |

Distilled Operational Understanding nodes for the Deluge scripting language, grouped by category.

### Built-in Functions — Conversion

| Task | Read This File |
|---|---|
| Parse TEXT, NUMBER, or DATE-TIME expression into a DATE-TIME value | [toDate.dou.md](../assets/functions/deluge/built-in-functions/conversion/toDate.dou.md) |
| Convert Unix epoch milliseconds to formatted TEXT with timezone | [toDateTimeString.dou.md](../assets/functions/deluge/built-in-functions/conversion/toDateTimeString.dou.md) |
| Convert a NUMBER, DECIMAL, or numeric TEXT to a DECIMAL value | [toDecimal.dou.md](../assets/functions/deluge/built-in-functions/conversion/toDecimal.dou.md) |
| Convert a NUMBER to its hexadecimal string representation | [toHex.dou.md](../assets/functions/deluge/built-in-functions/conversion/toHex.dou.md) |
| Convert a JSON-formatted TEXT array into a Deluge LIST | [toJSONList.dou.md](../assets/functions/deluge/built-in-functions/conversion/toJSONList.dou.md) |
| Split a TEXT string by a separator into a LIST | [toList.dou.md](../assets/functions/deluge/built-in-functions/conversion/toList.dou.md) |
| Split a comma-separated TEXT or LIST into a LIST of TEXT elements | [toListString.dou.md](../assets/functions/deluge/built-in-functions/conversion/toListString.dou.md) |
| Deluge `toLowerCase()` / `toUpperCase()` — convert all string letters to lower or upper case | [toLowerCase-toUpperCase.dou.md](../assets/functions/deluge/built-in-functions/conversion/toLowerCase-toUpperCase.dou.md) |
| Convert a JSON-formatted TEXT string into a KEY-VALUE map | [toMap.dou.md](../assets/functions/deluge/built-in-functions/conversion/toMap.dou.md) |
| Deluge `toNumber()` / `toLong()` — convert any expression to an integer NUMBER, truncating decimals | [toNumber-toLong.dou.md](../assets/functions/deluge/built-in-functions/conversion/toNumber-toLong.dou.md) |
| Deluge `toString()` / `toText()` — convert any expression to TEXT with optional datetime formatting | [toString-toText.dou.md](../assets/functions/deluge/built-in-functions/conversion/toString-toText.dou.md) |
| Parse a datetime expression into DATE-TIME with explicit timezone conversion | [toTime.dou.md](../assets/functions/deluge/built-in-functions/conversion/toTime.dou.md) |
| Convert NUMBER or DECIMAL to words in a target language | [toWords.dou.md](../assets/functions/deluge/built-in-functions/conversion/toWords.dou.md) |

### Built-in Functions — Date-Time

| Task | Read This File |
|---|---|
| Add (or subtract) seconds from a DATE-TIME value | [add-seconds.dou.md](../assets/functions/deluge/built-in-functions/date-time/add-seconds.dou.md) |
| Deluge addBusinessDay() and subBusinessDay() — advance or retreat a date by business days | [add-sub-business-day.dou.md](../assets/functions/deluge/built-in-functions/date-time/add-sub-business-day.dou.md) |
| Deluge addDay() and subDay() — add or subtract calendar days from a date-time value | [add-sub-day.dou.md](../assets/functions/deluge/built-in-functions/date-time/add-sub-day.dou.md) |
| Deluge addHour() and subHour() — add or subtract hours from a DATE-TIME value | [add-sub-hour.dou.md](../assets/functions/deluge/built-in-functions/date-time/add-sub-hour.dou.md) |
| Deluge addMinutes() and subMinutes() — add or subtract minutes from a DATE-TIME value | [add-sub-minutes.dou.md](../assets/functions/deluge/built-in-functions/date-time/add-sub-minutes.dou.md) |
| Deluge addMonth() and subMonth() — add or subtract calendar months from a date-time value | [add-sub-month.dou.md](../assets/functions/deluge/built-in-functions/date-time/add-sub-month.dou.md) |
| Deluge daysBetween() and hoursBetween() — count calendar days or whole hours between two date-times | [days-hours-between.dou.md](../assets/functions/deluge/built-in-functions/date-time/days-hours-between.dou.md) |
| Shift a date by N months and return that month's last day | [eomonth.dou.md](../assets/functions/deluge/built-in-functions/date-time/eomonth.dou.md) |
| Deluge monthsBetween() and yearsBetween() — count months (30-day) or years (365-day) between dates | [months-years-between.dou.md](../assets/functions/deluge/built-in-functions/date-time/months-years-between.dou.md) |
| Deluge now and today — return the current date-time or current date-only value | [now-today.dou.md](../assets/functions/deluge/built-in-functions/date-time/now-today.dou.md) |
| Deluge toStartOfMonth() and toStartOfWeek() — get first day of a date's month or week | [to-start-of-month-week.dou.md](../assets/functions/deluge/built-in-functions/date-time/to-start-of-month-week.dou.md) |
| Deluge totalMonths() and totalYears() — count calendar months or years respecting actual day counts | [total-months-years.dou.md](../assets/functions/deluge/built-in-functions/date-time/total-months-years.dou.md) |

### Built-in Functions — List

| Task | Read This File |
|---|---|
| Deluge list add() and addAll() — append element(s) to a list in place | [list-add-addall.dou.md](../assets/functions/deluge/built-in-functions/list/list-add-addall.dou.md) |
| Deluge `average()` / `median()` — compute mean and median of a NUMBER or DECIMAL list | [list-average-median.dou.md](../assets/functions/deluge/built-in-functions/list/list-average-median.dou.md) |
| Deluge list contains() — exact membership test for a list element | [list-contains.dou.md](../assets/functions/deluge/built-in-functions/list/list-contains.dou.md) |
| Deluge list get() size() clear() — index access, element count, and list emptying | [list-get-size-clear.dou.md](../assets/functions/deluge/built-in-functions/list/list-get-size-clear.dou.md) |
| Deluge `indexOf()` / `lastIndexOf()` — find first or last index of element in a LIST | [list-indexOf-lastIndexOf.dou.md](../assets/functions/deluge/built-in-functions/list/list-indexOf-lastIndexOf.dou.md) |
| Deluge list intersect() and subList() — get common elements or a slice of a list | [list-intersect-sublist.dou.md](../assets/functions/deluge/built-in-functions/list/list-intersect-sublist.dou.md) |
| Deluge `largest()` / `smallest()` — max and min DECIMAL from a numeric list | [list-largest-smallest.dou.md](../assets/functions/deluge/built-in-functions/list/list-largest-smallest.dou.md) |
| Deluge `notContains()` / `isEmpty()` — boolean membership absence and empty checks on TEXT/LIST/MAP | [list-notContains-isEmpty.dou.md](../assets/functions/deluge/built-in-functions/list/list-notContains-isEmpty.dou.md) |
| Deluge `nthLargest()` / `nthSmallest()` — retrieve the Nth ranked value from a numeric COLLECTION | [list-nthLargest-nthSmallest.dou.md](../assets/functions/deluge/built-in-functions/list/list-nthLargest-nthSmallest.dou.md) |
| Deluge `remove()` / `removeAll()` / `removeElement()` — three ways to remove from a LIST | [list-remove-removeAll-removeElement.dou.md](../assets/functions/deluge/built-in-functions/list/list-remove-removeAll-removeElement.dou.md) |
| Deluge list sort() and distinct() — sort elements or return unique values from a list | [list-sort-distinct.dou.md](../assets/functions/deluge/built-in-functions/list/list-sort-distinct.dou.md) |

### Built-in Functions — Map

| Task | Read This File |
|---|---|
| Deluge map containKey() containValue() notContains() — membership test for keys and values | [map-containkey-containvalue-notcontains.dou.md](../assets/functions/deluge/built-in-functions/map/map-containkey-containvalue-notcontains.dou.md) |
| Deluge map get() keys() size() isEmpty() — read access and state inspection | [map-get-keys-size-isempty.dou.md](../assets/functions/deluge/built-in-functions/map/map-get-keys-size-isempty.dou.md) |
| Deluge map put() and putAll() — insert or merge key-value pairs in place | [map-put-putall.dou.md](../assets/functions/deluge/built-in-functions/map/map-put-putall.dou.md) |
| Deluge map remove() and clear() — delete a key-value pair or empty the entire map | [map-remove-clear.dou.md](../assets/functions/deluge/built-in-functions/map/map-remove-clear.dou.md) |

### Built-in Functions — Number

| Task | Read This File |
|---|---|
| Deluge `abs()` / `frac()` — extract the magnitude or fractional part of a number | [abs-frac.dou.md](../assets/functions/deluge/built-in-functions/number/abs-frac.dou.md) |
| Deluge `addWeek()` / `subWeek()` — shift a DATE-TIME forward or backward by weeks | [addWeek-subWeek.dou.md](../assets/functions/deluge/built-in-functions/number/addWeek-subWeek.dou.md) |
| Deluge `addYear()` / `subYear()` — shift a DATE-TIME forward or backward by years | [addYear-subYear.dou.md](../assets/functions/deluge/built-in-functions/number/addYear-subYear.dou.md) |
| Deluge `ceil()` / `floor()` — round a DECIMAL to the nearest integer above or below | [ceil-floor.dou.md](../assets/functions/deluge/built-in-functions/number/ceil-floor.dou.md) |
| Deluge `day()` / `month()` — extract day-of-month or month NUMBER from DATE-TIME | [day-month.dou.md](../assets/functions/deluge/built-in-functions/number/day-month.dou.md) |
| Extract year as NUMBER from a DATE-TIME value; alias `year()` | [getYear.dou.md](../assets/functions/deluge/built-in-functions/number/getYear.dou.md) |
| Deluge `hour()` / `minute()` / `second()` — get hour, minute, second from a DATE-TIME value | [hour-minute-second.dou.md](../assets/functions/deluge/built-in-functions/number/hour-minute-second.dou.md) |
| Return BOOLEAN true when expression is a valid DATE-TIME value | [isDate.dou.md](../assets/functions/deluge/built-in-functions/number/isDate.dou.md) |
| Check whether an expression evaluates to a valid numeric value | [isnumber.dou.md](../assets/functions/deluge/built-in-functions/number/isnumber.dou.md) |
| Deluge `nextWeekDay()` / `previousWeekDay()` — seek next or previous date by weekday name | [nextWeekDay-previousWeekDay.dou.md](../assets/functions/deluge/built-in-functions/number/nextWeekDay-previousWeekDay.dou.md) |
| Deluge `power()` / `sqrt()` — exponentiate a number or compute its square root | [power-sqrt.dou.md](../assets/functions/deluge/built-in-functions/number/power-sqrt.dou.md) |
| Round a number to a specified decimal or integer precision | [round.dou.md](../assets/functions/deluge/built-in-functions/number/round.dou.md) |
| Deluge max() and min() — compare two numbers and return the larger or smaller | [stat-max-min.dou.md](../assets/functions/deluge/built-in-functions/number/stat-max-min.dou.md) |
| Convert a TEXT date to Unix milliseconds since 1970-01-01 UTC | [unixEpoch.dou.md](../assets/functions/deluge/built-in-functions/number/unixEpoch.dou.md) |
| Get day-of-week NUMBER (1=Sunday, 7=Saturday) from DATE-TIME | [weekday.dou.md](../assets/functions/deluge/built-in-functions/number/weekday.dou.md) |
| Add business days to DATE-TIME with optional weekend and holiday lists | [workday.dou.md](../assets/functions/deluge/built-in-functions/number/workday.dou.md) |

### Built-in Functions — Text

| Task | Read This File |
|---|---|
| Join two TEXT strings into a single concatenated string | [concat.dou.md](../assets/functions/deluge/built-in-functions/text/concat.dou.md) |
| Deluge `contains()` / `containsIgnoreCase()` — check if a TEXT string contains a substring | [contains-containsIgnoreCase.dou.md](../assets/functions/deluge/built-in-functions/text/contains-containsIgnoreCase.dou.md) |
| Deluge `endsWith()` / `endsWithIgnoreCase()` — check if a TEXT string ends with a specific suffix | [endsWith-endsWithIgnoreCase.dou.md](../assets/functions/deluge/built-in-functions/text/endsWith-endsWithIgnoreCase.dou.md) |
| Compare two TEXT strings for equality, ignoring case differences | [equalsIgnoreCase.dou.md](../assets/functions/deluge/built-in-functions/text/equalsIgnoreCase.dou.md) |
| Deluge `find()` / `indexOf()` — return the 0-based index of a searchString's first occurrence | [find-indexOf.dou.md](../assets/functions/deluge/built-in-functions/text/find-indexOf.dou.md) |
| Deluge `getAlpha()` / `getAlphaNumeric()` — extract letters or alphanumeric characters from a string | [getAlpha-getAlphaNumeric.dou.md](../assets/functions/deluge/built-in-functions/text/getAlpha-getAlphaNumeric.dou.md) |
| Count occurrences of a substring within a text string | [getOccurenceCount.dou.md](../assets/functions/deluge/built-in-functions/text/getOccurenceCount.dou.md) |
| Deluge `getPrefix()` / `getSuffix()` — split a string on the first delimiter occurrence | [getPrefix-getSuffix.dou.md](../assets/functions/deluge/built-in-functions/text/getPrefix-getSuffix.dou.md) |
| Decode a hexadecimal-encoded string to its text equivalent | [hexToText.dou.md](../assets/functions/deluge/built-in-functions/text/hexToText.dou.md) |
| Return the 0-based index of the LAST occurrence of a searchString | [lastIndexOf.dou.md](../assets/functions/deluge/built-in-functions/text/lastIndexOf.dou.md) |
| Return a specified number of characters from a string's left side | [left.dou.md](../assets/functions/deluge/built-in-functions/text/left.dou.md) |
| Add leading whitespace to a text string for alignment | [leftpad.dou.md](../assets/functions/deluge/built-in-functions/text/leftpad.dou.md) |
| Deluge `len()` / `length()` — return the character count (including spaces) of a text string | [len-length.dou.md](../assets/functions/deluge/built-in-functions/text/len-length.dou.md) |
| Remove all leading whitespace characters from the left side of a string | [ltrim.dou.md](../assets/functions/deluge/built-in-functions/text/ltrim.dou.md) |
| Test if a string matches a regex pattern exactly | [matches.dou.md](../assets/functions/deluge/built-in-functions/text/matches.dou.md) |
| Extract a substring between two 0-based character indices | [mid.dou.md](../assets/functions/deluge/built-in-functions/text/mid.dou.md) |
| Convert a string to title/start case | [proper.dou.md](../assets/functions/deluge/built-in-functions/text/proper.dou.md) |
| Strip all alphabetic letters from a string | [remove-all-alpha.dou.md](../assets/functions/deluge/built-in-functions/text/remove-all-alpha.dou.md) |
| Strip all letters and digits from a string | [remove-all-alphanumeric.dou.md](../assets/functions/deluge/built-in-functions/text/remove-all-alphanumeric.dou.md) |
| Remove only the first matching substring occurrence | [remove-first-occurence.dou.md](../assets/functions/deluge/built-in-functions/text/remove-first-occurence.dou.md) |
| Remove only the last matching substring occurrence | [remove-last-occurence.dou.md](../assets/functions/deluge/built-in-functions/text/remove-last-occurence.dou.md) |
| Remove all occurrences of a substring from a string | [remove.dou.md](../assets/functions/deluge/built-in-functions/text/remove.dou.md) |
| Replace all occurrences of a substring in a string | [replace-all.dou.md](../assets/functions/deluge/built-in-functions/text/replace-all.dou.md) |
| Replace only the first occurrence of a substring | [replace-first.dou.md](../assets/functions/deluge/built-in-functions/text/replace-first.dou.md) |
| Return a specified number of characters from a string's right side | [right.dou.md](../assets/functions/deluge/built-in-functions/text/right.dou.md) |
| Add trailing whitespace to a text string for alignment | [rightpad.dou.md](../assets/functions/deluge/built-in-functions/text/rightpad.dou.md) |
| Remove all trailing whitespace characters from the right side of a string | [rtrim.dou.md](../assets/functions/deluge/built-in-functions/text/rtrim.dou.md) |
| Deluge `startsWith()` / `startsWithIgnoreCase()` — check if a TEXT string starts with a prefix | [startsWith-startsWithIgnoreCase.dou.md](../assets/functions/deluge/built-in-functions/text/startsWith-startsWithIgnoreCase.dou.md) |
| Deluge `subString()` / `subText()` — extract a substring between two 0-based character indices | [subString-subText.dou.md](../assets/functions/deluge/built-in-functions/text/subString-subText.dou.md) |
| Format NUMBER, DECIMAL, or DATE-TIME using a custom format pattern string | [text.dou.md](../assets/functions/deluge/built-in-functions/text/text.dou.md) |
| Encode a text string to its hexadecimal representation | [textToHex.dou.md](../assets/functions/deluge/built-in-functions/text/textToHex.dou.md) |
| Remove all leading and trailing whitespace from a text string | [trim.dou.md](../assets/functions/deluge/built-in-functions/text/trim.dou.md) |

### Deluge Tasks — Debug

| Task | Read This File |
|---|---|
| Deluge info statement — debug task to print expression values during script execution | [info.dou.md](../assets/functions/deluge/deluge-tasks/debug/info.dou.md) |

### Deluge Tasks — List Manipulations

| Task | Read This File |
|---|---|
| Deluge typed list declarations — List:String, List:Int, List:Float, List:date, List:Bool | [create-list-typed.dou.md](../assets/functions/deluge/deluge-tasks/list-manipulations/create-list-typed.dou.md) |
| Declare an empty or pre-populated heterogeneous list variable | [create-list.dou.md](../assets/functions/deluge/deluge-tasks/list-manipulations/create-list.dou.md) |
| Each-element loop — iterate over list elements or CSV file rows | [for-each-element.dou.md](../assets/functions/deluge/deluge-tasks/list-manipulations/for-each-element.dou.md) |
| Each-index loop — iterate over list element indices (0-based positions) | [for-each-index.dou.md](../assets/functions/deluge/deluge-tasks/list-manipulations/for-each-index.dou.md) |
| Permanently remove all elements from a list | [list-clear.dou.md](../assets/functions/deluge/deluge-tasks/list-manipulations/list-clear.dou.md) |
| Remove the first matching element by value | [list-remove-element.dou.md](../assets/functions/deluge/deluge-tasks/list-manipulations/list-remove-element.dou.md) |
| Remove and return the element at a specified index | [list-remove-index.dou.md](../assets/functions/deluge/deluge-tasks/list-manipulations/list-remove-index.dou.md) |

### Deluge Tasks — Map Manipulations

| Task | Read This File |
|---|---|
| Manipulation tasks — create, insert, merge, delete, and clear map entries | [map-manipulations.dou.md](../assets/functions/deluge/deluge-tasks/map-manipulations/map-manipulations.dou.md) |

> For data types, operators, variables, trig/log/hyperbolic/niche number functions, OpenURL, and XML tasks — see [deluge-index.md](../assets/functions/deluge/deluge-index.md). Do not use recalled knowledge for built-in signatures.