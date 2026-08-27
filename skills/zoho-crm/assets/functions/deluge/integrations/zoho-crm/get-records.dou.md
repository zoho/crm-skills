FILE_PURPOSE: zoho.crm.v8.getRecords — fetch paginated records from a CRM module from Deluge
MENTAL_MODEL: zoho.crm.v8.getRecords(module, query_data, page, per_page, connection) → list of record maps

WHEN_TO_USE:
- Fetch a page of records from a standard or custom CRM module with optional sort and field filtering.
- Iterate all records in a module by incrementing page parameter.

WHEN_NOT_TO_USE:
- Fetch a specific record by ID — use zoho.crm.v8.getRecordById.
- Search records by criteria — use zoho.crm.v8.searchRecords.

TRIGGER_KEYWORDS:
zoho.crm.v8.getRecords, sort_order, sort_by, per_page, query_data, getRecords, First_Name

RULES:
- Syntax: response = zoho.crm.v8.getRecords(module_name, query_value, page, per_page, connection);
- `query_value` must include `"fields"` key with comma-separated field API names; other keys (sort_order, sort_by) are optional.
- Prefer `Map()` + `.put(key, value)` for generated `query_value` payloads.
- `<page>` must be specified before `<per_page>` can be used; default per_page is 200.
- Both `<page>` and `<per_page>` must be specified before `<query_value>` or `<connection>` can be used.
- Do not pass an empty string as `connection`; omit it when not needed, or pass a confirmed Connection link name.
- Each execution consumes one external API call.

CANONICAL_EXAMPLES:
```deluge
queryData = Map();
queryData.put("sort_order", "asc");
queryData.put("sort_by", "Created_Time");
queryData.put("fields", "First_Name,Last_Name,Mobile");
response = zoho.crm.v8.getRecords("Contacts", queryData, 1, 10, "crm_connection");

// Extract record IDs
idList = list();
for each rec in response.toJsonList() { idList.add(rec.getJson("id")); }
```

FAILURE_MODES:
- `"fields"` key missing from `query_value` → error or unusable response.
- Field display label in `"fields"` value instead of API name → null or missing values silently.
- Specifying `<per_page>` without `<page>` first → parameter ordering failure.
- Specifying `<query_value>` without both `<page>` and `<per_page>` first → parameter ordering failure.
- HIPAA Restrict-Data-Access silently redacts restricted fields; they appear with null values.

RELATED_DOCS:
- Zoho CRM API V8 — Get Records — https://www.zoho.com/deluge/help/crm/get-records-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/get-records-V8.html
