FILE_PURPOSE: zoho.crm.v8.convertLead — convert a Lead into Contact, Account, and optionally Deal from Deluge
MENTAL_MODEL: zoho.crm.v8.convertLead(lead_id, values_map, connection) → {Contacts:id, Deals:id|null, Accounts:id}

WHEN_TO_USE:
- Convert a Lead record into Contact and Account (default) and optionally a Deal.
- Link a converting Lead to existing Account/Contact records instead of creating new ones.

WHEN_NOT_TO_USE:
- Already-converted Leads — `ID_ALREADY_CONVERTED` error is returned.

TRIGGER_KEYWORDS:
zoho.crm.v8.convertLead, ID_ALREADY_CONVERTED, INVALID_DATA, Deal_Name, Closing_Date, overwrite, Deals

RULES:
- Syntax: response = zoho.crm.v8.convertLead(lead_id, values, connection);
- Prefer `Map()` + `.put(key, value)` for generated `values` payloads.
- Contact and Account created by default; provide existing IDs in `values` to link instead of creating.
- Deal only created if `"Deals"` key with mandatory fields (Deal_Name, Closing_Date, Stage) is in `values`.
- `"Accounts"` / `"Contacts"` keys in `values` → existing record ID to link.
- `"overwrite":true` in `values` → overwrites existing Account/Contact fields with Lead data.
- Each execution consumes one external API call.

CANONICAL_EXAMPLES:
```deluge
// Convert Lead and create a Deal
dealValues = Map();
dealValues.put("Deal_Name", "Jake");
dealValues.put("Closing_Date", "2018-12-06");
dealValues.put("Stage", "Closed Won");
valuesMap = Map();
valuesMap.put("Deals", dealValues);
response = zoho.crm.v8.convertLead(2303XXXXXXXXXXXXXXX, valuesMap);
// response: {"Contacts":"...","Deals":"...","Accounts":"..."}

// Link to existing Account and Contact
valuesMap = Map();
valuesMap.put("overwrite", true);
valuesMap.put("Accounts", "2303XXXXXXXXXXXXXXX");
valuesMap.put("Contacts", "2303XXXXXXXXXXXXXXX");
response = zoho.crm.v8.convertLead(2303XXXXXXXXXXXXXXX, valuesMap);
```

FAILURE_MODES:
- `INVALID_DATA`: lead_id is invalid or non-existent.
- `ID_ALREADY_CONVERTED`: lead has already been converted; cannot convert twice.
- `"Deals"` key absent from `values` → Deal is NOT created; `Deals` returns null in response with no error.
- Missing mandatory Deal fields (Deal_Name, Closing_Date, Stage) when `"Deals"` key is provided → conversion failure.
- `"overwrite":true` immediately overwrites existing Account/Contact data; irreversible without a separate update.

RELATED_DOCS:
- Zoho CRM API V8 — Convert Lead — https://www.zoho.com/deluge/help/crm/convert-lead-V8.html

SOURCE:
https://www.zoho.com/deluge/help/crm/convert-lead-V8.html
