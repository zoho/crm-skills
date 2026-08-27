FILE_PURPOSE: Read when choosing the ZRC browser-side request client (`zrc.*`) — three request modes, method signatures, request-config keys, four error classes, and recurring CRM / Connection / External patterns.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/zrc_overview, .../zrc_methods, .../zrc_request_configuration_and_error_types, .../zrc_limitations_and_considerations, .../zrc_code_samples
TRIGGER_KEYWORDS: ZRC, zrc.get, zrc.post, zrc.request, zrc.createInstance, requestConfig, ZrcError, ZrcValidationError, ApiError, ConnectionError, COQL via zrc, attachment upload, function execute

## TECHNICAL_CONSTRAINTS
- **ZRC-first mandate**: Always use `zrc.*` over the legacy `ZOHO.CRM.API.*` / `ZOHO.CRM.HTTP.*` / `ZOHO.CRM.UI.*` SDK. Legacy surfaces are second priority and require explicit user approval.
- **`createInstance` rule for external APIs (non-negotiable)**: For any non-CRM external API endpoint, always create a new ZRC instance with the base URL and use relative paths on that instance. Never pass an absolute URL directly to `zrc.get` / `zrc.post`:
```javascript
// CORRECT
var client = zrc.createInstance({ baseUrl: "https://api.example.com" });
var res = await client.get("/endpoint", { params: { key: "value" } });
// WRONG
var res = await zrc.get("https://api.example.com/endpoint", {});
```
- Three request modes share one client — **CRM-API** (path starts `/crm/v{n}/...`, auto-auth, DC auto-resolved), **Connection-based** (absolute URL + `connection` link name, CRM-server-proxied), **External** (absolute URL, direct browser fetch, no auth injected).
- CRM API requests execute under the **logged-in user's** authorization — resource visibility follows that user's profile + sharing.
- Connection-based requests use a CRM-stored Connection (Setup → Developer Hub → Connections); pass its **link name** via `connection: '<link_name>'`.
- External requests are documented as syntactic sugar over the browser `fetch` API, but at runtime ALL three modes — CRM-API, Connection-based, and External — route through the CRM parent window via postMessage. ZRC is therefore unavailable when the widget is opened directly in a browser tab (no CRM host present). External mode is NOT a direct browser `fetch` wrapper despite documentation language.
- Connection response payload limit **100 MB**; Connection read timeout **40 s**.
- CRM API daily quota inherited per-org; ZRC enforces no extra cap. Timeouts for CRM-API and External modes follow browser default — no explicit ZRC timeout knob.
- File upload via Connection: pass `FormData` as body of `zrc.post` with a `connection` config — Connection-based file upload is **not** supported by `ZDK.Apps.CRM.Connections.invoke`, only by `zrc`.
- Eight quick-request methods plus `request` and `createInstance` — every method returns a Promise resolved with `{ status, data, headers }`.
- Quick signatures: `get(path, requestConfig?)`, `post(path, body, requestConfig?)`, `put(path, body, requestConfig?)`, `patch(path, body, requestConfig?)`, `delete(path, requestConfig?)`, `head(path, requestConfig?)`, `options(path, requestConfig?)`.
- `request(requestConfig)`: full control; `requestConfig` must include `method` and `path`.
- `createInstance(requestConfig)`: reusable instance pre-bound to `baseUrl`, `connection`, `headers`, `method` defaults; the `body` field is **ignored** in this config.
- `requestConfig` keys: `headers` (all), `connection` (Connection-based), `baseUrl` (Connection + `createInstance`), `params` (all, auto-encoded), `responseType` (`'json' | 'text' | 'blob' | 'arraybuffer'`, default `'json'`), `body` (`request` only), `method` (`request` + `createInstance`, default `'GET'`).
- `post / put / patch / request` natively serialize JSON, `FormData`, `URLSearchParams` — no manual `Content-Type` required.
- Per-request overrides on a `createInstance`'d instance do **not** mutate base config — instance is read-only after creation.
- Four typed error classes on rejection: `ZrcError` (request setup failure), `ZrcValidationError` (caller-arg shape violation), `ApiError` (status ≥ 300 / unreachable — carries `status` + `details`), `ConnectionError` (Connection-specific failure). Error shape: `{ name, message, status?, details? }`.
- **ZRC response envelope (applies to every call)**: All ZRC methods resolve to `{ status, data, headers }`. `data` IS the complete raw API response body — there is no additional wrapper. Every response field is accessed as `result.data.<api_response_key>`. For all CRM v8 module endpoints the API body wraps records under a `data` key, making the path `result.data.data` (array) or `result.data.data[0]` (single record).
- Recurring CRM-API patterns (all v8 except Function execute v7):
    · Current user — `zrc.get('/crm/v8/users?type=CurrentUser')` → `data.users[0]`.
    · Single record — `zrc.get('/crm/v8/{Module}/{id}')` → `data.data[0]`.
    · List records — `zrc.get('/crm/v8/{Module}', { params: { fields: 'A,B,C' } })` → `data.data` (array).
    · Related records — `zrc.get('/crm/v8/{Module}/{id}/{RelatedListAPIName}')` → `data.data` (array).
    · Search — `zrc.get('/crm/v8/{Module}/search', { params: { criteria: '(Email:contains:@x)' } })` → `data.data` (array); total in `data.info.count`.
    · Insert / update / delete — `zrc.post|put('/crm/v8/{Module}', { data: [{...}] })`, `zrc.delete('/crm/v8/{Module}/{id}')`.
    · COQL — `zrc.post('/crm/v8/coql', { select_query: '...' })` → `data.data` (array).
    · Picklist patch — `zrc.patch('/crm/v8/settings/fields/{id}?module={Module}', { fields: [{ pick_list_values: [...] }] })`.
    · Attachment upload — `zrc.post('/crm/v8/{Module}/{id}/Attachments', formData)`.
    · Attachment download — `zrc.get('/crm/v8/{Module}/{id}/Attachments/{aid}', { responseType: 'blob' })`.
    · Function execute — `zrc.post('/crm/v7/functions/{name}/actions/execute?auth_type=oauth', body)`; output at `response.data.details.output`.
- Connection patterns: second-arg `{ connection: '<link_name>' }`; URL absolute. WorkDrive upload: `FormData` with `parent_id` + `filename` + `content`.

REQUIRED_PARAMETERS:
- `path: string` — relative for CRM-API mode, absolute (or `baseUrl` + relative) otherwise.
- `body: object | FormData | URLSearchParams` — second positional arg for `post / put / patch`; inside `requestConfig` for `request`.
- `connection: string` — Connection link name; mandatory for Connection-based egress.
- `baseUrl: string` — required when `path` is relative and not a CRM-API path.
- `method: string` — required in `requestConfig` for `zrc.request`; default `'GET'` for `createInstance`.
- Insert / update body shape: `{ data: [{ <field_api_name>: <value>, ... }] }` (array even for single record).
- COQL body: `{ select_query: string }`.
- Search params: `criteria` expression with parenthesized atoms; `email` / `phone` / `word` alternatives also accepted.

UI_ONLY_ACTIONS:
- Create a Connection ZRC can reference by link name: `Setup → Developer Hub → Connections → New Connection`. Note: link name (not display label) is the runtime identifier.
- Enable OAuth2 on a Function so the `auth_type=oauth` execute path works: `Setup → Developer Space → Functions → {function} → REST API → OAuth2 → Enable`. Note: REST-execute without this toggle returns 401.

CRITICAL_FAILURE_MODES:
- `await` omitted on a quick-request call: caller works against a Promise — always `await` or chain `.then`.
- Insert / update body authored as a bare object instead of `{ data: [{...}] }`: CRM v8 rejects with `INVALID_DATA`.
- Field keys / module names in body use display labels (`"Last Name"`, `"Deal"`): silently dropped or `INVALID_DATA` — `label-vs-api-name`.
- COQL SELECT list addressed by display label rather than API name: `INVALID_QUERY`.
- Connection link name typo / display label used in `connection` config: rejects with `ConnectionError` — pass exact link name from Setup.
- CRM API path hardcoded with a DC domain (`https://www.zohoapis.com/crm/v8/...`): bypasses DC auto-resolution and breaks for non-US data centres — pass relative `/crm/v8/...` only.
- Connection-based `path` is relative with `baseUrl` missing: throws `ZrcValidationError`.
- External call to a host that disallows browser-side CORS for the CRM origin: switch to Connection so CRM-server egress is used.
- File upload attempted via `ZDK.Apps.CRM.Connections.invoke`: not supported — use `zrc.post(<url>, FormData, { connection })`.
- Connection response > 100 MB: truncated / rejected — stream / page from target service.
- Connection target service exceeds 40 s read timeout: ZRC throws `ApiError` — restructure as async webhook + poll.
- `requestConfig.body` set on a quick `post / put / patch`: ignored — second positional arg wins.
- `body` field passed inside `createInstance` config: ignored per source.
- Caller branches on `error.message` instead of `error.name`: brittle — branch on `error.name === 'ApiError' | 'ConnectionError' | 'ZrcValidationError' | 'ZrcError'`.
- 4xx / 5xx diagnostics need `error.details`, not `error.message`.
- `responseType: 'blob'` consumer parses `data` as JSON: silent type mismatch.
- Attachment download missing `responseType: 'blob'`: binary content corrupted by JSON / text decode.
- `FormData` body composed without `file.name` (third `append` arg): receiving service rejects 400.
- `URLSearchParams` body with caller-set `Content-Type: application/json`: serialization mismatch — drop the manual header.
- `head` / `options` `.data` empty per HTTP spec — read from `headers`.
- `request` with `method: 'GET'` plus a body: body dropped silently across proxies.
- Per-call `Authorization` header on a CRM-API request: bypasses ZRC auto-auth, fails 401.
- Function execute output read as `response.data.output` instead of `response.data.details.output`: `undefined`.
- Function execute missing `?auth_type=oauth` query param: returns 401.
- Search `criteria` with unescaped parens / colons inside literal values: parser fails silently with empty result.
- COQL response row cap exceeded by broad SELECT: silently truncated — paginate with `LIMIT` + `OFFSET`.
- WorkDrive upload `FormData` missing `parent_id`: file uploads to root folder silently.
- Picklist patch with `display_value` already present: `DUPLICATE_DATA` — dedupe before append.
- `params.fields` projection without `id`: id absent from v8 response — request explicitly when needed.
- Reusable instance shared across two Connections: baked-in `connection` dominates — one instance per Connection.
- Per-request override on an instance assumed to mutate instance defaults: instance config immutable.
- CRM-API `createInstance` with `baseUrl: 'https://www.zohoapis.com'`: defeats DC auto-resolution — do not set `baseUrl` for CRM-API instances.
- Per-org CRM API daily quota exhausted by a polling loop: ZRC returns 429 — back off + cache.
- `URLSearchParams` mutated after passing to `zrc.post`: serialization race — build then send.
- Mixing CRM-API and External modes inside one promise chain without per-call try / catch: a single rejected mode collapses the chain — catch per call.
- ZRC called outside CRM iframe context (direct browser tab, no CRM parent window): all three modes throw `Error: "Parentwindow reference not found"` — use native `fetch` as a dev-preview fallback gated on `err.message.includes("Parentwindow reference not found")`.
- External API call made via `zrc.get('https://example.com/path', ...)` with absolute URL instead of `zrc.createInstance({ baseUrl: 'https://example.com' })` + `instance.get('/path', ...)`: always bind `baseUrl` in `createInstance` for any external service and call relative paths on the instance — never pass an absolute URL directly to a ZRC quick-request method.
- `zrc` referenced before confirming the widget is inside CRM: `zrc` is a live production API documented on `zohocrm.dev` (Zoho CRM’s Developer Space portal, which is itself in Early Access — the "Early Access" label refers to the portal, not the features). `zrc` is absent only when the widget runs outside the CRM iframe (direct browser tab, no CRM parent window). Always wrap `zrc.createInstance` in `try/catch` to guard against the no-CRM-parent-window scenario.
