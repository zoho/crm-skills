FILE_PURPOSE: Read when invoking a server-side Deluge Custom Function by name from a ClientScript via `ZDK.Apps.CRM.Functions.execute` with optional URL parameters and optional body map.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/webapi_v2/Functions
TRIGGER_KEYWORDS: ZDK.Apps.CRM.Functions.execute, function_name, parameters, functions_body, Custom Functions, CRMResponses

TECHNICAL_CONSTRAINTS:
- Surface is `ZDK.Apps.CRM.Functions` — single method `execute` for invoking a saved Custom Function by name.
- Returns `CRMResponses` synchronously from the script's perspective.
- Source signature does not wrap the return in a Promise.
- The target Function must exist server-side under `Setup → Developer Hub → Functions`.
- `function_name` is the Function's API name (e.g. `"dealtoquote2"`), not its display label.
- Source does not state whether the target Function requires its REST API toggle to be on for ZDK invocation.
- Source does not enumerate OAuth scope, edition gating, or rate-limit caps for this helper.
- Source does not state execution-timeout for the helper; bound to the underlying Function's own runtime limits.
- Both `parameters` and `functions_body` are JSON objects, both optional.
- Sample 1 omits both optional args; Sample 2 supplies only `parameters`; Sample 3 supplies both.
- The two optional args are positional — to pass only `functions_body`, pass an explicit `{}` in the `parameters` slot.
- Source page lists exactly one method on this surface (`execute`); no helpers for listing Functions or fetching Function metadata are exposed here.
- Companion ZRC `ZDK.Client.invoke` / `zoho.crm.invokeConnector` / `ZOHO.CRM.FUNCTIONS.execute` (Widget) cover the same primitive on other surfaces — do not mix surfaces in one DOU.
- The Function runs as the user under whose ClientScript session this `execute` call originated — record visibility, territory filtering, and HIPAA redaction follow that user's profile.
- The helper does not surface a separate timeout knob; the script-side call blocks until the underlying Function returns or times out server-side.
- The helper does not surface a `trigger` map — any write performed inside the Function fires the full automation stack unless the Deluge body suppresses it via `optionalMap.trigger` on its own writes.

REQUIRED_PARAMETERS:
- Source samples (verbatim) live at SOURCE_DOC — three samples cover (1) no-arg, (2) `parameters` only, (3) `parameters` + `functions_body`.
- `execute(function_name: String, parameters?: object, functions_body?: object)` — three-arg signature.
- `function_name` — required; API name of the target Custom Function (e.g. `"dealtoquote2"`).
- `parameters` — optional; JSON map of URL / query parameters surfaced to the Function as named args.
- `parameters` sample shape: `{ "page": 1, "per_page": 10 }`.
- `functions_body` — optional; JSON map sent as the request body.
- `functions_body` sample shape: `{ "amount": 100, "name": "test" }`.
- Returns `CRMResponses`.
- Source does not document the `CRMResponses` schema for this method in detail; inspect `.status` / `.code` / `.message`.

UI_ONLY_ACTIONS:
- Setup → Developer Hub → Functions → New Function → author Deluge → assign API name (the `function_name` token passed here) → Save → Active. Note: the Function authoring lifecycle itself is UI-only and out of scope of this page; this DOU only covers the ClientScript-side invocation contract.

CRITICAL_FAILURE_MODES:
- `function_name` passed as the display label (`"Deal To Quote"`) instead of the API name (`"dealtoquote2"`) → server returns function-not-found — `label-vs-api-name`.
- Target Function does not exist (mistyped name) → invocation fails server-side; surfaced in `CRMResponses`.
- Target Function not yet activated → invocation fails server-side.
- Target Function scoped to a different sandbox / production environment → invocation fails; sandbox-vs-production naming drift is a recurrent failure source.
- `parameters` keys not matching the target Function's declared argument names → Function receives those parameters as null / undefined.
- `parameters` key mismatch → silent over-broad behaviour rather than hard error, mirroring the Native Query `:placeholder` mismatch class.
- Function recursion: a Function invoked here that updates the record currently displayed in the ClientScript host page can re-trigger workflows that loop until the daily-credit cap — `automation-interaction`.
- Function exceeds its server-side execution timeout → returns `EXECUTION_TIMEOUT` from the underlying runtime, surfaced into `CRMResponses`.
- Source does not state execution-timeout on this page — consult the Functions runtime doc for the per-edition limit.
- Daily Function-credit exhaustion → 429 returned silently into the ClientScript handler with no UI alert.
- Source does not document error codes for the ZDK wrapper specifically.
- Failures bubble from the underlying Function runtime; treat any non-success `status` in `CRMResponses` as failure and branch on `.code` / `.message`.
- Source page does not document how the wrapper serializes `parameters` when both `parameters` and `functions_body` carry overlapping keys — keep key sets disjoint to avoid ambiguity.
