# Widgets Subskill

> DOU nodes are authoritative — see [DOU Reference Nodes](#dou-reference-nodes) below.

Zoho CRM Widgets are **embedded iFrame-based UI components** built with HTML, CSS, and JavaScript. They run in a sandboxed iFrame inside Zoho CRM pages and communicate with CRM via the **Zoho CRM JS SDK** (v1.5). They support [ZRC](https://www.zohocrm.dev/explore/widgets/v1.5/zrc_overview) for unified API call syntax.

---

## Execution Instructions

1. Check the DOU node for current ZDK/ZRC method signatures — DOU overrides inline examples.
2. For the full development workflow (scaffold, code, test, pack): read [widgets-dev-workflow.dou.md](../assets/widgets/widgets-dev-workflow.dou.md).
3. Output the complete widget HTML/JS. Confirm the `ZOHO.embeddedApp.on` listener is registered **before** `ZOHO.embeddedApp.init()` (Critical Gotcha below).
4. If the Widget will be opened via a Flyout — register it as **Custom Button type** in `Setup → Developer Hub → Widgets`.

**Architecture defaults** (apply unless the user explicitly requests otherwise):
- ZRC (`zrc.*`) is always first priority over legacy `ZOHO.CRM.API.*`.
- External API calls: use ZRC with `createInstance({ baseUrl })` — never pass absolute URL directly to `zrc.get`/`zrc.post`.

## Validation Checklist

Before delivering the code, verify:

- [ ] Project scaffolded via `zet init` (not manually created) — see [widgets-dev-workflow.dou.md#step-2-initialise-the-project](../assets/widgets/widgets-dev-workflow.dou.md#step-2-initialise-the-project)
- [ ] ZDK method signatures match DOU nodes
- [ ] `ZOHO.embeddedApp.on()` listeners registered **before** `init()` (see Critical Gotcha below)
- [ ] All external API calls use ZRC (`zrc.createInstance`) — never direct `fetch`
- [ ] No DOM manipulation outside sandboxed iframe context
- [ ] `zet validate` passes with no violations
- [ ] Widget packaged via `zet pack` → `dist/<project>.zip` ready, or HTTPS URL confirmed
- [ ] If Widget is opened via a Flyout → Widget is registered as **Custom Button type**; stated in deployment steps

## Critical Gotchas

### Widget listener registered AFTER `ZOHO.embeddedApp.init()` never fires

No error, no console warning. `ZOHO.embeddedApp.init()` resolves any already-registered listeners synchronously; listeners registered after it never receive `PageLoad`.

```javascript
// CORRECT — listener first, init second
ZOHO.embeddedApp.on("PageLoad", function(data) {
  // data = { Entity, EntityId, ButtonPosition? }
});
ZOHO.embeddedApp.init();
```

**Rule**: Register every `ZOHO.embeddedApp.on(...)` listener **before** the single `ZOHO.embeddedApp.init()` call. Treat `init()` as the last line of the bootstrap script.

## When to Use Widgets

- Build a fully custom UI panel with complete HTML/CSS/JS control
- Embed third-party services or visualizations (charts, maps, dialers) inside CRM
- Display complex multi-source data in a related list or dashboard tile
- Create multi-step flows embedded in a Wizard or Blueprint transition
- Integrate external web apps as web tabs or popup overlays
- Use as a notification panel via Signals

## Prerequisites

- Available in **Professional, Enterprise, and Ultimate** editions of Zoho CRM
- **Developer Permissions** must be enabled for the profile: `Setup > Users and Control > Security Control > {Profile} > Developer Permissions`
- Node.js and npm (for local development with CLI)

## Limits

| Constraint | Value |
|-----------|-------|
| Max widgets per org (Enterprise) | 200 |
| Max widgets per org (Ultimate) | 200 |
| Max ZIP file size (internal hosting) | 25 MB |

## Types of Widgets (8 Placements)

| Type | Where it appears | Typical use |
|------|-----------------|-------------|
| **Dashboard** | Home page / custom dashboards | KPI panels, charts, external data tiles |
| **Web Tab** | Tab in the top navigation | Full-page embedded apps |
| **Custom Button** | Button on record / list view | Popups for actions, forms, external lookups |
| **Custom Related List** | Related list tab on a record | Show 3rd-party data related to the record |
| **Wizard** | Step in a Wizard form | Custom data entry steps inside Wizards |
| **Signal** | Signal notification detail view | Enrich notification context with external data |
| **Settings** | CRM Settings screen | Admin-facing configuration panels |
| **Blueprint** | Blueprint transition screen | Assist users during a transition step |

## Hosting Options

| Type | How | Notes |
|------|-----|-------|
| **Internal (Zoho)** | Run `zet pack` from project root → upload `dist/<project>.zip` via Setup → Developer Hub → Widgets | Max 25 MB; Zoho-hosted |
| **External** | Enter a public HTTPS URL | App hosted on your own server; use for active development |

## DOU Reference Nodes

Distilled Operational Understanding nodes for the Widgets primitive, grouped by category.

### Widgets — Setup & Lifecycle

| Task | Read This File |
|---|---|
| Scope a Widget feature — edition, profile, cap, supported locations | [widgets-overview.dou.md](../assets/widgets/widgets-overview.dou.md) |
| Install zet CLI and run the init / run / validate / pack lifecycle | [widgets-zet-cli.dou.md](../assets/widgets/widgets-zet-cli.dou.md) |
| Full 7-step widget development + packaging workflow | [widgets-dev-workflow.dou.md](../assets/widgets/widgets-dev-workflow.dou.md) |
| Host, register, associate, download, or delete a Widget | [widgets-usage.dou.md](../assets/widgets/widgets-usage.dou.md) |
| Mark a Widget mobile-compatible for the CRM mobile app | [widgets-mobile-compatibility.dou.md](../assets/widgets/widgets-mobile-compatibility.dou.md) |

### Widgets — JS SDK

| Task | Read This File |
|---|---|
| Scaffold a Widget bootstrap and wire `ZOHO.embeddedApp` listeners (PageLoad / Dial / Notify / ContextUpdate) before the single `init()` | [widgets-jssdk-events.dou.md](../assets/widgets/jssdk/widgets-jssdk-events.dou.md) |
| Prompt the user via `ZDK.Client` dialogs / loaders / popups or close a popup via `$Client.close` | [widgets-jssdk-client.dou.md](../assets/widgets/jssdk/widgets-jssdk-client.dou.md) |
| Read, write, search, attach, or delete CRM records via `ZOHO.CRM.API.*` | [widgets-jssdk-api.dou.md](../assets/widgets/jssdk/widgets-jssdk-api.dou.md) |
| Fetch CRM module / field / layout / view / related-list metadata via `ZOHO.CRM.META.*` | [widgets-jssdk-meta.dou.md](../assets/widgets/jssdk/widgets-jssdk-meta.dou.md) |
| Read current-user / org / user-preference context via `ZOHO.CRM.CONFIG.*` | [widgets-jssdk-config.dou.md](../assets/widgets/jssdk/widgets-jssdk-config.dou.md) |
| Egress to an external HTTP service via `ZOHO.CRM.HTTP` / `CONNECTION.invoke` / `CONNECTOR.*` | [widgets-jssdk-egress.dou.md](../assets/widgets/jssdk/widgets-jssdk-egress.dou.md) |
| Invoke a server-side Deluge Function from a Widget via `ZOHO.CRM.FUNCTIONS.execute` | [widgets-jssdk-functions.dou.md](../assets/widgets/jssdk/widgets-jssdk-functions.dou.md) |
| Manipulate CRM UI — resize iframe, open record forms, open WebTab Widgets, control Dialer, close popups | [widgets-jssdk-ui.dou.md](../assets/widgets/jssdk/widgets-jssdk-ui.dou.md) |
| Advance a Blueprint transition or post Wizard form data via `ZOHO.CRM.BLUEPRINT.proceed` / `ZOHO.CRM.WIZARD.post` | [widgets-jssdk-flows.dou.md](../assets/widgets/jssdk/widgets-jssdk-flows.dou.md) |

### Widgets — ZRC (Cross-cutting)

| Task | Read This File |
|---|---|
| Author any ZRC call — three modes (CRM / Connection / External), method signatures + `requestConfig`, four error classes, and recurring patterns (insert, COQL, file, Function execute) | [widgets-zrc-reference.dou.md](../assets/widgets/widgets-zrc-reference.dou.md) |

### Widget Code Patterns

| Task | Read This File |
|---|---|
| Read current record on PageLoad | [#pattern-1-read-record-on-pageload](../assets/widgets/widgets-patterns.dou.md#pattern-1-read-record-on-pageload) |
| Update a CRM field from widget UI | [#pattern-2-update-field-from-widget](../assets/widgets/widgets-patterns.dou.md#pattern-2-update-field-from-widget) |
| Search + display related records | [#pattern-3-search-and-display-related-records](../assets/widgets/widgets-patterns.dou.md#pattern-3-search-and-display-related-records) |
| Personalise widget with current user | [#pattern-4-personalise-with-current-user](../assets/widgets/widgets-patterns.dou.md#pattern-4-personalise-with-current-user) |
| Deployment association paths per placement | [#deployment-association-paths](../assets/widgets/widgets-patterns.dou.md#deployment-association-paths) |
