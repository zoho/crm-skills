FILE_PURPOSE: zoho.crm.v8.bulkCreate — insert up to 100 records simultaneously into a CRM module from Deluge
MENTAL_MODEL: zoho.crm.v8.bulkCreate(module, records_list, trigger_map, connection) → per-record result list

WHEN_TO_USE:
- Batch-insert multiple records (up to 100) into a standard or custom CRM module in one API call.

WHEN_NOT_TO_USE:
- Single record insertion — use zoho.crm.v8.createRecord.
- More than 100 records — split into batches of ≤ 100.

TRIGGER_KEYWORDS:
zoho.crm.v8.bulkCreate, MANDATORY_NOT_FOUND, options_map, records_value, Last_Name, bulkCreate, workflow

RULES:
- Syntax: response = zoho.crm.v8.bulkCreate(module_name, records_value, options_map, connection);
- `records_value` must be a LIST of KEY-VALUE maps; use `List()` + `.add(recordMap)` and `Map()` + `.put(key, value)` in generated code.
- Maximum 100 records per call; exceeding this limit causes the entire request to fail.
- options_map key: `"trigger"`; values: `"workflow"`, `"approval"`, `"blueprint"`, `"orchestration"`.
  - Omitted options_map → only approvals, blueprints, orchestration run by default; `"workflow"` does NOT run.
  - Deluge trigger values use list/collection literal syntax, for example `optionMap.put("trigger", {"workflow"});`; this serializes to an array in the API payload.
  - Empty trigger list → suppresses all automations silently across all records in the call.
- Partial success is possible — some records succeed while others fail; check per-record status in response.

CANONICAL_EXAMPLES:
```deluge
createList = List();
recordMap1 = Map();
recordMap1.put("Company", "Zylker");
recordMap1.put("Last_Name", "Daly");
recordMap1.put("First_Name", "Paul");
recordMap1.put("Email", "p.daly@zylker.com");
recordMap2 = Map();
recordMap2.put("Company", "Tycoon");
recordMap2.put("Last_Name", "Richard");
recordMap2.put("First_Name", "Brian");
recordMap2.put("Email", "brian@villa.com");
createList.add(recordMap1);
createList.add(recordMap2);
response = zoho.crm.v8.bulkCreate("Leads", createList);
```

FAILURE_MODES:
- `MANDATORY_NOT_FOUND`: required field absent from one or more record maps; that record fails while others succeed.
- Field display label instead of API name in a record map → `MANDATORY_NOT_FOUND` or silent wrong-field write per affected record.
- Exceeding 100 records per call → entire request fails; split into batches.
- options_map omitted → `"workflow"` does NOT run by default.
- Passing `records_value` as KEY-VALUE instead of LIST → execution failure.

RELATED_DOCS:
- Zoho CRM API V8 — Create Records — create-record.dou.md

SOURCE:
https://www.zoho.com/deluge/help/crm/bulk-create-records-V8.html
