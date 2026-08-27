FILE_PURPOSE: zoho.crm.v8.getFields — fetch field metadata for all fields in a CRM module from Deluge
MENTAL_MODEL: zoho.crm.v8.getFields(module, connection) → {fields:[{field_label, operation_type, field_read_only, ...}]}

WHEN_TO_USE:
- Discover field properties (read-only status, API writability) before constructing create/update payloads.
- Inspect operation_type flags to determine which fields support api_create or api_update.

WHEN_NOT_TO_USE:
- Fetching record values — use zoho.crm.v8.getRecords or zoho.crm.v8.getRecordById.
- Repeated calls inside a loop — cache the result; each call consumes one external API credit.

TRIGGER_KEYWORDS:
zoho.crm.v8.getFields, INVALID_MODULE, field_label, field_read_only, operation_type, api_create, getFields

RULES:
- Syntax: response = zoho.crm.v8.getFields(module_name, connection);
- Returns metadata for all fields in the specified module — not record values.
- Each field metadata object includes: `field_label`, `display_label`, `read_only`, `field_read_only`, `operation_type` (`{api_create, api_update, web_create, web_update}`), `webhook`, `id`.
- `operation_type.api_create: false` → field cannot be set at record creation via API; submission silently ignored.
- `operation_type.api_update: false` → field cannot be updated via API; submission silently ignored.
- `field_read_only: true` → field cannot be updated via API; write attempts silently ignored.

CANONICAL_EXAMPLES:
```deluge
response  = zoho.crm.v8.getFields("Contacts", "crm_connection");
fieldsList = response.get("fields");
for each field in fieldsList {
  info field.get("field_label");
  info field.get("field_read_only");
}
```

FAILURE_MODES:
- `INVALID_MODULE`: module API name is incorrect. Response: `{"code":"INVALID_MODULE","status":"error"}`.
- `field_label` / `display_label` is the human-readable display name; using it as a payload key in create/update calls → `MANDATORY_NOT_FOUND` or silent wrong-field write.
- `field_read_only: true` fields silently ignore write attempts — no error returned.
- `operation_type.api_create: false` fields silently ignore creation-time submissions.

RELATED_DOCS:
- Zoho CRM API V8 — Get Fields — https://www.zoho.com/deluge/help/crm/get-fields-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/get-fields-V8.html
