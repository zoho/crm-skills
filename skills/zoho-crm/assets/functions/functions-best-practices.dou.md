FILE_PURPOSE: Read when designing production-quality CRM Functions — idempotency, credential hygiene, performance, logging discipline, and naming conventions.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/functions/best-practices.html
TRIGGER_KEYWORDS: idempotency-guard, single-responsibility, crm-variable-config, standalone-fn-reuse, connection-least-privilege, batch-over-loop, sandbox-first-workflow

TECHNICAL_CONSTRAINTS:
- Category timeout hard limits (non-configurable): Button/Validation/Related List/REST API = 10s; Automation = 30s; Scheduled = 15min.
- Deluge: no `for` or `while` loops — only `for each` over lists, maps, or JSON collections; batch patterns required for multi-record operations.
- `standalone.FunctionName()` inline calling is Deluge-only — Java/Node.js/Python alternatives: ZRC REST call to the Function's endpoint, shared helper class/module, or chained Workflow Rules.
- Java/Node.js/Python: every deploy creates a revision — full version history available; Deluge editor also saves a revision snapshot on every save.
- Workflow Rules do not propagate errors to users — Functions triggered by Workflow Rules must implement their own alerting/retry logic via `sendmail` or equivalent.
- `zoho.crm.getOrgVariable("VarName")` in Deluge; access org variables via ZRC in Java/Node.js/Python.
- Java/Node.js/Python Functions: use `config.json` for environment-specific values (sandbox vs production endpoints, feature flags).
- Connection data access is scoped to the authenticated user of the Connection — admin-level CRM operations require a Connection authenticated by an admin user.
- Standalone Functions can be called from other Deluge Functions via `standalone.FunctionName(arg)` and exposed as a REST API — they are the primary reuse mechanism.
- Log output persists at `Setup → Developer Hub → Functions → [Name] → Logs` — CRM logs are the primary debugging surface for all categories.
- Button/Related List/Validation Rule Functions surface return values to the user — error handling in these categories must return a user-readable message, not only log.
- Every Function execution is isolated — a misbehaving execution cannot impact other Functions or the core CRM platform.
- One Connection per integration purpose — sharing a Connection across unrelated Functions means credential rotation or revocation breaks all dependents simultaneously.
- Restrict Manage Extensibility in production to admins — developers work only in Sandbox to prevent accidental live changes.

REQUIRED_PARAMETERS:
- Idempotency guard: `existing = zoho.crm.searchRecords("Module", "(External_ID:equals:" + extId + ")"); if(existing.size() == 0) { /* safe to create */ }`.
- CRM Variable for configurable URL: `baseUrl = zoho.crm.getOrgVariable("Sync_API_Base_URL"); resp = invokeurl [url: baseUrl + "/endpoint" type: POST ...];`.
- Deluge inline call: `result = standalone.FunctionName(arg1, arg2);` — called Function must be of category Standalone.
- Batch fetch pattern (Deluge): `allRecords = zoho.crm.searchRecords("Module", "(id:in:" + idList.toString(",") + ")");` — avoids per-record API call inside `for each`.
- Java/Node.js/Python batch: COQL `SELECT Last_Name, Email FROM Leads WHERE id IN (...)` via ZRC POST to `/crm/v7/coql`.
- Background trigger error handling (Deluge): `try { /* operation */ } catch(e) { info "Failed: " + e.toString(); sendmail [from: zoho.adminuserid to: zoho.adminuserid subject: "Failure" message: e.toString()]; }`.
- Logging entry/exit (Deluge): `info "Function started — " + recordId;` then `info "API status: " + resp.get("status_code");`.
- Connection naming convention: `ServiceName_Purpose` (e.g. `Cliq_Notifications_Bot`, `ERP_Order_Sync`); append environment suffix when maintaining separate sandbox/production Connections.

UI_ONLY_ACTIONS:
- `Setup → Developer Hub → Functions` — all Function creation, editing, execution, log review, and schedule management.
  Note: No API equivalent for Function creation or log access — UI-only.
- `Setup → Developer Space → Connections` — create Connections with required OAuth scopes; name by service + purpose; one Connection per integration.
  Note: No API equivalent for Connection credential authentication — UI-only.
- Restrict Manage Extensibility: `Setup → [Administration] → Profiles` → edit profile → remove Functions access in production.
  Note: See Security — Permissions at /crm/developer/docs/functions/security.html#permissions-who-can-access-functions.

CRITICAL_FAILURE_MODES:
- Automation/Blueprint/Scheduled triggers may fire multiple times for the same record (retry, re-trigger) — Functions without idempotency guards produce duplicate records or double-sent notifications.
- Hardcoded API URLs or record IDs break on sandbox promotion — sandbox staging URLs and shifted IDs carry over to production; use CRM Variables.
- `standalone.FunctionName()` called from Java/Node.js/Python → not supported → compilation or runtime failure.
- API calls inside `for each` loop → N individual calls → hits category timeout or CRM API rate limits; batch fetch instead.
- Sharing one Connection across unrelated Functions → credential rotation or revocation breaks all dependent Functions simultaneously.
- PII (emails, phone numbers) or credentials logged via `info()` → exposed in CRM Logs tab — log status codes and record IDs only.
- Developing directly in production → changes go live immediately with no rollback — always use Sandbox.
- Function declared as void (e.g. Automation) but caller expects a return value — Automation return is discarded; verify return semantics per category before relying on a return value.
- Empty `catch` block with no logging → silent failure with no trace in logs — always include `info "Failed: " + e.toString()` in every catch.
- Workflow Rule trigger fires Function before the record save is committed — reading a triggered field may return the pre-save value; use mapped arguments rather than fetching the record inside the Function.
- Circular Standalone calls (Function A calls A, or A → B → A) → infinite recursion; no runtime recursion guard is documented — design must explicitly prevent circular call chains.
- CRM Variables edited in Sandbox hold sandbox-specific values — after promotion, always audit production CRM Variables for staging URLs, test thresholds, or disabled flags before going live.