FILE_PURPOSE: Deluge invokeapi task — CRM-aware REST client with automatic data-center URL routing
MENTAL_MODEL: invokeapi = invokeUrl variant that auto-prepends Zoho CRM base domain; specify path only, not full URL

WHEN_TO_USE:
- Call Zoho CRM REST APIs from within a Zoho CRM Deluge Function.
- Avoid hardcoding data-center base URLs (let `service: zohocrm` resolve them).

WHEN_NOT_TO_USE:
- Default code generation — always generate `invokeurl` for HTTP calls; use `invokeapi` only when the user explicitly requests it.
- Calling non-Zoho or third-party APIs — use `invokeUrl` instead.
- Local or on-premise Zoho deployments with non-standard base domains — use `invokeurl` with the explicit host URL and a named connection instead.
- Responses requiring streaming — 40 s socket / 10 s connection timeouts apply.

TRIGGER_KEYWORDS:
invokeapi, service:zohocrm, data-center routing, invokeapi.status, invokeapi.headers, JSON-toString body, invokeapi path-only, zohocrm connection

RULES:
- `service: zohocrm` resolves the Zoho CRM base domain automatically per data center.
- Specify URL path only (e.g. `/crm/v7/Leads`); never include the base domain in `path`.
- Socket timeout: 40 s; connection timeout: 10 s; connection request timeout: 5 s.
- File download size: up to 15 MB for Zoho CRM.
- Default HTTP method: GET.
- `response-format: NONE` discards the entire response; no status code or body accessible.
- `<response>.status` → HTTP response code; `<response>.headers` → KEY-VALUE of response headers.
- JSON body: call `.toString()` on map/list and set `content-type: application/json` in headers.
- `connection` optional when called from within Zoho CRM (same service); required from other services.

CANONICAL_EXAMPLES:
```deluge
// GET CRM records
response = invokeapi[service:zohocrm path:"/crm/v7/Leads" type:GET connection:"zohocrm_conn"];

// POST with JSON body
data = Map();
data.put("Last_Name","Doe");
data.put("Company","Zylker");
response = invokeapi[
  service:zohocrm path:"/crm/v7/Leads" type:POST
  body:data.toString() headers:{"content-type":"application/json"}
  connection:"zohocrm_conn"
];
status = response.status;

// POST file attachment
attachment = invokeUrl[url:"https://example.com/file.xls" type:GET];
response = invokeapi[
  service:zohocrm path:"/crm/v7/Leads/"+recordId+"/Attachments" type:POST
  body:{{"param-name":"file","param-value":attachment}}
  connection:"zohocrm_conn"
];
```

FAILURE_MODES:
- Full URL (including domain) in `path` → data-center routing error; use path only starting with `/`.
- JSON body map without `.toString()` + `content-type: application/json` → body format mismatch.
- `response-format: NONE` silently discards response; remove when debugging.
- Field keys in body using display labels (e.g. `"Last Name"`) → silently ignored or request fails; use API names (`Last_Name`).
- Non-FILE body for file uploads → body format error.

RELATED_DOCS:
- invokeapi full reference — https://www.zoho.com/deluge/help/webhook/invokeapitask.html

SOURCE:
https://www.zoho.com/deluge/help/webhook/invokeapitask.html
