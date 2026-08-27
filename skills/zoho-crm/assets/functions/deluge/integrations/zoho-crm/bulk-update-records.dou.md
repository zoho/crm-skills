FILE_PURPOSE: zoho.crm.v8.bulkUpdate — update up to 100 existing CRM records simultaneously from Deluge
MENTAL_MODEL: zoho.crm.v8.bulkUpdate(module, records_list_with_ids, trigger_map, connection) → per-record result list

WHEN_TO_USE:
- Batch-update multiple existing records (up to 100) in one API call.

WHEN_NOT_TO_USE:
- Single record update — use zoho.crm.v8.updateRecord.
- More than 100 records — split into batches of ≤ 100.

TRIGGER_KEYWORDS:
zoho.crm.v8.bulkUpdate, MANDATORY_NOT_FOUND, INVALID_DATA, records_value, options_map, bulkUpdate, workflow

RULES:
- Syntax: response = zoho.crm.v8.bulkUpdate(module_name, records_value, options_map, connection);
- `records_value` must be a LIST of KEY-VALUE maps; use `List()` + `.add(recordMap)` and `Map()` + `.put(key, value)` in generated code. Each map must include `id` plus field API names to update.
- Maximum 100 records per call; exceeding this limit causes the entire request to fail.
- options_map key: `"trigger"`; values: `"workflow"`, `"approval"`, `"blueprint"`, `"orchestration"`.
  - Omitted options_map → approvals, blueprints, orchestration run by default; `"workflow"` does NOT run.
  - Deluge trigger values use list/collection literal syntax, for example `optionMap.put("trigger", {"workflow"});`; this serializes to an array in the API payload.
  - Empty trigger list → suppresses all automations silently across all updated records.
- Partial success is possible; check per-record status in response; response order not guaranteed to match input order.

CANONICAL_EXAMPLES:
```deluge
updateList = List();
recordMap1 = Map();
recordMap1.put("id", "3171565000000600001");
recordMap1.put("Company", "Zylker");
recordMap1.put("Last_Name", "Daly");
recordMap1.put("Email", "p.daly@zylker.com");
recordMap2 = Map();
recordMap2.put("id", "3171565000000600002");
recordMap2.put("Company", "Tycoon");
recordMap2.put("Last_Name", "Richard");
recordMap2.put("Email", "brian@villa.com");
updateList.add(recordMap1);
updateList.add(recordMap2);
response = zoho.crm.v8.bulkUpdate("Leads", updateList);
```

FAILURE_MODES:
- Missing `"id"` key in a record map → that record fails with `INVALID_DATA`; others proceed.
- `MANDATORY_NOT_FOUND`: required field absent from a record map; that record fails while others succeed.
- Field display label instead of API name → silent wrong-field write or per-record failure.
- Exceeding 100 records per call → entire request fails.
- options_map omitted → `"workflow"` does NOT run by default.

RELATED_DOCS:
- Zoho CRM API V8 — Update Records — update-record.dou.md

SOURCE:
https://www.zoho.com/deluge/help/crm/bulk-update-records-V8.html
