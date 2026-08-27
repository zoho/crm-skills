FILE_PURPOSE: Read when inspecting the return value of `ZDK.HTTP.request(...)` — extract the response body via `getResponse()`, headers via `getHeaders()`, or HTTP status code via `getStatusCode()`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Response
TRIGGER_KEYWORDS: ZDK.HTTP.request, Response.getResponse, Response.getHeaders, Response.getStatusCode, http response, status code

TECHNICAL_CONSTRAINTS:
- Response instances are returned synchronously by `ZDK.HTTP.request(config)` (see [http.dou.md](./http.dou.md)). Response is not directly constructible.
- `getResponse() {Object}` — returns the parsed response body as an Object. Source does not document raw-string vs auto-parsed-JSON semantics.
- `getHeaders() {Object}` — returns the response headers as an Object (header-name keyed). Source does not document case-sensitivity or multi-value-header handling.
- `getStatusCode() {Number}` — returns the HTTP status code as a Number. Source example output: `201`.
- Source does not enumerate any error / failure shape. For 4xx / 5xx responses, the assumption is that `getStatusCode()` returns the non-2xx code and `getResponse()` / `getHeaders()` still resolve, but source is silent.

REQUIRED_PARAMETERS:
- `getResponse() {Object}` — no params.
- `getHeaders() {Object}` — no params.
- `getStatusCode() {Number}` — no params.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- **Response is the return of a synchronous `ZDK.HTTP.request` call** — the `request` call counts against the documented per-page cap (15 — see [http.dou.md](./http.dou.md)). Holding a Response and re-issuing the request does not bypass the cap.
- **`getResponse()` shape is not contractually documented** — code that assumes `JSON.parse`-style Object access will throw on a non-JSON response if the call returns String. Type-guard before property access.
- **`getHeaders()` key case is not documented** — `headers['Content-Type']` vs `headers['content-type']` may not be interchangeable.
- **No error-shape documented** — non-2xx responses, network failures, and timeouts are not described. A caller that branches only on `getStatusCode() >= 400` may miss network errors that throw before Response is constructed.
- **Holding a Response across an `await` / `Page` transition** — source does not document Response lifetime; treat as ephemeral and re-fetch rather than caching across page navigation.

SUPPORTED_PAGES:
- `getResponse` — no page restriction; available on all page types.
- `getHeaders` — no page restriction; available on all page types.
- `getStatusCode` — no page restriction; available on all page types.
