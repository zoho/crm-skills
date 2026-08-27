## FILE_PURPOSE
zoho.crm.v8.updateRecord — update a single existing CRM record by ID from Deluge

## MENTAL_MODEL
zoho.crm.v8.updateRecord(module, record_id, fields, trigger_map, connection) → modification metadata

## WHEN_TO_USE
- Update specific fields on one existing CRM record identified by its record ID.

## WHEN_NOT_TO_USE
- Batch updates of multiple records — use zoho.crm.v8.bulkUpdate (up to 100 records per call).
- Record creation — use zoho.crm.v8.createRecord.

## TRIGGER_KEYWORDS
zoho.crm.v8.updateRecord, INVALID_DATA, INVALID_MODULE, record_Id, options_map, Last_Name, workflow

## RULES
- Syntax: response = zoho.crm.v8.updateRecord(module_name, record_Id, record_value, options_map, connection);
- Parameters must follow defined syntax order; assign null to any skipped optional parameter before a later-used one.
- Prefer `Map()` + `.put(key, value)` for generated `record_value` and `options_map` payloads.
- options_map key: `"trigger"`; values: `"workflow"`, `"approval"`, `"blueprint"`, `"orchestration"`.
  - Omitted options_map → only approvals, blueprints, orchestration run by default; `"workflow"` does NOT run.
  - Deluge trigger values use list/collection literal syntax, for example `optionMap.put("trigger", {"workflow"});`; this serializes to an array in the API payload.
  - Empty trigger list → suppresses all automations silently.
- Connection mandatory for Zoho Cliq; optional for all other Zoho services.
- Do not pass an empty string as `connection`; omit it when not needed, or pass a confirmed Connection link name.
- Each execution consumes one external API call.

## CANONICAL_EXAMPLES
```deluge
leadInfo = Map();
leadInfo.put("Company", "Zylker");
leadInfo.put("Last_Name", "Stewart");
leadInfo.put("Phone", "9876XXXXXX");
leadInfo.put("Email", "stewart@zylker.com");
response = zoho.crm.v8.updateRecord("Leads", 23033XXXXXXXXXXXXXX, leadInfo);

// Enable workflows explicitly
optionMap = Map();
optionMap.put("trigger", {"workflow", "approval", "blueprint", "orchestration"});
response = zoho.crm.v8.updateRecord("Leads", recordId, leadInfo, optionMap, "crm_conn");
```

## FAILURE_MODES
- `INVALID_DATA`: record_Id is incorrect or non-existent. Response: `{"code":"INVALID_DATA","message":"the id given seems to be invalid"}`.
- `INVALID_MODULE`: module API name is incorrect.
- Field display label instead of API name (e.g. `"Last Name"` not `"Last_Name"`) → silent wrong-field write.
- options_map omitted → `"workflow"` does NOT run by default.
- Empty trigger list suppresses all automations silently.
- **Workflow Function infinite loop**: A Workflow Function that calls `zoho.crm.v8.updateRecord` on the same record that triggered it re-fires the same workflow rule. The loop continues until the daily Function-execution credit is exhausted or the record-update history quota is hit; the chain then returns 429 silently into any upstream workflow. Guard using one of: (a) a `last_modified_by` check that excludes the Function's own service user, or (b) a custom boolean flag field (e.g. `Loop_Guard__c`) that the Function flips and the workflow rule condition checks.

## RELATED_DOCS
- Zoho CRM API V8 — Update Record — https://www.zoho.com/deluge/help/crm/update-record-V8.html

## SOURCE
https://www.zoho.com/deluge/help/crm/update-record-V8.html
