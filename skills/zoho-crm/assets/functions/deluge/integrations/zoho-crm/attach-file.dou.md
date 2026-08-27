FILE_PURPOSE: zoho.crm.v8.attachFile — attach a file to an existing CRM record from Deluge
MENTAL_MODEL: zoho.crm.v8.attachFile(module, record_id, FILE_object, connection) → attachment metadata; FILE must be fetched first

WHEN_TO_USE:
- Attach a file downloaded via invokeUrl to a specific CRM record.

WHEN_NOT_TO_USE:
- Passing a URL string directly as the file — fetch it first via invokeUrl to get a FILE type object.

TRIGGER_KEYWORDS:
zoho.crm.v8.attachFile, invokeUrl, file_object, INVALID_DATA, attachFile, record_id

RULES:
- Syntax: response = zoho.crm.v8.attachFile(module, record_id, file_object, connection);
- `file_object` must be a Deluge FILE type; obtain via `invokeUrl` task before passing.
- Applicable modules for file attachment are listed in Zoho CRM API documentation.
- Connection mandatory for Zoho Cliq; optional for all other Zoho services.
- Each call attaches a new attachment; it does not replace an existing attachment with the same name.
- Each execution consumes one external API call.
- To LIST attachments on a record via REST: `GET /crm/v{n}/{Module}/{id}/Attachments` — v3+ requires a `fields` query parameter (e.g. `?fields=id,$file_name`); v2 does not require it.
- To DOWNLOAD a specific attachment via REST: `GET /crm/v{n}/{Module}/{id}/Attachments/{attachmentId}` — the attachment `id` must be in the URL path; omitting it returns the attachment list instead of a file.

CANONICAL_EXAMPLES:
```deluge
file_object = invokeUrl[url:"https://assets.example.com/file.jpg" type:GET];
response = zoho.crm.v8.attachFile("Leads", 4770XXXXXXXXXX, file_object);
// Success response: {"code":"SUCCESS","message":"attachment uploaded successfully","status":"success"}
```

FAILURE_MODES:
- `INVALID_DATA`: record_id is invalid or non-existent. Response: `{"code":"INVALID_DATA","message":"the related id given seems to be invalid"}`.
- Passing a TEXT URL string as `file_object` instead of a FILE type → execution failure.
- Failed invokeUrl (unreachable URL, HTTP error) → null file_object → `INVALID_DATA` or runtime error.
- Module display name instead of API name → `INVALID_DATA` or incorrect module resolution.
- Listing attachments on v3+ API without `fields` query param → empty or error response; add `?fields=id,$file_name` to the URL.
- Attempting to download an attachment without the specific `attachmentId` in the URL path → returns the attachment list instead of a file.

RELATED_DOCS:
- Zoho CRM API V8 — Attach File — https://www.zoho.com/deluge/help/crm/attach-file-V8.html
- invokeUrl task — ../invokeurl-task.dou.md

SOURCE:
https://www.zoho.com/deluge/help/crm/attach-file-V8.html
