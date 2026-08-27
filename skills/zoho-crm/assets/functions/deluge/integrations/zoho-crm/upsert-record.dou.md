FILE_PURPOSE: zoho.crm.v8.upsert — create or update a CRM record based on a duplicate-check field from Deluge
MENTAL_MODEL: zoho.crm.v8.upsert(module, values, dup_check, connection) → creates new or updates matched record

WHEN_TO_USE:
- Insert or update a record where a unique field (e.g. Email) determines whether a match exists.

WHEN_NOT_TO_USE:
- Known record ID updates — use zoho.crm.v8.updateRecord.
- Guaranteed new creation — use zoho.crm.v8.createRecord.

TRIGGER_KEYWORDS:
zoho.crm.v8.upsert, duplicate_check_fields, INVALID_MODULE, MANDATORY_NOT_FOUND, duplicate_check, Email

RULES:
- Syntax: response = zoho.crm.v8.upsert(module, values, duplicate_check, connection);
- Prefer `Map()` + `.put(key, value)` for generated `values` and `duplicate_check` payloads.
- Duplicate check priority: `duplicate_check` parameter → manually configured "Do not allow duplicate values" field → system-defined default (e.g. Email for Leads).
- If no duplicate-check field value is provided in `values`, no match is attempted and a new record is created.
- `duplicate_check` parameter format: `{"duplicate_check_fields":{"<FieldAPIName>"}}`.
- If multiple records share the same identifier value, upsert updates any one non-deterministically; no error is returned.
- Each execution consumes one external API call.

CANONICAL_EXAMPLES:
```deluge
// Upsert with explicit duplicate check on Email
recordValues = Map();
recordValues.put("Last_Name", "Mark");
recordValues.put("Company", "Zylker");
recordValues.put("Email", "john@zylker.com");
duplicateCheck = Map();
duplicateCheck.put("duplicate_check_fields", {"Email"});
response = zoho.crm.v8.upsert("Leads", recordValues, duplicateCheck, "crm");

// Upsert relying on system default (no Email value provided → new record created)
recordValues = Map();
recordValues.put("Last_Name", "John");
recordValues.put("Company", "Zylker");
response = zoho.crm.v8.upsert("Leads", recordValues);
```

FAILURE_MODES:
- `INVALID_MODULE`: module API name is incorrect. Response includes `{"details":{"resource_path_index":0}}`.
- `MANDATORY_NOT_FOUND`: no match found (falls back to create) and a mandatory field is absent.
- Non-unique identifier (multiple matching records) → upsert updates a non-deterministic record; no error.
- Field display label instead of API name in `values` or `duplicate_check` → match fails; new record created instead of update.
- Duplicate-check field value absent from `values` entirely → no match performed; new record created unconditionally.

RELATED_DOCS:
- Zoho CRM API V8 — Upsert Record — https://www.zoho.com/deluge/help/crm/upsert-record-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/upsert-record-V8.html
