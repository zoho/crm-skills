FILE_PURPOSE: zoho.crm.v8.createRecord — insert a single record into a Zoho CRM module from Deluge
MENTAL_MODEL: zoho.crm.v8.createRecord(module, fields, trigger_map, connection) → creation metadata KEY-VALUE

WHEN_TO_USE:
- Insert one new record into a standard or custom CRM module.
- Create a Notes submodule record linked to a parent via Parent_Id and $se_module.

WHEN_NOT_TO_USE:
- Batch creation — use zoho.crm.v8.bulkCreate (up to 100 records per call).

TRIGGER_KEYWORDS:
zoho.crm.v8.createRecord, MANDATORY_NOT_FOUND, options_map, Last_Name, $se_module, Parent_Id, workflow

RULES:
- Syntax: response = zoho.crm.v8.createRecord(module_name, record_details, options_map, connection);
- Parameters must follow defined syntax order; assign null to any skipped optional parameter before a later-used one.
- Prefer `Map()` + `.put(key, value)` for generated `record_details` and `options_map` payloads.
- options_map key: `"trigger"`; values: `"workflow"`, `"approval"`, `"blueprint"`, `"orchestration"`.
  - Omitted options_map → approvals, blueprints, orchestration run by default; `"workflow"` does NOT run.
  - Deluge trigger values use list/collection literal syntax, for example `optionMap.put("trigger", {"workflow"});`; this serializes to an array in the API payload.
  - Empty trigger list → suppresses all automations silently.
- Connection mandatory for Zoho Cliq; optional for all other Zoho services.
- Do not pass an empty string as `connection`; omit it when not needed, or pass a confirmed Connection link name.
- Each execution consumes one external API call; a loop of N iterations = N calls.
- Notes submodule: include `"Parent_Id"` (parent record ID) and `"$se_module"` (parent module API name) in record_details.
- Extract created record ID: `response.get("id").toLong();`

CANONICAL_EXAMPLES:
```deluge
leadInfo = Map();
leadInfo.put("Company", "Zylker");
leadInfo.put("Last_Name", "Williams");
leadInfo.put("Email", "will@zylker.com");
response = zoho.crm.v8.createRecord("Leads", leadInfo);
newId = response.get("id").toLong();

// Notes submodule
notes = Map();
notes.put("Parent_Id", "2303XXXXXXXXXX");
notes.put("Note_Title", "Title");
notes.put("Note_Content", "Desc");
notes.put("$se_module", "Leads");
response = zoho.crm.v8.createRecord("Notes", notes);

// Suppress all automations
optionMap = Map();
optionMap.put("trigger", {});
response = zoho.crm.v8.createRecord("Leads", leadInfo, optionMap, "crm_conn");
```

FAILURE_MODES:
- `MANDATORY_NOT_FOUND`: required field absent. Response includes `{"code":"MANDATORY_NOT_FOUND","details":{"api_name":"Last_Name"}}`.
- Field display label (e.g. `"Last Name"`) instead of API name (`"Last_Name"`) → `MANDATORY_NOT_FOUND` or silent wrong-field write.
- options_map omitted → `"workflow"` does NOT run by default; include it in trigger list to enable workflows.
- Empty trigger list suppresses all automations silently.
- Parameters out of defined order → execution failure; use null as placeholder for skipped optional params.

RELATED_DOCS:
- Zoho CRM API V8 — Create Record — https://www.zoho.com/deluge/help/crm/create-record-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/create-record-V8.html
