FILE_PURPOSE: Read when building multi-function pipelines, migrating Workflow Rules to Functions, or implementing bulk-record pagination and chunking.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/functions/guides.html
TRIGGER_KEYWORDS: pipeline-controller-pattern, workflow-rule-migration, sandbox-promotion-steps, bulk-pagination-coql, cursor-based-chunking, searchRecords-200-cap, bulkUpdate-100-cap

TECHNICAL_CONSTRAINTS:
- Inline function calling (`standalone.FunctionName()`) is Deluge-only — Java, Node.js, and Python do not support this syntax.
- Java/Node.js/Python pipeline alternatives: (a) shared helper class/module in a multifile project, (b) chained Workflow Rules, (c) ZRC REST call to the other Function's endpoint.
- `zoho.crm.searchRecords` returns a maximum of 200 records per call — no error or warning when the result is truncated.
- `zoho.crm.bulkUpdate("Module", updateList)` processes up to 100 records per call — chunk lists to ≤100 before calling.
- Controller Function timeout includes all chained Standalone Function execution time — Automation category total: 30 seconds; Scheduled: 15 minutes.
- Button/REST API timeout: 10 seconds — not suitable for bulk processing; trigger a Scheduled Function asynchronously instead.
- Deluge has no `while` loop — paginate using `for each` over `maxPages.toList()` (e.g. `50.toList()` creates list [0..49]).
- COQL pagination: `SELECT id FROM Module WHERE ... LIMIT <pageSize> OFFSET <offset>`; offset = `pageNum * pageSize`; extract records via `result.get("data")`.
- Bulk processing strategy by dataset size:
  - < 100 records — any category; single `bulkUpdate` call.
  - 100–2,000 records — Automation (30s) or Schedule (15min); paginated fetch + `bulkUpdate` in one execution.
  - 2,000–10,000 records — Schedule (15min); paginated + `bulkUpdate` with timeout monitoring.
  - 10,000+ records — Schedule (15min, repeated); chunking across runs with CRM Variable cursor.
  - Button/REST API (10s) — do not use for bulk; return a summary and trigger async via Scheduled Function.
- Cursor-based chunking: read via `zoho.crm.getOrgVariable("Bulk_Update_Cursor").toLong()`; advance via `zoho.crm.updateOrgVariable("Bulk_Update_Cursor", newCursor.toString())`; reset to "0" when no more records.
- During Workflow Rule migration, run old rules and new Function in parallel — disable old rules only after confirming the Function handles all cases correctly.

REQUIRED_PARAMETERS:
- Controller Function: argument (e.g. `dealId`) must be mapped to a merge variable (e.g. `${Deals.Id}`) in the Workflow Rule action — not in the Function editor.
- `bulkUpdate` updateList: LIST of MAPs; each MAP must include key `"id"` plus the fields to update.
- COQL exit condition: `break` when `records == null || records.size() == 0` or `records.size() < pageSize`.
- Cursor bootstrap guard: `cursor = if(cursorStr != null && cursorStr != "", cursorStr.toLong(), 0)`.
- Sandbox promotion batch: select Function + associated Workflow Rules + dependent custom fields/modules together in the promotion interface.

UI_ONLY_ACTIONS:
- `Setup → Automation → Workflow Rules` → New Rule → Action → Call Function → select function + map arguments.
  Note: No API equivalent for attaching a Function to a Workflow Rule — UI-only.
- `Setup → Data Administration → Sandbox` → Create Sandbox or Refresh to sync the latest production configuration.
  Note: No API equivalent — UI-only.
- Sandbox promotion interface → select components (Function + rules + fields) → review summary → promote.
  Note: No API equivalent for sandbox-to-production promotion — UI-only.
- `Setup → Developer Space → Connections` → verify and re-authenticate each Connection post-promotion.
  Note: No API equivalent for Connection credential re-authentication — UI-only.

CRITICAL_FAILURE_MODES:
- `standalone.FunctionName()` invoked in Java/Node.js/Python → not supported → compilation or runtime failure.
- Pipeline timeout: entire chain aborts if any step exceeds the controller's Automation 30-second total; a slow external API call fails the whole pipeline.
- `searchRecords` silently caps at 200 records — no error raised; records beyond 200 are dropped without warning.
- `bulkUpdate` with list > 100 records — source does not specify behavior beyond limit; always chunk to ≤100.
- `for each` without `break` on empty page iterates all `maxPages` iterations unnecessarily — always `break` when `records.size() == 0`.
- Post-promotion: Connections require re-authentication in production — credentials are not carried over from Sandbox.
- Post-promotion: CRM Variables in Sandbox hold staging values (staging API URLs, test org IDs) — verify and update production values immediately after promotion.
- Running old Workflow Rules and new Function in parallel during migration: if both write the same field on the same record simultaneously, double-execution corrupts data.
- Cursor advances past failed records if Scheduled Function errors mid-run without resetting — implement `catch` with cursor reset before updating the cursor variable.
- Workflow Rules fail silently by default — if the Function needs to send failure alerts, it must implement this explicitly via `sendmail` or equivalent.
