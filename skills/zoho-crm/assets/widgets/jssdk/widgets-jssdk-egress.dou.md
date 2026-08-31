FILE_PURPOSE: Read when egressing to an external HTTP service from a Widget via `ZOHO.CRM.HTTP.*`, `ZOHO.CRM.CONNECTION.invoke`, or `ZOHO.CRM.CONNECTOR.*`.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_HTTP, https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_CONNECTION, https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_CONNECTOR
TRIGGER_KEYWORDS: ZOHO.CRM.HTTP, ZOHO.CRM.CONNECTION, ZOHO.CRM.CONNECTOR, invoke, invokeAPI, authorize, external API egress, connection link name

TECHNICAL_CONSTRAINTS:
- Three egress mechanisms with distinct auth models — pick by external-service auth requirement.
- `HTTP.{get,post,put,patch,delete}(request)`: direct browser fetch from the widget iframe; no CRM-side auth injected — caller supplies any auth header inline.
- `CONNECTION.invoke(conn_name, req_data)`: routes the call through a pre-configured CRM Connection (Setup → Developer Hub → Connections); CRM injects the connection's stored OAuth / token transparently.
- `CONNECTOR.invokeAPI(nameSpace, data)` + `CONNECTOR.authorize(nameSpace)`: routes through a Marketplace-style Connector identified by namespace; `authorize` initiates the OAuth flow for the connector.
- HTTP `request` object keys: `url` (absolute), `headers`, `params` (query string for `get`), `body` (POST/PUT/PATCH).
- CONNECTION `req_data` keys: `url` (absolute), `method` (GET/POST/PUT/DELETE/...), `param`, `headers`, `body`.
- CONNECTOR `data` keys: `url` (relative to connector base or absolute), `method`, `param`, `headers`, `body`.
- All three return Promises resolved with the external service's response payload; rejection contract not specified in source — wrap each in try / catch.
- Connection link name (`conn_name`) is the admin-defined identifier from Setup — display name of the connection is **not** accepted.
- Connector `nameSpace` is the developer-defined namespace from the connector definition, not the display label.
- See sibling [widgets-zrc-reference.dou.md](../widgets-zrc-reference.dou.md) for a unified browser-side egress path (`zrc.*`) that consolidates these three surfaces and adds file-upload + 100 MB connection response support.

REQUIRED_PARAMETERS:
- `HTTP.get({ url, headers?, params? })`; `HTTP.post|put|patch({ url, headers?, body? })`; `HTTP.delete({ url, headers? })`.
- `CONNECTION.invoke(conn_name: string, { url, method, param?, headers?, body? })`.
- `CONNECTOR.invokeAPI(nameSpace: string, { url, method, param?, headers?, body? })`.
- `CONNECTOR.authorize(nameSpace: string)`.

UI_ONLY_ACTIONS:
- Create / list / edit CRM Connections: `Setup → Developer Hub → Connections`. Note: definitions are admin-only; runtime `invoke` is the only SDK equivalent.
- Manage installed Connectors and their authorization state: `Setup → Marketplace → Installed → Connectors`. Note: authorization can be re-triggered from `CONNECTOR.authorize()` at runtime.

CRITICAL_FAILURE_MODES:
- `HTTP.*` used for an external service that requires auth: token is exposed in the browser iframe and visible in devtools — switch to `CONNECTION.invoke` so the credential stays server-side.
- `CONNECTION.invoke` `conn_name` populated with the Connection's display label instead of the link name: returns connection-not-found error — `label-vs-api-name`.
- `CONNECTION.invoke` `req_data.url` left relative when the connection has no base URL configured: request silently misroutes / 404s — always pass absolute URL.
- `CONNECTOR.invokeAPI` called before `CONNECTOR.authorize` for the current user: returns `AUTHORIZATION_FAILED` — gate `invokeAPI` behind a successful `authorize`.
- `HTTP.*` blocked by the external service's CORS policy: iframe request rejected by the browser — no SDK error, only a browser-console CORS line. Use `CONNECTION.invoke` to route through CRM-server-side egress.
- POST / PUT body passed as a string to `HTTP.*`: SDK does not auto-serialize — set `Content-Type: application/json` and stringify, or use `zrc.*` which auto-serializes (see [widgets-zrc-reference.dou.md](../widgets-zrc-reference.dou.md)).
- `param` (CONNECTION / CONNECTOR) vs `params` (HTTP) key mismatch: query string silently empty — match each method's exact key.
- Connector `nameSpace` typo: SDK error obscure — list installed connectors in Setup → Marketplace before authoring.
- File-upload payloads against `CONNECTION.invoke`: source documents text/JSON bodies only — for file upload through a connection use `zrc.post` with `FormData` (see [widgets-zrc-reference.dou.md](../widgets-zrc-reference.dou.md)).
- `HTTP.*` response size assumed to be small: no documented response cap — large payloads can exceed the iframe memory budget; stream / page where possible.
- `CONNECTION.invoke` against a connection whose stored OAuth refresh-token expired: returns auth error — admin must re-authorize the connection in Setup → Developer Hub → Connections.
- Mixing two egress paths against the same external service across the codebase: token-refresh state diverges (HTTP path holds its own header, CONNECTION path holds the CRM-stored token) — pick one mechanism per service.
- `HTTP.delete` body passed in `request`: source signature lists `headers` only — the body is silently dropped.
- `CONNECTION.invoke` second arg shape differs from `CONNECTOR.invokeAPI`: `param` (singular) on Connection, also `param` on Connector — do not paste from `HTTP.*` which uses `params`.
- `CONNECTOR.authorize` Promise resolution treated as proof that the next `invokeAPI` will succeed: token still requires non-expired status — always wrap `invokeAPI` in try / catch.
- Bearer / API-key header rotated only inside `HTTP.*` callers: scattering the secret — centralize in a Connection definition and migrate.
- Connection that uses OAuth1 (e.g. legacy Twitter): file-upload signing differs — verify file paths work against an OAuth1 connection before relying on it.
- `HTTP.post` body sent as a `URLSearchParams` instance: SDK serialization unspecified — prefer JSON body or switch to `zrc.post` which natively supports `URLSearchParams`.
- Connection-stored token expired silently mid-session: first call after expiry returns auth error — detect and prompt admin to re-authorize.
- `HTTP.*` request stuck on a slow third-party host: no caller timeout knob — wrap in `Promise.race` against a manual timer or migrate to `zrc.*`.
- Connector `nameSpace` differs from its display name in Setup → Marketplace: use the developer-supplied namespace from the connector's `connector.json`, never the Marketplace listing title.
- Connection-based GET with `param` containing a JSON object value: serialization behaviour is unspecified — stringify the value before passing.
