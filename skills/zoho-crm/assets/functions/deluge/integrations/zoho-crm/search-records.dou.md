FILE_PURPOSE: zoho.crm.v8.searchRecords — search CRM module records by criteria string from Deluge
MENTAL_MODEL: zoho.crm.v8.searchRecords(module, criteria, page, per_page, search_value, connection) → list of record maps

WHEN_TO_USE:
- Find records matching field-value criteria (equals, not_equal, starts_with) in a CRM module.
- Filter records by converted/approved status via search_value parameter.

WHEN_NOT_TO_USE:
- Fetching all records without filtering — use zoho.crm.v8.getRecords.
- Known record ID lookup — use zoho.crm.v8.getRecordById.

TRIGGER_KEYWORDS:
zoho.crm.v8.searchRecords, INVALID_MODULE, INVALID_QUERY, criteria, equals, starts_with, not_equal, converted

RULES:
- Syntax: response = zoho.crm.v8.searchRecords(module_name, criteria, page, per_page, search_value, connection);
- Criteria format: `(<colName>:<operator>:<colValue>)`; compound: `((<col>:<op>:<val>) and (<col>:<op>:<val>) ...)`.
- Supported operators: `equals`, `not_equal`, `starts_with`; maximum 10 criteria per call.
- Default page: 1; default per_page: 200.
- `<page>` must be specified before `<per_page>`; both before `<search_value>`; all three before `<connection>`.

CANONICAL_EXAMPLES:
```deluge
// Search custom module by email
response = zoho.crm.v8.searchRecords("Prospects", "(Email:equals:john@zylker.com)");

// Search Accounts starting with A
response = zoho.crm.v8.searchRecords("Accounts", "(Account_Name:starts_with:A)");

// Extract record IDs
for each rec in response { info rec.get("id"); }
```

FAILURE_MODES:
- `INVALID_MODULE`: module API name is incorrect.
- `INVALID_QUERY`: malformed criteria (e.g. using `=` instead of `equals`). Response: `{"code":"INVALID_QUERY","details":{"reason":"invalid operator found"}}`.
- `not_equal` operator: records where specified field is null are NOT returned — silent omission.
- Field display label (e.g. `"Account Name"`) in criteria instead of API name (`"Account_Name"`) → `INVALID_QUERY`.
- Specifying `<search_value>` without first specifying `<page>` and `<per_page>` → ordering failure.

RELATED_DOCS:
- Zoho CRM API V8 — Search Records — https://www.zoho.com/deluge/help/crm/search-records-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/search-records-V8.html
