FILE_PURPOSE: Read when calling Zoho CRM REST APIs, Zoho Connections, or external HTTP services from a ClientScript via the built-in `zrc` HTTP client.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/zrc/overview, https://www.zohocrm.dev/explore/client-script/zrc/zrc_methods, https://www.zohocrm.dev/explore/client-script/zrc/request_configuration_and_error_types, https://www.zohocrm.dev/explore/client-script/zrc/limitations_and_considerations, https://www.zohocrm.dev/explore/client-script/zrc/code_samples
TRIGGER_KEYWORDS: zrc.get, zrc.post, zrc.request, zrc.createInstance, connection, baseUrl, responseType, ApiError, ConnectionError, ZrcValidationError

TECHNICAL_CONSTRAINTS:
- Surface is `zrc` — a built-in REST client exposed in the ClientScript runtime. The source documentation is hosted on `zohocrm.dev`, which carries an Early Access banner for the developer portal itself — this does NOT indicate that `zrc` as a feature is in Early Access.
- Three request modes documented: (1) CRM API (relative path `/crm/v8/...`), (2) Connection-based (absolute URL + `connection` link name in `requestConfig`), (3) External API (absolute URL, no auth, "syntactic sugar over the standard fetch API").
- All three modes share identical request-config semantics — source asserts: "All other request configuration like request body, params, headers behave the same way for both Zoho CRM APIs and Connection-based requests" and "Consistent syntax for making API calls — Whether it's CRM, Connection, or External API calls, ZRC uses the same syntax."
- CRM-mode: API domain is auto-resolved from the logged-in user's data centre; calls to the same-org CRM are auto-authenticated (no token / credential handling required by the script).
- CRM-mode: can target any publicly available CRM API version (`/crm/v7/...`, `/crm/v8/...`, etc.); unlike the `clientscript-webapi-*` helpers which wrap v2 endpoints only.
- Connection-mode: the Connection (`connection` link name) must be pre-created out-of-band; ZRC does not expose a Connection-creation API (sibling node: [clientscript-webapi-connections.dou.md](../web-apis/clientscript-webapi-connections.dou.md)).
- Connection-mode supports file upload / download via `FormData` payloads and `responseType: 'blob'` (sample-confirmed: WorkDrive upload + Desk download in `code_samples`); CRM-mode also supports file upload via `FormData` (sample-confirmed: `/crm/v8/Leads/.../Attachments`). Source's "Why use ZRC" header reads "File uploads via Connection or External API" but no External-mode upload sample is provided on any of the 5 pages.
- All `zrc.*` methods return `Promise`s; `async`/`await` and `.then(...).catch(...)` are both supported per the Code Samples page.
- Request body is auto-serialized for three payload shapes: JSON, `FormData`, `URLSearchParams`; source instructs callers **not** to set `Content-Type` manually for these three shapes — the wrapper handles it.
- Query parameters supplied via `requestConfig.params` are auto-URL-encoded; JSON / array values are auto-serialized.
- Response is auto-parsed per `requestConfig.responseType` (default `'json'`); when `responseType` is omitted, parsing falls back to the response's `content-type` header.
- Response shape for body-returning methods: `{ status: number, data: any, headers: object }`. `HEAD` and `OPTIONS` responses omit `data` per source samples (`HEAD` → `{ status, headers }`; `OPTIONS` → `{ status, headers }` with `Allow` and `Content-Length` populated).
- External-mode is documented with "no request limits" (browser-direct, fetch-sugar); CRM-mode has "no enforced ZRC-layer limits" and inherits browser timeout; Connection-mode is the only mode with explicit ZRC-enforced caps (see CRITICAL_FAILURE_MODES).
- Source does not enumerate OAuth scope, edition, profile, or rate-limit caps for the `zrc` helper itself — auth derives from the ClientScript-session user (CRM mode) or the named Connection (Connection mode).

REQUIRED_PARAMETERS:
- Source samples (verbatim) live across the five SOURCE_DOC pages — the `code_samples` page covers ~16 end-to-end examples (CRM CRUD, COQL, Function `execute`, attachment upload / download, Desk / WorkDrive Connection, external POST); re-fetch when authoring a non-trivial payload, Connection call, or Function invocation.
- Quick API methods (one method per HTTP verb):
    - `get(path: String, requestConfig?: object) → Promise<Response>`.
    - `delete(path: String, requestConfig?: object) → Promise<Response>`.
    - `head(path: String, requestConfig?: object) → Promise<Response>`.
    - `options(path, requestConfig?: object) → Promise<Response>`.
    - `post(path: String, body: any, requestConfig?: object) → Promise<Response>`.
    - `put(path: String, body: any, requestConfig?: object) → Promise<Response>`.
    - `patch(path: String, body: any, requestConfig?: object) → Promise<Response>`.
- Custom request:
    - `request(requestConfig: object) → Promise<Response>` — `path` is the only required key in `requestConfig`. Source prose declares "Must include method, path, etc." but the property table lists `method` default as `'GET'` and the first `zrc.request` sample on the same page omits `method` and returns `status: 200`; treat `method` as optional (defaults to `'GET'`).
- Reusable instance:
    - `createInstance(requestConfig: object) → ZRC Instance` — returns an object exposing the same Quick / Custom methods seeded with the base config; per-request overrides allowed without affecting the base.
    - `createInstance` ignores `body` in the base config (source Note: "body is not accepted in requestConfig for createInstance and will be ignored if provided").
    - Source-recommended pattern for Connection calls: pair `connection` + `baseUrl` inside `createInstance` to avoid repeating the connection link name and domain on every request (source Note under "Connection-based Requests").
- `requestConfig` properties (verbatim from source's property table):
    - `headers: Object` — applies to all methods; e.g. `{ 'content-type': 'application/json' }`.
    - `connection: String` — Connection link name; applies to Connection-based requests only.
    - `baseUrl: String` — API domain (e.g. `https://api.example.com`); applies to Connection-based requests and `createInstance()`; **mandatory when `path` is a relative URL**.
    - `params: Object` — query parameters as key-value pairs; applies to all methods; auto-encoded; JSON / arrays auto-serialized. Source escape-hatch: "if you need more customization, please add queryparams directly in the path variable, e.g. `/path/to/myservice?name=brad&city=jaipur`".
    - `responseType: 'json' | 'text' | 'blob' | 'stream' | 'arraybuffer'` — default `'json'`; applies to all methods.
    - `body: any` — applies to `zrc.request()` only (the Quick methods take `body` as a positional arg, not via config).
    - `method: String` — default `'GET'`; applies to `zrc.request()` and `createInstance()` only.
    - `path: String` — applies to `zrc.request()` only.
- Response shape (consistent across all methods and modes): `{ status, data, headers }` — `data` is the parsed body, `headers` is the response-headers object.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- **ZRC errors not wrapped in `try/catch` are silently absorbed by the ClientScript execution environment — no console error, no visible exception, no log entry.** This is intentional ClientScript behavior: unhandled Promise rejections from `zrc` do not propagate as visible runtime errors. Always wrap every `zrc` call in `try { ... } catch (error) { ... }` and branch on `error.name` to surface failures.
- Error type catalogue (source-stated, verbatim from the Error Types table):
    - `ZrcError` — error occurred while setting up the request (pre-flight); inspect `error.message`.
    - `ZrcValidationError` — validation error due to incorrect arguments passed to ZRC methods; inspect `error.message`.
    - `ApiError` — server-side issue (`status >= 300`, server unreachable, or no response received); carries `error.status` and `error.details` (sample shows `{ "name": "ApiError", "message": "Request failed with status code 404", "status": 404, "details": { "error": "User not found" } }`).
    - `ConnectionError` — issues specific to connection-based API calls.
- Connection-mode hard caps (source-stated, Limitations & Considerations page):
    - Response payload cap **100 MB** (source: "Accepts responses up to 100 MB").
    - Read timeout fixed at **40 seconds** against the upstream Connection target (source: "Uses a 40-second read timeout from the target service").
- CRM-mode caps (source-stated, Limitations & Considerations page):
    - No enforced ZRC-layer request / response limits (sent directly from the browser).
    - Request timeout follows the browser's default timeout behaviour — not pinned by ZRC.
    - All CRM-mode calls execute under the logged-in user's authorization (source: "All Zoho CRM APIs are executed under the logged-in user's authorization").
    - Subject to the standard Zoho CRM API limits (`zoho.com/crm/developer/docs/api/v8/api-limits.html`).
- `zrc.request(...)` config missing `path` → `ZrcValidationError`; `method` is optional and defaults to `'GET'` per the property table (see REQUIRED_PARAMETERS note on the source prose / property-table conflict).
- `createInstance({..., body: ...})` → `body` is silently dropped at instance construction (source-stated Note); pass `body` per-call on the returned instance instead.
- Connection-mode call without `connection` in the config (or with a mistyped / unconfigured link name) → `ConnectionError`; the Connection must be pre-created out-of-band before any `zrc` call against it succeeds.
- Connection-mode or `createInstance` with a relative `path` and no `baseUrl` → request setup fails; source states `baseUrl` is **mandatory if `path` is relative**.
- Function execution via `/crm/v7/functions/<api_name>/actions/execute?auth_type=oauth` requires the target Function to have its OAuth2 toggle enabled in the CRM Functions setup page (source-stated in the sample comment: "oauth2 should be enabled for 'my_function' in Zoho CRM functions setup page"); without it the call fails server-side.
- Function execution return value: source-stated in the sample comment — "Function output will be in `details.output` key" (read via `response.data.details.output`).
- Function execution `function_name` passed as display label instead of the Function's API name → server returns function-not-found — same class as [clientscript-webapi-functions.dou.md](../web-apis/clientscript-webapi-functions.dou.md).
- Body auto-serialization vs explicit `Content-Type` collision — if the caller sets `headers['content-type']` manually for a JSON / `FormData` / `URLSearchParams` body, the auto-serializer's content-type and the manual header may conflict.
- `responseType: 'json'` against an upstream that returns a non-JSON body → parsing fails.
- The `zohocrm.dev` documentation portal carries an Early Access banner — this refers to the portal itself, not to `zrc` as a feature. Do not surface Early Access caveats about `zrc` to users based on this banner.
- Source does not enumerate per-call error codes for the `ApiError` / `ConnectionError` cases beyond the catalogue above; surface failures by reading `error.name`, `error.status`, `error.message`, and `error.details` and the upstream endpoint's documented error catalogue.
