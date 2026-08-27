FILE_PURPOSE: Read when understanding CRM Functions architecture — categories, trigger types, execution lifecycle, and return type semantics per category.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/functions/overview.html, https://www.zoho.com/crm/developer/docs/functions/lifecycle.html
TRIGGER_KEYWORDS: functions-lifecycle, crmAPIRequest, crmAPIResponse, category-return-types, cold-start-latency, failure-rerun

TECHNICAL_CONSTRAINTS:
- Deluge: direct access to `zoho.crm.*` built-in namespace and native Zoho service connectors.
- Deluge input: arguments populated from field mappings using merge variables (e.g. `${Deals.Deal Name}`) configured at the association point — for HTTP calls, input arrives via `crmAPIRequest`.
- **Argument mapping (all trigger-based categories)**: Every argument declared in a Deluge function signature must be mapped to a CRM merge variable at the trigger's setup surface — unmapped arguments resolve to null at runtime with no error. Applies to Button, Automation, Related List, and Signals categories. Schedule takes no arguments. Standalone receives arguments from the caller. Validation Rule input arrives via `crmAPIRequest`.
- Cold start latency possible if runtime environment is not already warm from recent use — not caused by script logic; inherent runtime warm-up.
- Execution isolation: each run gets dedicated resource allocation — a misbehaving script cannot impact other Functions or the CRM platform.
- Every save creates a revision snapshot — previous versions are restorable from the editor without external tooling.
- Seven categories: Automation (Workflow Rules/Blueprints/Approvals), Button, Schedule, Standalone, Related List, Signals, Validation Rule.
- Return type per category: Automation/Schedule = void; Button = String (modal); Standalone = String; Related List = String (XML); Validation Rule = Map; Signals = signal notification.
- Category determines the allowed triggers, input shape, return type, and timeout — set at Function creation; cannot be changed post-creation.
- Function–trigger association is configured at the trigger's setup surface (Workflow Rule → Action, Blueprint → transition, Custom Button → setup) — NOT in the Function editor.
- Connections are resolved before script execution — credentials and tokens are injected automatically; the script does not handle authentication logic.
- `invokeurl` calls external third-party APIs via a Connection; `invokeAPI` calls other Zoho ecosystem APIs via a Connection.
- Failed executions are captured with error details and are manually rerunable from logs — without re-triggering the original event.
- Execution logs available at `Setup → Developer Hub → Functions → [Name] → Logs` — contain duration, status, `info()` output, and runtime errors.
- Standalone category: general-purpose — called by other Deluge Functions via `standalone.FunctionName()`, invoked via REST API, or executed manually.
- Schedule category: no input arguments — the Function queries CRM data directly inside the script; no trigger event context is available.

REQUIRED_PARAMETERS:
- Button/Automation/Related List/Signals (Deluge): define argument names in the function signature; map each to a CRM merge variable (e.g. `${Deals.Id}`) at the trigger's association point (Workflow Rule action, Custom Button setup, Blueprint transition, Signals config). Not applicable to Schedule (no arguments), Standalone (arguments from caller), or Validation Rule (uses `crmAPIRequest`).
- REST API/Webhook: read request headers, parameters, and body via `crmAPIRequest`.
- Standalone as REST API: control HTTP status, headers, content type, and body via `crmAPIResponse`.
- Validation Rule: return a Map with pass/fail semantics — `true` allows the save; `false` blocks the save and delivers the error message to the user.
- Related List: return a valid XML string — CRM parses this to render the related list section on the record detail page.

UI_ONLY_ACTIONS:
- `Setup → Developer Hub → Functions` — create, edit, view execution logs, manage schedules, and access all Function management.
  Note: No API equivalent for Function creation or management — UI-only.
- `Setup → Automation → Workflow Rules` / Custom Button setup / Blueprint transition configuration — associate a Function with its trigger.
  Note: No API equivalent for Function–trigger association — UI-only.

CRITICAL_FAILURE_MODES:
- Function not associated with any trigger → never executes — association is a separate step at the Workflow Rule, Button, or Blueprint setup, not in the Function editor.
- Cold start: first execution after inactivity has higher latency — expected runtime warm-up, not a script error.
- Automation/Schedule/Approval/Blueprint return type is void — return values are discarded; side effects must be performed within the execution itself.
- Button return type is String (displayed as modal dialog) — non-string returns are not shown to the user.
- Validation Rule must return a Map with correct pass/fail structure — returning void or a String does not block the record save.
- Related List must return valid XML — malformed XML renders an empty or broken related list section without an explicit error.
- Standalone exposed as REST API without `crmAPIResponse` → HTTP status code and headers are uncontrolled — always use `crmAPIResponse` explicitly for REST API endpoints.
- Manual rerun uses original trigger input — if the CRM record was modified or deleted after the failure, the rerun behavior differs from the original execution.
- Automation category fires asynchronously after the triggering record save — real-time blocking of record save is not achievable via Automation category.
- Signals: if the signal payload has incorrect structure or the notification delivery fails, the failure is silent — verify signal payload format against the Signals API spec.
- `invokeurl` without a `connection:` parameter calls the URL without authentication — Connection must be specified in the call for authenticated external API access.
- Functions is the right tool only when built-in automation (Workflow Rules, Blueprints, Macros) cannot fulfil the requirement — use declarative automation primitives first.

CANONICAL_EXAMPLES:

### Quick Reference — Deluge Function Categories

| Category | Return Type | Namespace prefix | Triggered by | Callable from |
|----------|-------------|-----------------|--------------|---------------|
| Button | `string` | `button.*` | Custom Button click | UI button only |
| Automation | `void` | `automation.*` | Workflow Rule / Blueprint / Approval | Workflow, Blueprint |
| Schedule | `void` | `schedule.*` | Time-based trigger | Scheduled Actions |
| Related List | `string` (XML) | `related_list.*` | Related List display | UI Related List |
| Standalone | `string` | `standalone.*` | API call / Button / inter-function | Any authorized caller |
| Sales Signals | `void` | `salessignals.*` | Signal event | Signal automation |
| Validation Rule | `map` | `validation_rule.*` | Record create/update | Validation Rule trigger |

**Brace format**: Opening `{` must be on the same line as the signature — Allman style is rejected with "Improper code format".

---

#### Button
```deluge
string button.{FunctionName}(){
    return "";
}
// With mapped argument:
string button.{FunctionName}(String argName){
    return "";
}
```
Arg mapping: each declared arg must be mapped to a CRM merge variable at `Setup → Modules → {Module} → Links and Buttons → {button} → Arguments`. Unmapped args resolve to null at runtime, no error.
Setup: `Setup → Developer Hub → Links & Buttons → Create Button → Action: Call a Function`

---

#### Automation
```deluge
void automation.{FunctionName}(){
    // side-effects only
}
```
Setup: `Setup → Automation → Workflow Rules` or Blueprint Transitions → Function action.

---

#### Schedule
```deluge
void schedule.{FunctionName}(){
    // no input args; query CRM data directly inside the script
}
```
Setup: `Setup → Scheduled Actions → Create`.

---

#### Related List
```deluge
string related_list.{FunctionName}(){
    return "<record><row no=\"0\"><FL val=\"Name\">John</FL></row></record>";
}
```
XML format: `<record>` → `<row no="{index}">` → `<FL val="{col}">{value}</FL>`.
Setup: Custom Related List via `Setup → Developer Hub → Functions`.

---

#### Standalone
```deluge
string standalone.{FunctionName}(){
    return "";
}
// Return structured data — serialize to string; callers parse on their end:
string standalone.{FunctionName}(){
    result = Map();
    result.put("status", "success");
    return result.toString();
}
```
CRM editor enforces `string` as the only valid declared return type for `standalone.*` — map/list/int declarations are rejected with "Invalid return Type".
Invokers: REST API, Custom Button, Workflow, `zoho.crm.invokeFunction()`, ClientScript `ZDK.Apps.CRM.Functions.execute()`, Widget `ZOHO.CRM.FUNCTIONS.execute()`.
Setup: `Setup → Developer Hub → Functions → Get API key` for REST exposure.

---

#### Sales Signals
```deluge
void salessignals.{FunctionName}(){
    // react to signal events
}
```
Setup: Signal automation rules.

---

#### Validation Rule
```deluge
map validation_rule.{FunctionName}(string crmAPIRequest){
    entityMap = crmAPIRequest.toMap().get("record");
    response = Map();
    if (/* validation fails */)
    {
        response.put("status", "error");
        response.put("message", "Error message (max 100 chars)");
        return response;
    }
    response.put("status", "success");
    return response;
}
```
`crmAPIRequest` — STRING containing record field values as JSON; use `.toMap()` to parse.
Return: `status` = `"success"` or `"error"`; `message` required when `"error"` (max 100 chars).
Setup: `Setup → Automation → Validation Rules → Create Validation Rule → Function`.
