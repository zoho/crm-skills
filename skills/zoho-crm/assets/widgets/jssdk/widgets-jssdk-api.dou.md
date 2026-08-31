FILE_PURPOSE: Read when calling `ZOHO.CRM.API.*` from a Widget to read, write, search, attach, or delete CRM records under the logged-in user's auth.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_API
TRIGGER_KEYWORDS: ZOHO.CRM.API, getRecord, getAllRecords, insertRecord, updateRecord, upsertRecord, deleteRecord, searchRecord, coql, attachFile, addNotes

TECHNICAL_CONSTRAINTS:
- All `ZOHO.CRM.API.*` calls return a Promise resolved with the v2 CRM API response envelope (`{ data: [...], info: {...} }`); reject path is not detailed in source — wrap in `.catch` / try / await.
- Read methods: `getRecord`, `getAllRecords`, `getRelatedRecords`, `getUser`, `getAllUsers`, `getProfile`, `getAllProfiles`, `getApprovalById`, `getApprovalRecords`, `getApprovalsHistory`, `getOrgVariable`, `getBluePrint`, `getFile`, `getAllActions`, `searchRecord`, `coql`.
- Write methods: `insertRecord`, `updateRecord`, `upsertRecord`, `deleteRecord`, `attachFile`, `uploadFile`, `addNotes`, `delinkRelatedRecord`, `updateRelatedRecords`, `approveRecord`, `updateBluePrint`, `updateProfile`.
- `Entity` is the module's API name (`Contacts`, `Leads`, custom-module API name) — never the singular / plural display label.
- `searchRecord` `Type` accepts `email | phone | criteria | word`; `Query` shape depends on type (raw string for `email`/`phone`/`word`, criteria expression for `criteria`).
- `coql` body keyed `select_query`, value is the COQL SELECT string — column list must use API names; cross-module joins follow COQL grammar.
- `getAllRecords` defaults to `per_page=200`; pagination is caller responsibility (loop `page` until `info.more_records === false`).
- Calls execute under the logged-in user's OAuth context — no token / scope passed by the caller; resource visibility follows that user's profile + sharing.
- Source does **not** document a per-call rate limit at the Widget layer — limits are the host org's CRM API daily quota.

REQUIRED_PARAMETERS:
- `getRecord({ Entity, RecordID })` — both strings.
- `getAllRecords({ Entity, sort_order?, per_page?, page?, fields?, ... })` — `Entity` mandatory.
- `insertRecord({ Entity, APIData })` — `APIData` is an array of record objects keyed by field API name.
- `updateRecord({ Entity, APIData })` — each `APIData[i]` requires `id` plus updatable API-named fields.
- `upsertRecord({ Entity, APIData })` — uses duplicate-check fields defined on the module to match-or-create.
- `deleteRecord({ Entity, RecordID })`.
- `searchRecord({ Entity, Type, Query })`.
- `coql({ select_query })`.
- `attachFile({ Entity, RecordID, File })`; `uploadFile` follows similar shape; `addNotes({ Entity, RecordID, Title?, Content })`.
- `approveRecord({ Entity, RecordID })` for queued approval records.
- `getRelatedRecords({ Entity, RecordID, RelatedListAPIName })`; `delinkRelatedRecord` mirrors that signature.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- `Entity: "Contact"` (singular display label) passed instead of `"Contacts"` (module API name): API returns `INVALID_MODULE` / empty data — `label-vs-api-name`.
- `APIData` keys use display labels (e.g. `"Last Name"`) instead of API names (`Last_Name`): field silently ignored, record created with the field unset.
- `updateRecord` payload object missing `id` key: API rejects or upserts unexpectedly — always include `id` for update.
- `searchRecord` `Type: "criteria"` with an unescaped paren / colon inside `Query` value: query parser fails silently with empty result — escape per CRM criteria grammar.
- `coql` SELECT list addressed by display label rather than API name: `INVALID_QUERY` 400.
- Widget-runtime writes do not surface a `trigger` knob in source — all writes fire the full workflow / blueprint / approval stack; cannot suppress automation from `ZOHO.CRM.API`.
- `getAllRecords` consumer that does not loop on `info.more_records`: silently truncates dataset at page 1 (200 rows).
- `attachFile` / `uploadFile` invoked against a module where the Files related-list is hidden by profile: returns success but file is not attached visibly — verify the related-list visibility per profile.
- `insertRecord` for a record violating a layout-level mandatory field: returns 400 — pre-validate against [widgets-jssdk-meta.dou.md](./widgets-jssdk-meta.dou.md) `getFields`.
- `coql` SELECT exceeding the documented row cap (see [widgets-zrc-reference.dou.md](../widgets-zrc-reference.dou.md) for ceiling): silently truncated — page via `LIMIT` + `OFFSET`.
- `upsertRecord` against a module with no duplicate-check fields defined: every call creates a new record instead of upserting.
- Cross-module joins in `coql` against a module the logged-in user lacks read access to: rows filtered silently — no warning that visibility, not query, caused the omission.
- `getApprovalRecords` / `getApprovalsHistory` consumer assumes single-page response: long approval queues paginate — honour `info.more_records`.
- `getFile` invoked for an attachment behind sharing rules the user lacks: returns 401 without body — surface to the caller, do not retry.
- `addNotes` payload without `Content`: API accepts but creates an empty note — require non-empty `Content` at the caller.
- `delinkRelatedRecord` invoked without the `RelatedListAPIName` matching the module schema (e.g. `"Deals"` vs `"Potentials"`): silently no-ops — read related-list API name from [widgets-jssdk-meta.dou.md](./widgets-jssdk-meta.dou.md) `getRelatedList`.
- `approveRecord` called against a record not in an approval queue for the current user: returns approval-not-pending error — pre-check via `getApprovalRecords`.
- `getOrgVariable` requested by display label rather than variable API name: returns null — `label-vs-api-name`.
