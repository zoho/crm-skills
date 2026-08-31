FILE_PURPOSE: Read when scoping a ClientScript build — confirming edition / profile prerequisites, supported pages, event-vs-command triggers, 10 s timeout, and ZDK / ZRC surface area before authoring.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/overview.html
TRIGGER_KEYWORDS: ZDK.Client.showAlert, ZDK, ZRC, Developer Permissions, $Crm.user, onLoad, onChange, onSave

TECHNICAL_CONSTRAINTS:
- Execution context — JavaScript runs on the user's web browser instead of the server.
- Edition gating — Client Script feature is available in Enterprise, Ultimate and Professional editions of Zoho CRM.
- Browser gating — only the CRM-supported browser versions render Client Script (per the linked browser-versions page).
- Profile gating — Developer Permissions must be enabled on the caller's profile before they can access the Client Script feature.
- Execution timeout — every Client Script execution is bounded to 10 seconds.
- Supported pages: Create page, Edit page, Clone page, List Page (Standard), Detail Page (Standard), Detail Page (Canvas), Create Page (Wizard), Edit Page (Wizard).
- Per-layout binding — author one Client Script per layout of a module; one definition does not span layouts.
- Custom Button binding — a Client Script for a custom button can be created only from the Buttons page (edit / update later from the Client Script setup page).
- Portal scope — Client Scripts automatically run inside Zoho CRM Portals; scope to portal-wide, specific user types, or individual users; newly created user types have Client Script enabled by default.
- ZDK Web (CRM) API calls invoke Zoho CRM APIs internally and consume an API credit per call; ZDK Client API calls do not.
- ZRC (Zoho Request Client) is a built-in SDK with one consistent syntax for CRM APIs, Connection requests, and public APIs; **org-level feature enablement required when used from ClientScript; available by default in Widgets without any org enablement**.

REQUIRED_PARAMETERS:
- Trigger category — choose Module (for event-based) or Commands (for command palette / keyboard shortcut) when creating a script (see [clientscript-creation.dou.md](./clientscript-creation.dou.md)).
- Event family per supported page (page-event vs field-event vs subform-event vs button-event vs blueprint-event vs tag-event vs mandatory-form-event vs canvas-button/icon/text vs notes-related-list) — full event list in [clientscript-events.dou.md](./clientscript-events.dou.md).
- ZDK Client API surface (in-page UI + record field manipulation) — entry points include `ZDK.Page.getField`, `ZDK.Client.showAlert`; full surface in the Client APIs nodes.
- ZDK Web API surface (CRM data reads / writes via the SDK) — entry point `ZDK.Apps.CRM.*` family; full surface in the Web APIs nodes.
- Portal user context — read user-specific details from `$Crm.user` when running inside a Portal.
- ZRC invocation pattern — covered in the ZRC nodes.

UI_ONLY_ACTIONS:
- Enable per-profile Client Script access: `Setup → Users and Control → Security Control → {Profile} → enable Developer Permissions → Save`. Note: No API equivalent — UI-only.
- Confirm tenant edition: `Setup → General → Company Details`. Note: No API equivalent — UI-only.
- Create a Client Script for a Custom Button: open the Buttons setup page for the target module and configure the Client Script from there (the standalone Client Script setup page cannot create button-bound scripts). Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- Edition below Professional / Enterprise / Ultimate: Client Script node hidden in Setup; no API workaround. (edition-gating)
- Caller's profile missing Developer Permissions: Client Script setup is inaccessible for that profile; admin sees it work, end-users get silent no-fire. (profile-binding)
- Layout-binding mismatch — script attached to one layout will not fire on records using a different layout of the same module; no error, no log. (layout-binding)
- Browser off the supported-versions list: Client Script does not run on that browser; verify browser before triage.
- Execution exceeds 10 s: the script is halted; long-running ZDK Web API or third-party calls require a loader pattern (see [clientscript-best-practices.dou.md](./clientscript-best-practices.dou.md)).
- ZDK Web (CRM) API calls account for an API credit per invocation — high-fan-out scripts drain the daily credit pool.
- ZRC org feature not enabled: `zrc` is unavailable in the ClientScript runtime — fails silently or throws on first call; confirm org enablement before using ZRC from ClientScript. In Widgets, ZRC is available by default.
- ZRC errors not caught in `try/catch`: silently absorbed by the ClientScript environment — no console error, no log (see [clientscript-zrc.dou.md](./zrc/clientscript-zrc.dou.md)).
- Custom Button Client Script attempted from the standalone Client Script page instead of the Buttons page: creation rejected; use the Buttons page.
- Portal Client Script auto-enables for newly created user types — assume opt-in unless explicitly disabled per user type.
