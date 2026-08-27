FILE_PURPOSE: zoho.crm.v8.getRecordById — fetch a single CRM record by its record ID from Deluge
MENTAL_MODEL: zoho.crm.v8.getRecordById(module, record_id, fields, connection) → flat field-value map or {status:failure}

WHEN_TO_USE:
- Fetch a known record's field values using its record ID.

WHEN_NOT_TO_USE:
- Bulk fetching multiple records — use zoho.crm.v8.getRecords.
- Searching by criteria — use zoho.crm.v8.searchRecords.

TRIGGER_KEYWORDS:
zoho.crm.v8.getRecordById, record_Id, INVALID_MODULE, query_value, getRecordById, First_Name

RULES:
- Syntax: response = zoho.crm.v8.getRecordById(module_name, record_Id, query_value, connection);
- `query_value` must include `"fields"` key; `<query_value>` must be specified before `<connection>` can be used.
- Prefer `Map()` + `.put(key, value)` for generated `query_value` payloads.
- Response returns only the fields listed in `query_value["fields"]`; unlisted fields are absent (not null).
- Invalid record_Id returns `{"status":"failure"}` — no `code` field; check for `status == "failure"` specifically.
- Do not pass an empty string as `connection`; omit it when not needed, or pass a confirmed Connection link name.
- Each execution consumes one external API call.

CANONICAL_EXAMPLES:
```deluge
queryData = Map();
queryData.put("fields", "First_Name,Last_Name,Company,Email");
response = zoho.crm.v8.getRecordById("Leads", 2303XXXXXXXXXX, queryData);
info response;
```

FAILURE_MODES:
- Invalid or non-existent record_Id → `{"status":"failure"}` (no `code` key); distinct from `INVALID_MODULE` pattern.
- `INVALID_MODULE`: module API name is incorrect. Response: `{"code":"INVALID_MODULE","status":"error"}`.
- `"fields"` key missing from `query_value` → error or empty response.
- Field display label in `"fields"` value instead of API name → null values silently.
- Specifying `<connection>` without first specifying `<query_value>` → ordering failure.

RELATED_DOCS:
- Zoho CRM API V8 — Get Record by ID — get-records.dou.md

SOURCE:
https://www.zoho.com/deluge/help/crm/get-record-by-id-V8.html
