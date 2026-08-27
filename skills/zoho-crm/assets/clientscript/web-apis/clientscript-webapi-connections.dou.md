FILE_PURPOSE: Read when egressing to an external HTTP service (or a Zoho CRM REST endpoint) from a ClientScript via a pre-configured named Connection using `ZDK.Apps.CRM.Connections.invoke`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/webapi_v2/Connections
TRIGGER_KEYWORDS: ZDK.Apps.CRM.Connections.invoke, connection_name, param_type, request parameter, request body, GET, POST, DELETE, CRMResponses

TECHNICAL_CONSTRAINTS:
- Surface is `ZDK.Apps.CRM.Connections` — single method `invoke` that routes an HTTP request through a named Connection (auth + endpoint allow-list owned by the Connection).
- The Connection (`connection_name`) must be pre-created under Setup → Developer Hub → Connections and must list the target endpoint's host in its allowed-domains / scope set; ClientScript cannot create Connections.
- `param_type` is numeric: `1` → send `parameters` as URL query parameters; `2` → send `parameters` as request body / payload. The two are mutually exclusive; pass empty `{}` for the unused slot rather than omitting the arg.
- Source samples demonstrate three HTTP methods (`GET`, `POST`, `DELETE`); the `method` arg is a free string forwarded to the underlying HTTP layer.
- Returns `CRMResponses` synchronously — response body shape depends on the upstream endpoint, not the helper.
- Source samples target both Zoho CRM endpoints (`https://www.zohoapis.com/crm/v2/Leads`) and external services (`https://mailchimp.api/sample_api`); choice is encoded in the Connection.
- DC base host varies per data centre (`zohoapis.com` / `.eu` / `.in` / `.com.au` / `.jp` / `.com.cn`) — ensure the `url` host matches the Connection's data-centre binding.
- Source page lists exactly one method on this surface (`invoke`); no helpers for listing Connections or rotating tokens are exposed here.
- Sandbox Connections and production Connections have distinct names — republish per environment, or fetch the active Connection name at runtime.
- The helper does not surface a separate timeout knob — timeout behaviour is inherited from the upstream endpoint and the Connection layer.

REQUIRED_PARAMETERS:
- Source samples (verbatim) live at SOURCE_DOC — three samples cover `GET` with `param_type=1`, `POST` with `param_type=2`, `DELETE` with `param_type=2`.
- `invoke(connection_name: String, url: String, method: String, param_type: number, parameters: object, headers: object)` — six positional args.
- `connection_name` — Connection API name (e.g. `"cscript"`, `"mailchimp4"`); required.
- `url` — full request URL (scheme + host + path).
- `url` host must match a domain authorized by the Connection.
- `method` — HTTP method string (`"GET"`, `"POST"`, `"DELETE"` shown in source; other methods follow the same forwarding contract).
- `param_type` — numeric mode selector.
- `param_type = 1` → `parameters` serialized as URL query parameters.
- `param_type = 2` → `parameters` serialized as request body / payload.
- `parameters` — object; for `GET` sample: `parameters.ids = "347706269003,34770129002"`.
- `parameters` — for `POST` sample: `{ "data": [{ "Last_Name": "CScript", "Company": "DOTSDK" }] }`.
- Pass `parameters` as `{}` when none are needed (source instructs to pass empty json rather than omit).
- `headers` — object of HTTP request headers.
- Pass `headers` as `{}` when none are needed.
- Auth headers are owned by the Connection — do not pass `Authorization` in `headers`.
- Returns `CRMResponses` — inspect `.status` / `.code` / `.message` for failure detection.

UI_ONLY_ACTIONS:
- Setup → Developer Hub → Connections → +Create your First Connection → Pick Service or Custom Service → scopes + Client ID/Secret → Create and Connect → authorize popup → copy Connection Name. Note: Connection Name is the exact string passed as `connection_name` here; there is no API to create Connections.

CRITICAL_FAILURE_MODES:
- `connection_name` mistyped or referring to a Connection scoped to a different sandbox / production environment → invocation fails with connection-not-found.
- Sandbox-vs-production drift is a recurring failure source.
- `param_type=1` against an endpoint that requires a body → endpoint returns 4xx with field-not-found / bad-request; helper does not validate against the endpoint.
- `param_type=2` against an endpoint that requires query params → endpoint returns 4xx with missing-param error.
- `param_type=2` (body) used with `method="GET"` → some upstreams reject GET-with-body silently and return an empty / 200 with no data; treat as protocol error.
- Calling `invoke` against a URL whose host is **not** in the Connection's allowed-domains list → Connection layer rejects the call with permission / scope error before egress; no upstream call is fired.
- Passing `Authorization` (or any auth header) inside `headers` → helper either overrides with the Connection's auth or rejects; redundant and may leak intent. Let the Connection own auth.
- Connection's OAuth scope set narrower than the upstream call needs → upstream returns `OAUTH_SCOPE_MISMATCH`; re-authorize Connection with the broader scope.
- Connection's stored refresh token revoked at the upstream provider → `invoke` returns auth-failed; re-authorize via the Setup UI flow.
- Source does not document a per-call rate limit, payload-size cap, or per-Connection daily quota for the helper.
- Helper limits are inherited from the upstream endpoint and the org's Connection quota.
- Source does not enumerate error codes for the wrapper.
- Surface failures by reading `CRMResponses.status` / `.code` / `.message` and any upstream-specific error body inside the response.
