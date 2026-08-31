FILE_PURPOSE: Read when calling `ZDK.Apps.CRM.<Module>.*` from a ClientScript to fetch, create, update, upsert, delete, search, convert, tag, mail, or approve module records.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/webapi_v2/Modules
TRIGGER_KEYWORDS: ZDK.Apps.CRM.Leads.fetch, ZDK.Apps.CRM.<Module>.create, fetchById, upsert, deleteByIds, searchByCriteria, fetchRelatedRecords, convert, approveRecord, sendMail, addTagsToRecords

TECHNICAL_CONSTRAINTS:
- Surface is the per-module facade exposed at `ZDK.Apps.CRM.<Module_API_Name>` inside a ClientScript runtime; module token must be the module API name (`Leads`, `Contacts`, `Invoices`, `Price_Books`, `Events`, `Notes`, custom-module API name) — never the display label.
- Each method wraps a documented Zoho CRM v2 REST endpoint — `Reference API` links from source point to `zoho.com/crm/developer/docs/api/v2/{get-records,insert-records,update-records,upsert-records,delete-records,get-deleted-records,convert-lead,search-records,get-related-records,delink,update-related-records,blueprint-details,add-tags,remove-tags,tag-record-count}.html` and `v2.1/send-mail.html`.
- Calls are synchronous from script perspective — return value is the response array / object directly (e.g. `var leads = ZDK.Apps.CRM.Leads.fetch();`), not a Promise.
- Record creation requires `new ZDK.Apps.CRM.<Module>.Models.<Module>()`; picklist fields must be assigned from `ZDK.Apps.CRM.<Module>.Models.<Field>Picklist.<MEMBER>` (e.g. `Lead_StatusPicklist.CONTACTED`, `StagePicklist.CLOSED_WON`, `Pricing_ModelPicklist.FLAT`).
- Inventory modules require nested `Line_Items` built from `ZDK.Apps.CRM.<Module>.Models.Line_Items`; `Price_Books` requires nested `Pricing_Details`; `Events` requires nested `Participants`; `Notes` requires `Parent_Id_Lookup_Id` + `$se_module`.
- `getFeatureInfo` hard caps documented in source: max 100 record ids per call, max 5 feature names per call.
- Source does not enumerate OAuth scopes, edition gating, rate limits, or HTTP error codes for these helpers — bound to the underlying v2 REST endpoint's scope and quota; consult the linked `Reference API` page per method.

REQUIRED_PARAMETERS:
- `fetch(page?, per_page?, sort_by?, sort_order?)` — all optional; `sort_by` is field API name; `sort_order` ∈ `"asc" | "desc"`. Returns array.
- `fetchById(id: String)` — returns single record object of module type.
- `create(arrayOfObjects | singleObject)` — payload built via `Models.<Module>` constructor; returns array.
- `update(arrayOfObjects | singleObject)` — each object must carry `id`; built by mutating a `fetchById` result.
- `updateById(arrayOfObjects | singleObject, record_id: String)` — explicit id form; returns `CRMResponses`.
- `upsert(arrayOfObjects | singleObject)` — duplicate match driven by module's configured duplicate-check fields.
- `deleteByIds(ids: Array<String>)` — bulk delete; returns array.
- `fetchDeletedRecords()` — returns deleted-records array.
- `convert(convertLeads: ConvertLeads, id: String)` — Leads only; `ConvertLeads` model carries optional `Accounts` (id string) + nested `Deals` object built from `ZDK.Apps.CRM.Deals.Models.Deals`.
- `searchByCriteria(criteria: String)` — criteria expression per CRM search-records grammar, URL-percent-encoded (commas as `%5C%2C`).
- `searchByEmail(email: String)` · `searchByPhone(phone: String)` · `searchByWord(word: String)` — single-string queries.
- `fetchRelatedRecords(id: String, related_list_api_name: String)` — `related_list_api_name` is the related-list API name (e.g. `"Notes"`).
- `delinkRelatedRecords(id, related_list_api_name, array_of_related_record_ids: Array<String>)` and singular `delinkRelatedRecord(id, related_list_api_name, related_record_id: String)`.
- `updateRelatedRecords(related_record_object: Related_Records, record_id, related_list_api_name, related_record_id)` — mutate a `fetchRelatedRecords` element then pass it back.
- `fetchBlueprint(record_id: String)` — returns `Blueprint` object.
- `addTagsToRecord(record_id, array_of_tag_names: Array<String>)` and bulk `addTagsToRecords(array_of_tag_names, record_ids: Array<String>)`; mirror methods `removeTagsToRecord` / `removeTagsToRecords`.
- `sendMail(mail_object: Mail, record_id: Array<String>)` — `mail_object` built from `new ZDK.Apps.CRM.__Actions.Models.Mail()`; required fields `from {user_name,email}`, `to [{user_name,email}]`, `subject`, `content`, `mail_format` (e.g. `"text"`).
- `approveRecord(record_id: String, action: String, comment: String)` — `action` ∈ `"approve" | "delegate" | "reject"`; response carries `.status`.
- `getFeatureInfo(ids: Array<String>, features: Array<String>)` — `features` from `{blocked_emails, consecutive_negative_emails}`; response `[0]._features_info` is the per-record feature array.

- Source-sample payloads (verbatim from source) for the non-trivial shapes:

Invoices `create` (Line_Items via `product()` + `quantity`):

```javascript
var invoice = new ZDK.Apps.CRM.Invoices.Models.Invoices();
invoice.Subject = "testing2";
invoice.Account_Name_Lookup_Id = "2000000136022";
var line_item = new ZDK.Apps.CRM.Invoices.Models.Line_Items();
var product = ZDK.Apps.CRM.Products.fetchById("2000000136027");
line_item.product(product);
line_item.quantity = 3.0;
invoice.Product_Details = [line_item];
var response = ZDK.Apps.CRM.Invoices.create(invoice);
```

Price_Books `create` (`Pricing_Details` rows: `from_range` / `to_range` / `discount`):

```javascript
var book = new ZDK.Apps.CRM.Price_Books.Models.Price_Books();
book.Price_Book_Name = "test";
book.Pricing_Model = ZDK.Apps.CRM.Price_Books.Models.Pricing_ModelPicklist.FLAT;
var pricing_detail = new ZDK.Apps.CRM.Price_Books.Models.Pricing_Details();
pricing_detail.from_range = 10;
pricing_detail.to_range = 100;
pricing_detail.discount = 5;
book.Pricing_Details = [pricing_detail];
var response = ZDK.Apps.CRM.Price_Books.create(book);
```

Events `create` (`Event_Title` / `Start_DateTime` / `End_DateTime` / `Participants[].type`):

```javascript
var my_event = new ZDK.Apps.CRM.Events.Models.Events();
my_event.Event_Title = "testing";
my_event.Start_DateTime = "2020-10-22T21:00:00+05:45";
my_event.End_DateTime = "2020-10-24T21:00:00+06:45";
my_event.Currency = "USD";
var participant = new ZDK.Apps.CRM.Events.Models.Participants();
participant.participant = "423383000004997180";
participant.type = "lead";
my_event.Participants = [participant];
var response = ZDK.Apps.CRM.Events.create(my_event);
```

Notes `create` (`Note_Content` + `Parent_Id_Lookup_Id` + `$se_module`):

```javascript
var note = new ZDK.Apps.CRM.Notes.Models.Notes();
note.Note_Content = "create test";
note.Parent_Id_Lookup_Id = "2000000069181";
note.$se_module = "Leads";
var response = ZDK.Apps.CRM.Notes.create(note);
```

Leads `convert` (`ConvertLeads.Accounts` + nested `Deals.{Deal_Name, Closing_Date, Stage, Amount}`):

```javascript
var convertLead = new ZDK.Apps.CRM.Leads.Models.ConvertLeads();
convertLead.Accounts = "4312588000000296007";
var deal = new ZDK.Apps.CRM.Deals.Models.Deals();
deal.Deal_Name = "Convert";
deal.Closing_Date = "2020-11-20";
deal.Stage = ZDK.Apps.CRM.Deals.Models.StagePicklist.CLOSED_WON;
deal.Amount = 56.6;
convertLead.Deals = deal;
var response = ZDK.Apps.CRM.Leads.convert(convertLead, "4312588000000846005");
```

`sendMail` (`Mail` model shape):

```javascript
var mail = new ZDK.Apps.CRM.__Actions.Models.Mail();
mail.from = { "user_name": "james", "email": "james.cooper@zoho.com" };
mail.to = [{ "user_name": "john", "email": "john.carlton@zoho.com" }];
mail.subject = "Mail subject";
mail.content = "Content of the mail";
mail.mail_format = "text";
var response = ZDK.Apps.CRM.Leads.sendMail(mail, "423383000000015966");
```

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- Module token passed as display label (`"Lead"`, `"Price Books"`) instead of API name (`Leads`, `Price_Books`) → `ZDK.Apps.CRM.<label>` is undefined; `TypeError` at script load — `label-vs-api-name`.
- Field assignment using display label key (`record["Last Name"]`) instead of API-name property (`record.Last_Name`) → field silently unset on `create` / `update`; record persists with field empty — `label-vs-api-name`.
- Picklist field assigned a raw display string (`lead.Lead_Status = "Contacted"`) instead of the model enum (`Models.Lead_StatusPicklist.CONTACTED`) → CRM rejects with picklist-value-not-allowed at server side.
- `update(obj)` payload missing `id` (object not seeded from `fetchById`) → API rejects update; the helpers do not auto-upsert on missing id.
- `upsert` invoked against a module with no duplicate-check fields configured → every call inserts a new record instead of matching.
- `searchByCriteria` query containing unescaped `,`, `(`, `)`, `:` inside a value → criteria parser returns empty array silently; escape per CRM search grammar (commas as `%5C%2C`).
- `searchByEmail` / `searchByPhone` / `searchByWord` on records where the searched field is null → records skipped silently; no warning.
- `fetch()` consumer not iterating `page` until response is empty → silently truncated at default page (1, server-side `per_page` cap). Source does not state the cap.
- `convert(convertLead, id)` invoked against a Lead already converted → API returns conversion-not-allowed error; pre-check `Converted` state.
- `delinkRelatedRecords` / `updateRelatedRecords` with `related_list_api_name` mismatch (`"Deals"` vs module-specific `"Potentials"`) → silently no-ops; resolve the related-list API name via [clientscript-webapi-settings.dou.md](./clientscript-webapi-settings.dou.md) `fetchRelatedLists`.
- `sendMail` without `mail_format` → API rejects; without `from`/`to` entries → rejects with malformed-mail payload.
- `approveRecord` called on a record not in an approval queue for the script's invoker user → returns approval-not-pending error; pre-check via [clientscript-webapi-settings.dou.md](./clientscript-webapi-settings.dou.md) `fetchApprovalProcess`.
- `getFeatureInfo` invoked with > 100 record ids or > 5 features → source declares hard cap; exceeding it returns request-too-large error.
- Source does not surface a `trigger` map / automation-suppression knob — every `create` / `update` / `upsert` / `delete` / `convert` here fires the full workflow / blueprint / approval / scoring / orchestration stack; this surface cannot suppress automation — `automation-interaction`.
- Source does not enumerate error codes; surface failures by inspecting the returned `CRMResponses` `status` / `code` / `message` and the linked `Reference API` doc for each method.
