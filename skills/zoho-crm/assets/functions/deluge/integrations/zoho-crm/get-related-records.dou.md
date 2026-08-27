FILE_PURPOSE: zoho.crm.v8.getRelatedRecords — fetch records from a CRM submodule related to a parent record
MENTAL_MODEL: zoho.crm.v8.getRelatedRecords(sub_module, parent_module, parent_id, fields, page, per_page, conn) → list

WHEN_TO_USE:
- Fetch related list records (Notes, Contacts, Price Books, etc.) linked to a specific parent record.

WHEN_NOT_TO_USE:
- Fetching records from a top-level module — use zoho.crm.v8.getRecords.

TRIGGER_KEYWORDS:
zoho.crm.v8.getRelatedRecords, relation_name, parent_module_name, record_id, per_page, getRelatedRecords

RULES:
- Syntax: response = zoho.crm.v8.getRelatedRecords(relation_name, parent_module_name, record_id, query_value, page, per_page, connection);
- `query_value` must include `"fields"` key; all other keys optional per CRM API.
- Prefer `Map()` + `.put(key, value)` for generated `query_value` payloads.
- `<page>` and `<per_page>` must be specified before `<query_value>` or `<connection>` can be used.
- Default per_page: 200. Default page: 1.
- Do not pass an empty string as `connection`; omit it when not needed, or pass a confirmed Connection link name.
- Each execution consumes one external API call.

CANONICAL_EXAMPLES:
```deluge
queryData = Map();
queryData.put("fields", "First_Name,id,Email,Last_Name");
response = zoho.crm.v8.getRelatedRecords("Contacts", "Accounts", 4770XXXXXXXXXXX, queryData, 1, 2, "crm");
```

FAILURE_MODES:
- Swapping `relation_name` and `parent_module_name` → empty results or error without clear message.
- `"fields"` key missing from `query_value` → error.
- Field display label instead of API name in `"fields"` → null values silently.
- Specifying `<connection>` without first specifying `<query_value>`, `<page>`, and `<per_page>` → ordering failure.
- Retrieve `sub_module_record_id` from this response before calling zoho.crm.v8.updateRelatedRecord; do not assume sub-record IDs match parent IDs.

RELATED_DOCS:
- Zoho CRM API V8 — Get Related Records — https://www.zoho.com/deluge/help/crm/get-related-records-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/get-related-records-V8.html
