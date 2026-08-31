FILE_PURPOSE: Read when mutating a single record instance via its `__`-prefixed instance methods (`record.__update`, `__remove`, `__addTags`, `__sendMail`, …) instead of the module-level facade.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/webapi_v2/Records
TRIGGER_KEYWORDS: __update, __create, __remove, __convert, __addTags, __removeTags, __fetchRelatedRecords, __delinkRelatedRecords, __updateRelatedRecords, __fetchBlueprint, __approveRecord, __sendMail, __getFeatureSpecificInfo, Owner

TECHNICAL_CONSTRAINTS:
- Instance-method surface lives on every record object returned by `ZDK.Apps.CRM.<Module>.fetchById(...)` / `.fetch(...)`.
- Also on every newly-constructed `new ZDK.Apps.CRM.<Module>.Models.<Module>()` instance.
- Methods are double-underscore-prefixed (`__create`, `__update`, `__remove`, etc.) to namespace them off the field accessors.
- Method semantics mirror the module-facade method one-for-one, but operate on the instance's own `id`.
- No separate `record_id` parameter required for `__update`, `__remove`, `__fetchRelatedRecords`, `__fetchBlueprint`, `__sendMail`.
- Lookup fields expose two access modes — scalar `<Lookup>_Lookup_Id` and method `<Lookup>(userObject?)`.
- Calling the lookup method with no arg fires an API call to hydrate the lookup object.
- Calling the lookup method with a model object reassigns the lookup in memory; persist with `__update`.
- Each method wraps the same v2 REST endpoint as its module-facade counterpart (`insert-records`, `update-records`, `delete-records`, `convert-lead`, `add-tags`, `remove-tags`, `get-related-records`, `delink`, `update-related-records`, `blueprint-details`, `v2.1/send-mail`).
- Returns are sync arrays / `CRMResponses` objects — not Promises.
- Source does not enumerate OAuth scope, edition gating, or rate-limit caps for the instance methods — inherited from the underlying v2 REST endpoint.

REQUIRED_PARAMETERS:
- Source samples (verbatim) live at SOURCE_DOC under each method heading; re-fetch when authoring a non-trivial payload (Mail / ConvertLeads / Related_Records) not fully described by the bullets below.
- `Owner(userObject?: Users)` — no-arg form returns the hydrated owner record; arg form assigns a new owner (then `__update` to persist). Scalar shortcut `record.Owner_Lookup_Id` reads/writes only the id.
- `__create()` — call on an instance built from `new ZDK.Apps.CRM.<Module>.Models.<Module>()` with fields assigned; returns array.
- `__update()` — call on an instance whose `id` is set (typically from `fetchById`); returns `CRMResponses`.
- `__remove()` — delete the record by its own `id`; returns `CRMResponses`.
- `__convert(object: ConvertLeads)` — Leads only; `object` built from `new ZDK.Apps.CRM.Leads.Models.ConvertLeads()` with optional `Accounts` id and nested `Deals` object.
- `__addTags(arrayOfTagNames: Array<String>)` · `__removeTags(arrayOfTagNames: Array<String>)`.
- `__fetchRelatedRecords(related_list_api_name: String)` — returns related-records array.
- `__delinkRelatedRecords(related_list_api_name: String, array_of_related_record_ids: Array<String>)`.
- `__updateRelatedRecords(record: Related_Records, related_list_api_name: String, id: String)` — mutate an element from `__fetchRelatedRecords`, then pass it back with its related-record id.
- `__fetchBlueprint()` — returns `Blueprint` object for this record.
- `__approveRecord(action: String, comment: String)` — `action` ∈ `"approve" | "delegate" | "reject"`; instance must have `id` set (can be a fresh model with `lead.id = "..."`); response carries `.status`.
- `__sendMail(mailObject: Mail)` — `mailObject` built from `new ZDK.Apps.CRM.__Actions.Models.Mail()` with `from {user_name,email}`, `to [{user_name,email}]`, `subject`, `content`, `mail_format`.
- `__getFeatureSpecificInfo(features: Array<String>)` — `features` from `{blocked_emails, consecutive_negative_emails, unsubscribed_emails}`; source caps at 5 features per call; response `[0]._features_info` carries the per-feature array.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- Calling `__update` / `__remove` / `__fetchRelatedRecords` / `__fetchBlueprint` / `__approveRecord` / `__sendMail` on an instance whose `id` is unset → API returns id-required / not-found error.
- Building an instance via `new …Models.<Module>()` without assigning `id` then calling `__update` → same id-missing failure (mirrors the module-facade `update` path).
- Reassigning a lookup via `record.Owner(newUser)` and forgetting the trailing `__update()` → in-memory change only; not persisted — silent no-op against CRM.
- Mixing scalar `Owner_Lookup_Id` write with a subsequent `Owner(otherUser)` method call before `__update` → the method-form wins and overwrites the scalar; ordering ambiguity.
- Calling `Owner()` no-arg in a loop → fires one extra API call per iteration.
- Prefer batch hydration via [clientscript-webapi-settings.dou.md](./clientscript-webapi-settings.dou.md) or module facade `fetchById` when resolving many owners.
- `__convert` invoked on an already-converted Lead → API returns conversion-not-allowed; pre-check `Converted` state.
- `__updateRelatedRecords` with the wrong `related_list_api_name` for the module (e.g. `"Deals"` on a module that exposes `"Potentials"`) → silently no-ops.
- Resolve `related_list_api_name` via [clientscript-webapi-settings.dou.md](./clientscript-webapi-settings.dou.md) `fetchRelatedLists`.
- `__sendMail` payload missing `mail_format` → API rejects.
- `__sendMail` payload missing `from` or `to` entries → API rejects malformed-mail.
- `__getFeatureSpecificInfo` invoked with > 5 features (source-stated cap) → request-too-large error.
- Instance-method writes have no `trigger` knob in source — every `__create` / `__update` / `__remove` / `__convert` fires the full workflow / blueprint / approval / scoring / orchestration stack — `automation-interaction`.
- Field assignment via display-label key on the instance (`lead["Last Name"]`) instead of API name (`lead.Last_Name`) before `__update` → field silently unset on persist — `label-vs-api-name`.
- Source does not enumerate error codes.
- Inspect returned `CRMResponses` `.status` / `.code` / `.message` and the underlying v2 REST endpoint's docs for each method.
