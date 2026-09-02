# Zoho CRM API v8.0 — Reference Guide

## !! API Doc Resolution Procedure — EXECUTE THIS FIRST !!

Before answering any API-related question, follow these steps in strict order.

**Prerequisite (optional)**: `pip3 install pyyaml` (required only if running Step 5; skip Step 5 entirely if Python is unavailable).

### Step 1 — Identify the resource folder

`{resource}` identified here is used in all subsequent steps.

| Need | Resource Folder |
|---|---|
| Any CRUD on a CRM module record (GET/POST/PUT/DELETE/Upsert/Clone/Deleted) | `record/` |
| Search records (`GET /{module}/search`, bulk search) | `module_search/` |
| Mass update records | `mass_update/` |
| Field metadata (list/create/update/delete fields) | `fields/` |
| Picklist values | `pick_list_values/` |
| All other needs | folder name = resource name directly (e.g., `coql`, `modules`, `users`, `layouts`, `bulk_read`, `bulk_write`, `notes`, `attachments`, `tags`, `roles`, `profiles`, `record_count`, `change_owner`, `convert`, `recycle_bin`, `composite_requests`, `timelines`, `apis`, `related_records`, `related_lists`) |

Note: `related_records` and `related_lists` are distinct — `related_records` for CRUD on related records; `related_lists` for listing a module's related list configuration.
For queries that touch multiple resources, repeat Step 2 for each resource.

### Step 2 — Locate or acquire the OAS resource folder

> Each resource folder contains `{resource}.yaml`, an `index.md` overview, and an `operations/` subfolder. Each `operations/{operationId}/` directory contains `operation.md` and an `examples/` subfolder with `request.md` and `response-*.md` files.

Check whether `.zoho-crm/references/api/{resource}/` exists (where `{resource}` is identified in Step 1 above):

1. **Already copied** — `.zoho-crm/references/api/{resource}/` exists → use it, skip to Step 3
2. **Existing local clone** — user has the OAS cloned at a known path → run `cp` from that folder directly; no git clone needed
   - If `cp` fails (wrong path or resource absent) → fall straight to HTTP fallback; do NOT attempt to clone `/tmp/crm-oas`
3. **No local copy** — clone to `/tmp/crm-oas`, then `cp`:
   ```bash
   mkdir -p .zoho-crm/references/api/
   [ -d /tmp/crm-oas ] || git clone --depth 1 https://github.com/zoho/crm-oas.git /tmp/crm-oas
   cp -r /tmp/crm-oas/v8.0/{resource}/ .zoho-crm/references/api/{resource}/
   ```
   - If `cp` fails → `rm -rf /tmp/crm-oas`, re-run clone + `cp` once; if that also fails → HTTP fallback

**HTTP fallback** (scenarios 2 and 3 on failure): fetch the entire YAML at:
```
https://raw.githubusercontent.com/zoho/crm-oas/main/v8.0/{resource}/{resource}.yaml
```
Skip Steps 3, 4, 4b, 5; read the full YAML and proceed directly to Step 6.

### Step 3 — Identify the operation from the resource index

```bash
cat .zoho-crm/references/api/{resource}/index.md
```

Each entry is a camelCase operationId directory name described in `index.md` — read the descriptions to pick the one matching intent. Prefer the more specific name (singular = single-record operation, plural = multiple-records operation).

**If `index.md` and `operations/` are absent** → skip Steps 3, 4, 4b; proceed directly to Step 5.

### Step 4 — Read the operation md

```bash
cat .zoho-crm/references/api/{resource}/operations/{operationId}/operation.md
```

Extract: HTTP method, path, parameters, request body fields (including nested schema details), responses per status code, OAuth scopes. The md is authoritative for schema structure and nested field details.

### Step 4b — Read operation examples

```bash
cat .zoho-crm/references/api/{resource}/operations/{operationId}/examples/request.md
cat .zoho-crm/references/api/{resource}/operations/{operationId}/examples/response-200-*.md
```

Read `examples/request.md` for named JSON request variants — use these to construct and validate the actual request body. Read the first relevant `examples/response-200-*.md` for the concrete success response shape. If `examples/` is absent or empty → skip this step silently and continue to Step 5. Examples are authoritative for concrete JSON shapes; they complement (not replace) the schema structure from `operation.md`.

### Step 5 — Run Python extractor *(optional)*

**Skip this step if Python 3 is not available** — proceed directly to Step 6 using Step 4 md data and Step 4b examples (if available). If Steps 4 and 4b were also skipped, use the HTTP fallback YAML. Run this step when Python is available; if Steps 4 and 4b were also skipped (operations/ absent), run this directly.

```bash
python3 dx-education-docs/.github/skills/zoho-crm/assets/api/extract_schema.py \
  --api-dir .zoho-crm/references/api \
  --resource {resource} \
  --operation {operationId}
```

Script lives permanently in the skill folder — never copied to `.zoho-crm/`. Only `--api-dir` points to the runtime clone.
**If the script is not found at this path, treat as Step 5 failure (see below).**

Output (three labeled sections):
```
=== SERVERS ===
<servers[0] YAML>

=== OPERATION ===
<path, method, full operation object YAML with $ref strings intact>

=== SCHEMAS ===
<each schema from components/schemas referenced in requestBody and 2xx responses — one level deep>
```

Error response schemas are excluded from `=== SCHEMAS ===` — they are covered by Step 4 `operation.md`, Step 4b examples, and Rule 5.

**Authority split**:

| Source | Authoritative for |
|---|---|
| Step 4 `operation.md` | Schema structure and nested field details |
| Step 4b examples | Concrete request/response JSON shapes and named variants |
| Step 5 `=== OPERATION ===` + `=== SCHEMAS ===` | Exact field names, constraints, security scopes |

- If Step 4 `operation.md` and Step 5 conflict on a field name or constraint, **Step 5 YAML wins** — treat the `operation.md` as stale
- If `security` is absent in Step 5 `=== OPERATION ===` (operation inherits global security), read scopes from Step 4 `operation.md` instead; if Step 4 was also skipped, read the global `security` block from the full YAML

**If Step 5 fails or is skipped** (Python unavailable, script not found, PyYAML missing, parse error) → proceed to Step 6 using Step 4 md data and Step 4b examples (if available); if Steps 4 and 4b were also skipped, fetch the entire `{resource}.yaml` via the fallback URL and read it directly.

### Step 6 — Interpret and execute

All 6 rules below are Zoho-specific — do not skip any:

1. **URL**: `servers[0].url` is `https://zohoapis.{dc}/crm/{version}`; substitute `{dc}` with the user's data-center suffix (`com`, `eu`, `in`, `cn`, `au`) and `{version}` with `v8`; append path params, then query params.
2. **Auth**: Read `security` at the **operation level** (overrides global default). Entries = OR alternatives; scopes within entry = AND. Pick the most permissive general option. Settings operations require `ZohoCRM.settings.*.READ` in addition to module scope — always check the resource folder + operation md, never assume module-scope alone suffices. Header: `Authorization: Zoho-oauthtoken {access_token}`.
3. **Body**: All `$ref` are internal (`#/components/schemas/...`). Use Step 4 `operation.md` for schema structure and nested field details; use Step 4b `examples/request.md` for concrete request body shapes and named variants; use Step 5 `=== SCHEMAS ===` output for exact field names and constraints when available. If Step 5 was skipped, rely on Step 4 `operation.md` and Step 4b examples (if available). Preserve every property name **exactly** as found — Zoho silently ignores renamed/inferred fields.
4. **Validate**: Confirm all required path params, query params, headers, and body fields are present before executing. Report missing items; never assume a value.
5. **Errors**: 4xx → extract `code` + `message` from error body, explain cause, suggest fix (missing scope → add OAuth scope; invalid field → check API name); also check `operations/{operationId}/examples/response-{code}-*.md` — filenames encode the error title (e.g., `response-400-invalidmodule.md`), match the `code` field to the filename suffix for a concrete JSON reference. 5xx → surface raw response, wait 10 s, retry once; if persists, escalate to Zoho CRM support.
6. **Execute**: If MCP tools are connected → call the tool with exact OAS-derived parameters. If not connected → output the complete cURL command with all headers, body, and expected response structure.

## Git Repo

```
https://github.com/zoho/crm-oas
```
Use the `v8.0/` folder. Files are OpenAPI Specification (OAS) 3.1.0 format (`.yaml`), organized into per-resource subfolders. Each folder contains `{resource}.yaml`, an `index.md` overview, and an `operations/` subfolder. Each `operations/{operationId}/` directory contains `operation.md` and an `examples/` subfolder with `request.md` and `response-*.md` files.

## API Base URL

```
https://zohoapis.com/crm/v8/
```

| Data center | Base URL |
|---|---|
| COM (US/Global) | `https://zohoapis.com/crm/v8/` |
| EU | `https://zohoapis.eu/crm/v8/` |
| IN | `https://zohoapis.in/crm/v8/` |
| CN | `https://zohoapis.com.cn/crm/v8/` |
| AU | `https://zohoapis.com.au/crm/v8/` |

## Authentication

All requests require a Bearer token from Zoho OAuth 2.0.

```
Authorization: Zoho-oauthtoken {access_token}
```

**Token endpoint**: `https://accounts.zoho.com/oauth/v2/token`

> **Settings scopes**: Operations on fields, layouts, picklist values, and module metadata require `ZohoCRM.settings.fields.READ` or `ZohoCRM.settings.ALL` in addition to (or instead of) module scopes. Always read the operation's `security` array in the resource folder + operation md to determine the exact scopes required — do not assume module-scope alone is sufficient.

> **Managed tokens**: For Deluge Functions and ClientScript calling CRM APIs internally, use a **Connection** (Zoho stores and auto-refreshes the token). See [connections.md](./connections.md) for setup. The raw OAuth flow described here is for **external callers** (scripts, backend servers, CI pipelines).

## Common Endpoints

| Operation | Method | Endpoint | Notes |
|-----------|--------|----------|-------|
| Get records | GET | `/crm/v8/{module}` | |
| Get record by ID | GET | `/crm/v8/{module}/{id}` | |
| Create records | POST | `/crm/v8/{module}` | |
| Update records | PUT | `/crm/v8/{module}` | |
| Upsert records | POST | `/crm/v8/{module}/upsert` | |
| Delete records | DELETE | `/crm/v8/{module}?ids={id1,id2}` | |
| Search records | GET | `/crm/v8/{module}/search` | Spec: resource `module_search/` |
| Run COQL | POST | `/crm/v8/coql` | SQL-like CRM query lang → [coql.md](./coql.md) |
| Run native query | POST | `/crm/v8/query` | UI-authored saved queries → [queries.md](./queries.md) |
| Execute function | POST | `/crm/v8/functions/{function_name}/actions/execute` | Invoke Deluge Standalone Function → [functions.md](./functions.md) |
| Mass update records | POST | `/crm/v8/{module}/actions/mass_update` | Spec: resource `mass_update/` |

## Query Parameters (GET /module)

| Param | Type | Description |
|-------|------|-------------|
| `fields` | string | Comma-separated field API names |
| `sort_order` | asc \| desc | Sort direction |
| `sort_by` | string | Field to sort by |
| `per_page` | int | Records per page (max 200) |
| `page` | int | Page number (1-indexed) |
| `page_token` | string | Cursor for pagination (v8) |
| `territory_id` | string | Filter by territory |
| `include` | string | Include related records |

## Search Parameters (GET /module/search)

| Param | Description |
|-------|-------------|
| `criteria` | Filter expression: `(field_api_name:equals:value)` |
| `email` | Search by email (Contacts, Leads only) |
| `phone` | Search by phone |
| `word` | Full-text search keyword |
| `converted` | `true` / `false` (Leads only) |
| `approved` | `true` / `false` |

**Criteria syntax:**
```
(Last_Name:equals:Smith)
((Last_Name:equals:Smith)and(Lead_Status:equals:New))
```

Operators: `equals`, `not_equal`, `starts_with`, `ends_with`, `contains`, `between`, `in`, `not_in`, `is_empty`, `is_not_empty`, `greater_than`, `less_than`, `greater_equal`, `less_equal`

## Standard Response Structure

```json
{
  "data": [ { ...record fields... } ],
  "info": {
    "per_page": 200,
    "count": 45,
    "page": 1,
    "more_records": false
  }
}
```

**Error response:**
```json
{
  "code": "INVALID_TOKEN",
  "details": {},
  "message": "invalid oauth token",
  "status": "error"
}
```

## Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content (delete success) |
| 400 | Bad Request (malformed input) |
| 401 | Unauthorized (token invalid/expired) |
| 403 | Forbidden (scope missing) |
| 404 | Not Found |
| 429 | Rate limit exceeded |

## Rate Limits

> Rate limits vary by plan — see https://www.zoho.com/crm/developer/docs/api/v8/api-limits.html. On 429: wait and retry using Retry-After header.
