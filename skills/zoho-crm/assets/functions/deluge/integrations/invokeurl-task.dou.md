## FILE_PURPOSE
Deluge invokeUrl task — outbound HTTP client for REST APIs, file downloads, and web integrations

## MENTAL_MODEL
invokeUrl = synchronous HTTP client with 40 s socket timeout; returns JSON, files, or raw text from any URL

## WHEN_TO_USE
- Call third-party REST APIs from a Deluge Function.
- Download remote files (returns FILE datatype).
- POST JSON, form-data, or multipart file uploads to external endpoints.

## WHEN_NOT_TO_USE
- Calling Zoho CRM's own REST APIs from within Zoho CRM — use `invokeapi` for automatic data-center routing.
- Real-time streaming or long-polling endpoints — 40 s socket timeout terminates the connection.

## TRIGGER_KEYWORDS
invokeUrl, detailed:true, 40s socket timeout, invokeUrl body format, multipart form-data, external call limit, SSL certificate restriction, response-format FILE

## RULES
- Socket timeout: 40 seconds; if exceeded, task terminates with "socket timeout error".
- File download size limits: Zoho domain — up to 15 MB; non-Zoho domain — up to 5 MB.
- URL domains with user-created SSL certificates cannot be invoked.
- Each execution counts as one external API call; a task in a loop of N iterations consumes N calls.
- Default HTTP method: GET.
- `detailed: false` (default) returns response content only; `detailed: true` returns `responseCode`, `responseHeader`, `responseContent` as KEY-VALUE.
- Raw TEXT body content-type defaults to `text/plain`; KEY-VALUE body defaults to `application/x-www-form-urlencoded`; explicit `Content-Type` header overrides.
- For multipart requests, use `body` as KEY-VALUE with `content-type: multipart/form-data`.

## CANONICAL_EXAMPLES
```deluge
// Minimal GET (fetch a file)
response = invokeUrl[url:"http://example.com/file.png" type:GET];

// POST with JSON body
contact_info = Map();
contact_info.put("contact_name","Shawn");
response = invokeUrl[
  url:"https://books.zoho.com/api/v3/contacts?organization_id=53792286"
  type:POST body:contact_info.toString()
  headers:{"content-type":"application/json"}
  connection:"books_connection"
];

// GET with detailed response
response  = invokeUrl[url:"..." type:GET detailed:true];
statusCode = response.get("responseCode");

// DELETE with JSON body
param = {"spamCategory":"whiteListEmail","whiteListEmail":{"email@domain.com"}};
response = invokeUrl[
  url:"https://mail.zoho.com/api/organization/68XXXXX72/antispam/data"
  type:DELETE body:param.toString()
  headers:{"content-type":"application/json"}
  connection:"mail_connection"
];
```

## FAILURE_MODES
- Socket timeout (40 s) → task terminates; build retry logic for time-sensitive endpoints.
- URL with user-created SSL certificate → invocation blocked.
- File exceeding size limit → runtime error.
- Missing `content-type: application/json` header when sending JSON body to a third-party API → body treated as plain text; API rejects or misparses. **Exception**: Any Zoho CRM API endpoint (any `/crm/v8/...` path) called via a named Connection accepts a `body:queryBody.toString()` string without an explicit `content-type` header — the Connection context is sufficient.
- `detailed: false` (default) returns only response body regardless of HTTP status; use `detailed: true` to capture status code and headers when diagnosing failures.
- Map literal `{"key": value}` used directly in `invokeurl parameters` field → Improper Statement Error; build the map as a variable first, then pass it. Note: inline map literals ARE allowed in the `headers` field.
- `connection:` field requires a bare literal link name — not a string variable. Passing a variable raises `"value of 'connections' does not match required data type 'CONNECTION LINKNAME'"`. Correct: `connection: "my_link_name"` not `connection: myVar`.

## RELATED_DOCS
- invokeUrl full reference — https://www.zoho.com/deluge/help/webhook/invokeurl-api-task.html

## SOURCE
https://www.zoho.com/deluge/help/webhook/invokeurl-api-task.html
