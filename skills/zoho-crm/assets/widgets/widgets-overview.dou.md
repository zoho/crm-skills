FILE_PURPOSE: Read when scoping a Widget feature — confirming runtime sandbox, edition gating, profile prerequisite, hard cap, and SDK surface before scaffolding.
SOURCE_DOC: widgets/zoho-crm-widgets.md
TRIGGER_KEYWORDS: Developer Permissions, ZRC, ZOHO.embeddedApp, ZOHO.CRM.API, ZOHO.CRM.UI, ZOHO.CRM.CONFIG, plugin-manifest.json, 200 widgets

TECHNICAL_CONSTRAINTS:
- Execution context — Widget runs as a sandboxed iframe inside CRM UI; bootstrap loaded from `app/widget.html`; reloaded on every CRM page navigation.
- SDK surface — `ZOHO.embeddedApp.*` (lifecycle), `ZOHO.CRM.API.*` (data), `ZOHO.CRM.UI.*` (UI), `ZOHO.CRM.CONFIG.*` (current user); ZRC unifies cross-service call syntax inside the same Widget.
- Network egress — JS SDK or ZRC only; direct cross-origin `fetch` and cross-frame DOM access to the host CRM page are sandbox-blocked.
- Edition gating — Widgets feature exposed in Professional, Enterprise, and Ultimate editions only; absent from Free / Standard.
- Profile gating — caller's profile must have Developer Permissions enabled; otherwise the Widgets node is hidden from Setup.
- Hard cap — 200 Widget definitions per CRM org in Enterprise edition; 200 in Ultimate; cap counts definitions, not placements, and is enforced per environment (sandbox vs production audited separately).
- Sandbox-scoped — Widget IDs, Internal-hosting `.zip` references, and External-hosting URLs do not promote automatically; republish per environment.
- Browser support — Widgets render only on the CRM-supported browser versions list.
- JS SDK is delivered from the embedded-app CDN; the SDK version is pinned inside `widget.html` (see [widgets-jssdk-events.dou.md](./jssdk/widgets-jssdk-events.dou.md)).
- Widget definitions are not API-managed — every CRUD action lives in Setup (see [widgets-usage.dou.md](./widgets-usage.dou.md)).
- One Widget definition can be associated with multiple host components (see [widgets-usage.dou.md](./widgets-usage.dou.md) for the eight supported locations).
- Logging surfaces only in the host browser's devtools console; CRM retains no server-side Widget log.
- Each CRM page navigation reloads the Widget iframe and re-runs the bootstrap — there is no persistent in-memory state across navigations.
- Sharing the same `widget.html` between two Widget definitions requires uploading the archive twice (Internal) or duplicating the URL (External) — there is no shared-asset registry.
- A Widget definition is independent of its placements; deleting a placement does not delete the definition, and vice versa.

REQUIRED_PARAMETERS:
- Authoring artefact set — JS SDK-based project (`app/widget.html` entry + `plugin-manifest.json` descriptor); see [widgets-zet-cli.dou.md](./widgets-zet-cli.dou.md) for the CLI lifecycle and [widgets-jssdk-events.dou.md](./jssdk/widgets-jssdk-events.dou.md) for bootstrap.
- Invocation contract — per Widget location (see [widgets-usage.dou.md](./widgets-usage.dou.md)) and per JS SDK call (see [widgets-jssdk-events.dou.md](./jssdk/widgets-jssdk-events.dou.md) + JS SDK reference docs).
- Cross-references:
    · CLI install / serve / validate / pack → [widgets-zet-cli.dou.md](./widgets-zet-cli.dou.md).
    · `PageLoad` listener + `init()` bootstrap + JS SDK call patterns → [widgets-jssdk-events.dou.md](./jssdk/widgets-jssdk-events.dou.md).
    · Hosting, association, deletion, location selection, Index URL → [widgets-usage.dou.md](./widgets-usage.dou.md).
    · Mobile rendering opt-in → [widgets-mobile-compatibility.dou.md](./widgets-mobile-compatibility.dou.md).

UI_ONLY_ACTIONS:
- Enable Developer Permissions per profile: `Setup → Users and Control → Security Control → {Profile} → enable Developer Permissions → Save`. Note: No API equivalent — UI-only.
- Confirm edition: `Setup → General → Company Details`. Note: No API equivalent — UI-only.
- Audit Widget cap usage: `Setup → Developer Hub → Widgets` (count against the 200-per-environment ceiling). Note: No API equivalent — UI-only.
- Cross-environment promotion: `Setup → Data Administration → Sandbox`. Note: No API to bulk-copy Widget definitions — UI-only.

## CRITICAL_FAILURE_MODES
- External API integration written before requirements are confirmed: do not write any Widget code that touches a non-CRM API until the exact endpoint URL, required headers (e.g. `orgId`, `X-API-Key`, `Authorization`), authentication type, and response shape are confirmed by the user. A missing required header causes a silent 400/403 with no obvious error trace.
- Free / Standard edition tenant: Widgets node absent from Setup — no API workaround because no API exists. (edition-gating)
- Profile lacks Developer Permissions: Widgets node hidden; admin sees Widgets working, end-users silently lose access. (profile-binding)
- 200-cap reached: Create pop-up Save rejected silently — delete an unused Widget (see [widgets-usage.dou.md](./widgets-usage.dou.md)) to free a slot; extension Widgets count against the cap but are removable only via Marketplace uninstall.
- Direct `fetch` to `zohoapis.com` or DOM access to the host CRM page from inside the iframe: sandbox blocks the call — route every CRM call through `ZOHO.CRM.API.*` or ZRC.
- JS SDK version pinned in `widget.html` falls behind host CRM: newer event payload fields are absent — re-pin to the supported SDK version.
- Sandbox Widget definition reused in production without republish: Widget renders blank or 401s. (sandbox-binding)
- Outdated browser (off the supported-versions list): iframe content refuses to render — verify browser before triage.
- Widget Type chosen by display label (e.g. picking "Button Widget" instead of `Custom Button`) maps to the wrong creation surface — use the eight documented Widget Type values verbatim. (label-vs-api-name)
- Stale Widget code persisting across CRM page navigations because of browser cache rather than per-page reload: hard-reload the host CRM page to bypass cache.
- Cross-frame communication between Widget iframe and host CRM page attempted via `postMessage`: not part of the documented contract — rely on `ZOHO.embeddedApp` events instead.
- Multiple Widgets on the same dashboard issuing concurrent `ZOHO.CRM.API.*` calls hitting org-wide rate limits: serialize or batch when the dashboard density grows.
- Widget definition retained in production after the source extension is uninstalled in sandbox only: orgs drift — audit each environment's Widget list independently.
- DC (data-center) host of the embedded-app SDK CDN tracks the CRM tenant's DC; pinning a CDN URL from a different DC blocks SDK load on the iframe.
