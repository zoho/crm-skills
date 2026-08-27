FILE_PURPOSE: Deluge Connections — authentication configuration for invokeUrl, invokeapi, and integration tasks
MENTAL_MODEL: Connection = named auth credential (OAuth/API key/etc.) passed as link name to integration calls; created via Setup UI only

WHEN_TO_USE:
- Authenticate outbound requests from a Deluge Function to Zoho or third-party services.
- Pass a named connection to `invokeUrl`, `invokeapi`, or CRM integration tasks.
- Use dynamic parameter placeholders `{ParameterKey}` in connection URLs for parameterized auth.

WHEN_NOT_TO_USE:
- Same-service `invokeapi` from within Zoho CRM — connection is optional (auto-resolved internally).
- Direct public endpoints requiring no auth — omit connection parameter.

TRIGGER_KEYWORDS:
connection linkname, OAuth 2 custom service, connection auto-revoke, dynamic parameter, My Connections, Shared Connections, AWS Signature connection

RULES:
- Link name rules: begin with lower-case letter; only lower-case letters, numbers, underscores; max 50 characters; unique.
- Supported auth types: API Key, Basic, OAuth 1, OAuth 2 (Auth code / PKCE / Client credentials), AWS Signature v4.
- AWS Signature: auth details via headers only; no query string or form data support.
- Connections unused 6+ months are automatically revoked.
- Editing or deleting a custom service immediately revokes all connections using it (including other org members' connections).
- Auth type and service link name are non-editable after creation; OAuth 2 scopes cannot be edited or deleted.
- Dynamic parameter placeholders `{ParameterKey}` in URLs are replaced at execution; case-sensitive.
- Connection creation is UI-only: `Setup → Developer Hub → Connections → My Connections → Create Connection`.

CANONICAL_EXAMPLES:
```deluge
response = invokeUrl[
  url: "https://api.service.com/endpoint"
  type: GET
  connection: "my_connection_link_name"
];

// Dynamic parameter in URL
response = invokeUrl[
  url: "https://{domain}.salesforce.com/services/data/v56.0/sobjects/..."
  type: GET
  connection: "salesforce_connection"
];
```

FAILURE_MODES:
- Using connection display name (not link name) in script → connection-not-found error.
- Connection unused 6+ months → auto-revoked; re-authorize before next execution.
- Resetting Zoho account password with "Revoke access" → all connections revoked.
- Shared connection without "Use credentials of login user" enabled → all requests run under owner's credentials.
- `{ParameterKey}` placeholder case-sensitive; must exactly match parameter key in custom service config.
- OAuth 2 scope missing at creation → cannot add/edit later; create a new connection with required scopes.

RELATED_DOCS:
- Connections documentation — https://www.zoho.com/deluge/help/connections.html

SOURCE:
https://www.zoho.com/deluge/help/connections.html
