FILE_PURPOSE: Read when calling a third-party HTTP endpoint from Client Script via `ZDK.HTTP.request` — covers method enum, request shape, response handle, and the per-page request cap.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/HTTP
TRIGGER_KEYWORDS: ZDK.HTTP, request, AJAX, headers, parameters, content, Response, third-party

TECHNICAL_CONSTRAINTS:
- **Per-page request cap**: source explicit — *"Supports a maximum of 15 requests per page."* The cap is per page load, not per script.
- Returns a `Response` object — see [response.dou.md] (separate node, not yet distilled).
- `method` enum: `'POST' | 'GET' | 'PUT' | 'DELETE' | 'PATCH'`. Default `'GET'`.
- `request_object.content` is the request body (raw string). For JSON payloads, set `headers['Content-Type'] = 'application/json'`.
- `request_object.parameters` is the query-string map; merged into the URL.
- `request_object.headers` is a free-form object of request headers.
- `ZDK.HTTP.request` is the only documented method on `ZDK.HTTP` (no `get`, `post`, `put` shortcuts).
- This API targets **external** endpoints. For Zoho CRM record operations, use Web API (`ZDK.Apps.CRM.*`) — those calls do not consume the 15-request cap on this page object.

REQUIRED_PARAMETERS:
- `request(request_object) → Response`
    · `request_object.url` (String, required) — request URL.
    · `request_object.method` (enum, optional, default `'GET'`).
    · `request_object.content` (String, optional) — request body.
    · `request_object.headers` (Object, optional).
    · `request_object.parameters` (Object, optional) — query parameters.

UI_ONLY_ACTIONS:
- *(none in source)* — `ZDK.HTTP.request` does not require any console-side binding; URL allow-listing (if any) is implicit.

CRITICAL_FAILURE_MODES:
- **15-requests-per-page hard cap** — request #16 silently errors (or rejects). Hoist repeated calls into a single batched endpoint, or cache in `getForm().getValues()` / `$Page.navigation_data`. (page-request-cap)
- **`content` is a String, not auto-serialised** — passing a JS object to `content` without `JSON.stringify` sends `[object Object]`. (body-serialisation)
- **`Content-Type` header is not auto-set** — JSON bodies need `headers: { 'Content-Type': 'application/json' }` explicitly.
- **`parameters` keys are URL-encoded once** — pre-encoding values double-encodes.
- **CORS / CSP / domain-allowlist behaviour unspecified in source** — third-party endpoints that block browser-origin calls fail with no documented error code in this page.
- **No documented `timeout` parameter** — long-running requests block per-page request budget and may contend with the 10 s mobile timeout (per `../clientscript-mobile.dou.md`).
- **No documented retry / circuit-breaker** — caller must implement retries manually; counts against the 15-call cap.
- **Synchronous vs async semantics not stated in source** — example does not show `await` / `.then`.
- **No Zoho CRM auth automatically attached** — `ZDK.HTTP.request` is for third-party calls; do not use it to hit `*.zohoapis.com/crm/...` (use Web API instead). (wrong-tool-for-crm)

SUPPORTED_PAGES:
- `request` — no page restriction; available on all page types.
