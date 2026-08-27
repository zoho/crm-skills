FILE_PURPOSE: Read when invoking a server-side Deluge Function from a Widget via `ZOHO.CRM.FUNCTIONS.execute` and parsing its `details.output` envelope.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_FUNCTIONS
TRIGGER_KEYWORDS: ZOHO.CRM.FUNCTIONS, execute, Deluge function, Widget API type, arguments, details.output, function api name

TECHNICAL_CONSTRAINTS:
- Single method exposed: `ZOHO.CRM.FUNCTIONS.execute(func_name, req_data)` returning a Promise resolved with the Function execution envelope.
- Target Deluge Function must be created at Setup → Developer Space → Functions and its **API type** must be set to `Widget` — Functions with other API types are not callable from this SDK surface.
- Maximum **5 arguments** per call, passed as key-value pairs in `req_data.arguments`.
- Argument values are serialized to strings on the way in — the Deluge Function receives `arg1`-style parameters typed per its declared signature.
- Function output is returned in the `details.output` property of the resolved envelope; values are strings — JSON-returning Functions need a caller-side `JSON.parse(result.details.output)`.
- Executes under the logged-in user's auth context — the Function runs with that user's record-visibility scope unless the Function is declared to run as admin.
- Source does not document a per-call timeout — assume the standard Function-execution credit and timeout caps from the Functions limits page.
- Source does not document automation suppression — Functions invoked here apply the `trigger` map semantics of any internal `zoho.crm.update / create / upsert` call they make (see parent skill Top-5 Gotcha #3).

REQUIRED_PARAMETERS:
- `execute(func_name: string, req_data: { arguments: Record<string, any> })`.
- `func_name` is the Function's **API name**, not its display label.
- `req_data.arguments` keys must match the Function's declared argument names verbatim.

UI_ONLY_ACTIONS:
- Create / edit a Function and set API type to `Widget`: `Setup → Developer Space → Functions → {function} → REST API → API Type`. Note: API type cannot be flipped after Functions referenced from production Widgets are live without breaking the contract — coordinate before changing.

CRITICAL_FAILURE_MODES:
- `func_name` populated with the Function display label instead of API name: returns function-not-found error — `label-vs-api-name`.
- Function created with API type `REST API` / `Standalone` instead of `Widget`: SDK rejects the call — flip API type in Setup before re-invoking.
- `req_data.arguments` populated with > 5 keys: SDK silently drops the overflow keys; downstream Function receives partial input — split into multiple calls or aggregate into a single JSON-string argument.
- Argument key spelling drift (caller `recordId` vs Function arg `record_id`): Function receives `null` for that argument and silently executes against the missing input (`label-vs-api-name` analogue for arguments).
- Caller treats `result.details.output` as already-parsed JSON: silent `[object Object]` / undefined access — always `JSON.parse` when the Function returns JSON.
- Function does a `zoho.crm.update` on the record that triggered the Widget without a loop guard: workflow recursion — see parent-skill Top-5 Gotcha #4 (`Loop_Guard__c` pattern).
- Function returns a string > 2 MB: source caps not stated — large outputs can hit the Function output cap and truncate; page the output via multiple calls.
- Widget invokes `execute` inside a tight loop (per row of a list): hits the Function-execution daily credit — batch into one call that processes the list server-side.
- Error path of `execute(...)` is uncaught: rejected Promise surfaces only as a browser-console unhandled-rejection — always `.catch` / try / await.
- Function references a Connection that the invoking user lacks access to: Function-internal `invokeurl` fails with auth error; surface that branch back to the Widget UI.
- `arguments` key reserved by Deluge runtime (`crmAPIRequest`, etc.) shadowed accidentally: Function receives unexpected payload — avoid runtime-reserved names.
- Same Function called concurrently from two Widget instances on one page: execution credits consumed per call regardless of duplication — debounce / dedupe at the caller.
- Function output containing a `null` `details.output`: source does not specify whether the resolved or rejected branch fires — defensive read both branches.
- Function argument names re-used as Deluge reserved words (`map`, `list`): runtime accepts but downstream `arg.get(...)` fails subtly — prefix or rename.
- Function execute output cached at the Widget while the Function's body changed in Setup: stale logic served — invalidate cache on Widget mount.
- Function returns a Deluge-thrown `info` payload rather than `return`: SDK envelope shape differs — always exit Functions with explicit `return`.
- `execute` invoked from a Widget hosted in a Settings location where no record context exists: Function args expecting `recordId` receive `null` — branch on null inside the Function.
- Function relying on the trigger user's profile permissions while the Widget caller is a low-privilege user: returns empty record visibility — elevate the Function to run as admin if cross-profile visibility is required.
- `execute` called recursively (Function invokes another Function which calls back): rapid credit drain — audit Function call graphs.
- Argument key collisions when same Function called for two records concurrently via `Promise.all`: SDK does not multiplex per-call state — each call is independent but the Function's daily credit is shared.
- Function declared with mandatory args not supplied by caller: returns `MANDATORY_NOT_FOUND` — caller must satisfy every required parameter.
- Function output > documented per-call cap: server truncates without warning — page or stream outputs.
- Function relying on a Connection the caller user lacks: returns auth error inside `details` — inspect `details` even on resolved branch.
- Function timeout (per Function-execution limits) hit mid-execution: SDK rejects with timeout error — split long workloads into Schedule Functions.
- `req_data.arguments` key starting with a digit or hyphen: Deluge parser rejects — keep argument names alphanumeric snake_case.
- Function name renamed in Setup after the Widget shipped: existing `execute(<old_name>, ...)` calls error — coordinate rename with Widget redeploy.
- Function's API type flipped from `Widget` to `REST API` after deployment: all existing Widget callers break — treat API type as a contract.
