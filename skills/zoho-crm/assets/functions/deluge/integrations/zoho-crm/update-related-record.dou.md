FILE_PURPOSE: zoho.crm.v8.updateRelatedRecord — update a submodule record related to a CRM parent record
MENTAL_MODEL: zoho.crm.v8.updateRelatedRecord(sub_mod, sub_id, parent_mod, parent_id, values, conn) → modification KEY-VALUE

WHEN_TO_USE:
- Update a field on a specific related record in a CRM submodule (e.g. Price_Books under Products).

WHEN_NOT_TO_USE:
- Updating the parent module record itself — use zoho.crm.v8.updateRecord.
- Fetching related records — use zoho.crm.v8.getRelatedRecords.

TRIGGER_KEYWORDS:
zoho.crm.v8.updateRelatedRecord, sub_module, sub_module_record_id, parent_module_record_id, INVALID_DATA, Price_Books

RULES:
- Syntax: response = zoho.crm.v8.updateRelatedRecord(sub_module, sub_module_record_id, parent_module, parent_module_record_id, values, connection);
- All 6 parameters are positional; `<connection>` is optional but must maintain position.
- Supported submodule-parent relation pairs are defined in Zoho CRM API V8 documentation; not all pairs are valid.
- Retrieve `sub_module_record_id` from a prior zoho.crm.v8.getRelatedRecords response.
- No `options_map`/trigger parameter — automation trigger behavior is not controllable for related-record updates.
- Each execution consumes one external API call.

CANONICAL_EXAMPLES:
```deluge
response = zoho.crm.v8.updateRelatedRecord("Price_Books", 2303XXXXXXXXXXXXXXX, "Products", 4770XXXXXXXXXXXXXXX, {"list_price":200});
```

FAILURE_MODES:
- `INVALID_DATA`: sub_module_record_id or parent_module_record_id is invalid; error message does not indicate which ID is wrong.
- Swapping sub_module and parent_module arguments (or their IDs) → `INVALID_DATA` without clear indication.
- Field display label instead of API name in `values` → silent wrong-field write.
- Unsupported submodule-parent pair → error; verify supported relations in CRM API V8 docs.

RELATED_DOCS:
- Zoho CRM API V8 — Update Related Records — https://www.zoho.com/deluge/help/crm/update-related-record-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/update-related-record-V8.html
