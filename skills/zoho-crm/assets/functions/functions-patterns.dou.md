## FILE_PURPOSE
Read when implementing a common Deluge coding pattern for CRM Functions.

## MENTAL_MODEL
Six recurring patterns cover the most common Deluge use cases. Each pattern is self-contained; link out to operation-specific DOU nodes for API signatures — do not duplicate them here.

## WHEN_TO_USE
- Implementing a multi-step Deluge coding pattern (fetch → transform → write, guard clause, loop, etc.).
- Building a two-step cross-module retrieval when a polymorphic field blocks COQL WHERE filtering.

## WHEN_NOT_TO_USE
- Looking up individual `zoho.crm.v8.*` method signatures — use `integrations/zoho-crm/*.dou.md` instead.
- Looking up `invokeurl` syntax — use [invokeurl-task.dou.md](./deluge/integrations/invokeurl-task.dou.md) instead.

## TRIGGER_KEYWORDS
read-then-write, guard-clause, loop-update, bulk-create-pattern, two-step-retrieval, polymorphic-activity, Who_Id, external-api-store

## RULES
- Always guard record IDs before `.toLong()` — check for `null` and blank first.
- Always check `zoho.crm.v8.*` response for `null` and `status == "failure"` before accessing fields.
- Use `trim()` on merge variable inputs before empty checks — merge variables can deliver whitespace-only strings.
- External API calls: use `invokeurl` with a named Connection; do not hardcode auth tokens.
- All field and module references: use API names — never display labels.

## CANONICAL_EXAMPLES

### Pattern 1: Read-then-write
Fetch a related record's field value, then use it to update the current record.

```deluge
account_id = input.Account_Name.get("id");
queryData = Map();
queryData.put("fields", "Industry,Annual_Revenue");
account = zoho.crm.v8.getRecordById("Accounts", account_id, queryData);
if (account != null && account.get("status") != "failure")
{
    industry = account.get("Industry");
    updateMap = Map();
    updateMap.put("Description", "Industry: " + industry);
    zoho.crm.v8.updateRecord("Contacts", input.id, updateMap);
}
```

### Pattern 2: External API and store result
Call an external REST endpoint via `invokeurl`, parse the response, then create or update a CRM record.

```deluge
response = invokeurl
[
    url: "https://api.example.com/company?domain=acme.com"
    type: GET
    connection: "example_connection"
];
company_data = response.toMap();
leadInfo = Map();
leadInfo.put("Company", company_data.get("name"));
leadInfo.put("No_of_Employees", company_data.get("employees"));
zoho.crm.v8.createRecord("Leads", leadInfo);
```

### Pattern 3: Conditional guard clause
Return early if prerequisite conditions are not met. Keeps the main logic unindented and readable.

```deluge
if (input.Email == null || input.Email.trim().length() == 0)
{
    info "Email required. Exiting.";
    return;
}
if (input.Lead_Status != "New")
{
    info "Not a new lead. Skipping.";
    return;
}
// main logic below — only reached when all guards pass
```

### Pattern 4: Loop over search results and update
Search records by criteria, iterate, and update each matching record.

```deluge
criteria = "(Account_Name:starts_with:Acme)";
contacts = zoho.crm.v8.searchRecords("Contacts", criteria, 1, 200);
for each contact in contacts
{
    contactId = contact.get("id");
    if (contactId != null)
    {
        updateMap = Map();
        updateMap.put("Lead_Source", "Partner");
        zoho.crm.v8.updateRecord("Contacts", contactId.toLong(), updateMap);
    }
}
```

### Pattern 5: Bulk create with trigger automation
Create multiple records in one call, explicitly controlling which automations run.

```deluge
createList = List();
record1 = Map();
record1.put("Last_Name", "Smith");
record1.put("Company", "Acme");
record2 = Map();
record2.put("Last_Name", "Jones");
record2.put("Company", "Beta");
createList.add(record1);
createList.add(record2);
optionMap = Map();
optionMap.put("trigger", {"workflow", "approval"});  // explicit subset — omit to run CRM defaults
response = zoho.crm.v8.bulkCreate("Leads", createList, optionMap);
```

### Pattern 6: Two-step cross-module retrieval
Use when a polymorphic Multi-Module Lookup field (e.g. `Who_Id` on Tasks/Calls/Events) cannot be filtered in a COQL WHERE clause. Decompose into two steps: fetch parent records, then fetch related sub-records per parent.

```deluge
// Goal: get all open Tasks for Contacts belonging to a given Account
// Who_Id cannot be used in COQL WHERE — use two-step approach

// Step 1 — fetch Contacts for the Account via searchRecords
contactList = zoho.crm.v8.searchRecords("Contacts", "(Account_Name:equals:" + accountId + ")", 1, 200);
if (contactList == null || contactList.size() == 0) { return; }

// Step 2 — for each Contact, fetch related Tasks
for each contact in contactList
{
    contactId = contact.get("id").toLong();
    // v2 syntax — for new code prefer zoho.crm.v8.getRelatedRecords where available
    taskList = zoho.crm.getRelatedRecords("Tasks", "Contacts", contactId, 1, 200);
    for each task in taskList
    {
        if (ifnull(task.get("Status"), "") != "Completed")
        {
            // process open task
        }
    }
}
```

> **v2 vs v8 note for Pattern 6**: `zoho.crm.getRelatedRecords` (v2, 5 params) is shown above for existing code compatibility. For new code, prefer `zoho.crm.v8.getRelatedRecords(relation_name, parent_module, parent_id, query_data, page, per_page, connection)` (v8, 7 params with `query_data` map requiring `"fields"` key). See [get-related-records.dou.md](./deluge/integrations/zoho-crm/get-related-records.dou.md).

## FAILURE_MODES
- Pattern 6: `Who_Id` is a polymorphic Multi-Module Lookup — cannot be filtered in COQL WHERE (neither `->` traversal nor `IN` subquery supported for this field). Use the two-step approach.
- Pattern 5: `optionMap.put("trigger", {})` (empty collection literal) suppresses ALL automations silently — pass an explicit subset (e.g. `{"workflow", "approval"}`) or omit `options_map` to run CRM defaults.
- Pattern 3: `input.Email.length() == 0` without `trim()` passes whitespace-only strings — always `trim()` merge variable inputs before empty checks.
- Pattern 2: `company_data.get("name")` on a failed `invokeurl` response returns `null` — check `response` is not null and does not contain an error key before accessing nested fields.

## RELATED_DOCS
- Function category boilerplate → [functions-categories.dou.md](./functions-categories.dou.md)
- getRelatedRecords v8 → [get-related-records.dou.md](./deluge/integrations/zoho-crm/get-related-records.dou.md)
- invokeurl task → [invokeurl-task.dou.md](./deluge/integrations/invokeurl-task.dou.md)
- bulkCreate → [bulk-create-records.dou.md](./deluge/integrations/zoho-crm/bulk-create-records.dou.md)

## SOURCE
https://www.zoho.com/crm/developer/docs/functions/guides.html
