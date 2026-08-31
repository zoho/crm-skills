FILE_PURPOSE: Read when scaffolding, developing, testing, or packaging a Zoho CRM Widget using the ZET CLI.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/widgets/create-widget.html, https://www.zoho.com/crm/developer/docs/widgets/install-cli.html
TRIGGER_KEYWORDS: widget-development-flow, zet-init, zet-run, zet-validate, zet-pack, external-api-gate, widget-scaffold, zrc-first, createInstance, pageload-fallback, chrome-cert-trust

TECHNICAL_CONSTRAINTS:

### Step 1: Verify or Install ZET CLI
```bash
zet --version
# If not found:
npm install -g zoho-extension-toolkit
zet --version   # confirm
```

### Step 2: Initialise the Project
**NEVER manually create widget project files** (`mkdir`, file-creation tools) — manual projects are missing `cert.pem`/`key.pem`, correct `server/index.js`, and `package-lock.json` that `zet run` and `zet pack` require.

Run from the workspace root:
```bash
cd <project-root>
zet init
# → Select "Zoho CRM"
# → Enter widget project name when prompted
cd <ProjectName>
```

Project structure created by `zet init`:
```
<ProjectName>/
├── app/
│   └── widget.html      ← primary entry point
├── plugin-manifest.json
└── dist/                ← produced by zet pack
```

### Step 3: External API Requirements Gate
Before writing any code that touches a non-CRM API, collect ALL of the following from the user:
- Exact endpoint(s) needed
- Required headers (e.g. `orgId`, `X-API-Key`, `Authorization`)
- Authentication type (OAuth via Connection, API key, or none)
- Response shape — top-level key for the records array
- Exact filter/query parameters

Do NOT rely on recalled knowledge for any of the above. If the user cannot supply an answer, direct them to the service's official API reference and pause.

### Step 4: Write Widget Code ZRC-First
Priority 1 — ZRC (`zrc.createInstance`, `zrc.get`, `zrc.post`, etc.) for all CRM reads/writes and external HTTP.
Priority 2 — Legacy `ZOHO.CRM.API.*` only after explicit user approval.

**`createInstance` rule (non-negotiable)**: For any external API, always create a ZRC instance with `baseUrl` and use relative paths — never pass an absolute URL directly to `zrc.get` / `zrc.post`:
```javascript
// CORRECT
var client = zrc.createInstance({ baseUrl: "https://api.example.com" });
var res = await client.get("/endpoint", { params: { key: "value" } });

// WRONG — absolute URL to zrc.get
var res = await zrc.get("https://api.example.com/endpoint", {});
```

### Step 5: Test Locally with zet run
```bash
cd <ProjectName> && zet run
# Server starts at https://127.0.0.1:<port>  (port defined in server/index.js)
# Port conflict: edit server/index.js → change port → rerun
```

In CRM: create widget with **External Hosting** → Base URL: `https://127.0.0.1:<port>/app/widget.html` (include `/app/widget.html` suffix — the server root alone will not load the widget).

**Chrome cert trust**: Visit `https://127.0.0.1:<port>` directly → click **Advanced → Proceed to 127.0.0.1 (unsafe)** before testing in the CRM iframe.

**PageLoad fallback**: If the widget fetches only external data and `PageLoad` may not fire (Dashboard placement or direct browser access), add a `setTimeout` fallback (~1500 ms) after `ZOHO.embeddedApp.init()` with a `fetchCalled` boolean guard to prevent double-invocation.

### Step 6: Validate and Pack
Run only after user confirms the widget is ready:
```bash
zet validate   # fix all reported violations before packing
zet pack       # produces dist/<ProjectName>.zip
```

Switch from External to Internal hosting: `Setup → Developer Hub → Widgets → {widget} → Edit → Hosting → Internal (Zoho) → upload dist/<ProjectName>.zip → Save`

### Step 7: Iterate on User Feedback
Apply requested changes to files under `app/`, re-test with Step 5, then re-run Step 6 only after user confirms satisfaction.

REQUIRED_PARAMETERS:
- Bootstrap contract: register every `ZOHO.embeddedApp.on(...)` listener **before** the single `ZOHO.embeddedApp.init()` call — listeners registered after `init()` never fire.
- All module and field references: use API names — never display labels.

UI_ONLY_ACTIONS:
- Create/edit Widget definition: `Setup → Developer Hub → Widgets → New Widget`. Note: No API to create or edit Widget definitions — UI-only.
- Associate Widget with placement: Dashboard, Custom Button, Related List, Web Tab, Blueprint, Signal, Settings, Wizard — see [widgets-usage.dou.md](./widgets-usage.dou.md) for full association paths. Note: No API for placement association — UI-only.

CRITICAL_FAILURE_MODES:
- Manually created project (via `mkdir` or file-creation tools) — missing TLS certs (`cert.pem`/`key.pem`), correct `server/index.js`, `package-lock.json`; `zet run` and `zet pack` fail silently or with confusing errors.
- Absolute URL passed directly to `zrc.get`/`zrc.post` for external APIs — always use `zrc.createInstance({ baseUrl })` first; absolute URLs bypass the instance configuration.
- Chrome cert trust step skipped — widget iframe shows "didn't send any data" or blank; trust the self-signed cert at `https://127.0.0.1:<port>` directly in the browser before testing in CRM.
- `zet run` / `zet validate` / `zet pack` run from a different terminal window than where `cd <ProjectName>` was run — directory change does not carry over between terminal windows; always chain: `cd <ProjectName> && zet run`.
- `zet pack` run before `zet validate` — pack produces a zip even with violations; always validate first.
- Widget code written before Step 3 completes — missing `orgId` / `X-API-Key` / `Authorization` headers cause silent 400/403 with no obvious error.
