# ClientScript Subskill

> DOU nodes are authoritative — see [DOU Reference Nodes](#dou-reference-nodes) below.

ClientScript = Zoho CRM's **browser-side JavaScript** that runs on CRM pages (create / edit / detail / list / wizard / canvas) via the ZDK runtime.

---

## Execution Instructions

1. Read the relevant DOU Reference Node — for Type + Event selection, start with [clientscript-event-type-matrix.dou.md](../assets/clientscript/clientscript-event-type-matrix.dou.md) (fast lookup); then read the matching `eventdict-*.dou.md` for full argument signatures, interceptor semantics, and failure modes.
2. Output the complete JavaScript using ZDK APIs only — no `document`, `window`, or external `fetch`. Never wrap the output in an explicit `function <name>(args) { ... }` declaration, and never declare any variable, constant, or helper outside the executing block — the CRM IDE already supplies the enclosing event-handler function for the bound Page + Type + Event, so everything (including API keys/config) belongs inside the pasted body. The one exception: a separate Static Resource `.js` file may contain a real named `function` declaration, invoked by bare name from the main script (see [clientscript-static-resources.dou.md](../assets/clientscript/clientscript-static-resources.dou.md)).
3. Confirm the target page type, event, and profile/layout binding requirements from the DOU Reference Nodes section in this file. If Category = Module, also state the Type (Event Details → Type dropdown value, e.g. Blueprint Event) alongside the Event name; if Category = Commands, state that no Type/Event applies (Command Palette / keyboard-shortcut trigger only, per [clientscript-commands.dou.md](../assets/clientscript/clientscript-commands.dou.md)).

**Architecture defaults** (apply unless the user explicitly requests otherwise):
- External service calls: use `ZDK.Apps.CRM.Connection.invoke` — direct `fetch` is rejected in the sandboxed environment.

## Validation Checklist

Before delivering the code, verify:

- [ ] All method calls use ZDK APIs only (no `document`, `window`, `fetch`)
- [ ] Event binding matches the DOU Reference Node for the target event
- [ ] Target page type (detail/edit), module, and profile/layout requirements stated
- [ ] Script properly bound in target layout + profile (see Critical Gotcha below)
- [ ] When both show and hide branches are required — used explicit `if/else` for `setVisibility` / `setReadOnly` (not a boolean expression)
- [ ] If `setValue` and `showError` are called on the same field — `setValue` is called first
- [ ] If Category = Module, response states the Type (Event Details → Type dropdown value, e.g. Blueprint Event) alongside the Event name; if Category = Commands, no Type/Event is stated at all
- [ ] If Type is Button Event or a Canvas element event (Canvas Button/Icon/Text Event), response states the actual creation entry point (Buttons page / Canvas element designer respectively) — not the standard Type dropdown
- [ ] Depending on Type: if Field Event, response names the specific Field API name chosen (the only genuine Event-Details "after Type" selector); if Subform Event, response's code correctly targets the intended subform via `ZDK.Page.getSubform(<api_name>)` — not described as a creation-time selector; if Page = Wizard Create/Edit, response separately states which Wizard was chosen in Page Details (applies regardless of Type — not an Event-Details/after-Type selector)
- [ ] Main event script has no top-level `function` wrapper and no variable/constant declared outside the executing block (everything, incl. API keys/config, is inside the body)
- [ ] Reusable logic is placed in a Static Resource `.js` file (named function) and invoked by bare name — never redeclared as a top-level function inside the main event script

## Critical Gotchas

### Layout / profile binding mismatch silently no-fires

A ClientScript is bound to a specific Module + Layout + Page Type + Event + Profile. If the record uses a different layout, or the user's profile lacks the Developer Permissions toggle, the script never runs — no error in console, no entry in execution logs.

**Rule**: When deploying a ClientScript, verify both:
- `Setup → Developer Hub → Client Script → {script} → Layouts` includes every layout that needs it.
- `Setup → Users and Control → Security Control → {Profile} → Developer Permissions → Client Script` is enabled for every profile that needs it.

### No global scope in the main event script

The code pasted into the Client Script IDE's code editor is **only the function body** — the CRM UI already supplies the enclosing event-handler function for the bound Page + Type + Event. There is no module-level or global scope that persists across invocations: a `var`/`let`/`const` declared "above" the executing logic, or an explicit `function name(args) { ... }` wrapper around the whole snippet, is not how the pasted body works and does not behave like a real global.

**Rule**: Declare every variable — including config-like values such as an API key — inside the executing block (e.g. inside the `if (field_name === ...) { ... }` gate itself), never above/outside it, and never show a `function` wrapper around the whole script. The only place a real named `function` declaration belongs is a separate Static Resource `.js` file, uploaded independently and invoked by bare function name from inside the main event script (see [clientscript-static-resources.dou.md](../assets/clientscript/clientscript-static-resources.dou.md)).

## Prerequisites & Hard Limits

- Editions: **Professional, Enterprise, Ultimate** only
- Profile needs **Developer Permissions** (`Setup → Security Control → {Profile}`)
- **30 scripts / page**, **30 Commands / org**, **10 s execution timeout**
- Static Resources: JS only, ≤ 5 MB, 200 / org, 5 / page
- No `document` / `window` access
- External fetches need Trusted Domains whitelist
- Scripts are **layout-specific**

## Primary APIs (at a glance)

- `ZDK.Page.*` — fields, subforms, form, buttons, blueprint transitions, tags
- `ZDK.Client.*` — toasts, alerts, popups, navigation, loader
- `ZDK.UI.*` — freeze / scroll / highlight canvas
- `ZDK.HTTP.request` — external HTTP (15/page cap)
- `ZDK.Apps.CRM.*` — Web API v2 (modules, users, org, functions, connections, settings)
- `zrc` (global) — preferred HTTP client (CRM / Connection / external); **org-level feature enablement required** (unlike Widgets where ZRC is available by default)
- Utility globals: `$Crm`, `$Page`, `$Client`

## DOU Reference Nodes

### Overview, Creation & IDE

| Task | Read This File |
|---|---|
| Scope / edition / limits | [clientscript-overview.dou.md](../assets/clientscript/clientscript-overview.dou.md) |
| Create a Client Script | [clientscript-creation.dou.md](../assets/clientscript/clientscript-creation.dou.md) |
| Pick page + event + cancel semantics | [clientscript-events.dou.md](../assets/clientscript/clientscript-events.dou.md) |
| Pick Type + Event via one fast lookup table | [clientscript-event-type-matrix.dou.md](../assets/clientscript/clientscript-event-type-matrix.dou.md) |
| Command-triggered script | [clientscript-commands.dou.md](../assets/clientscript/clientscript-commands.dou.md) |
| Client Script IDE usage | [clientscript-ide-components.dou.md](../assets/clientscript/clientscript-ide-components.dou.md) |
| Static Resources (shared JS) | [clientscript-static-resources.dou.md](../assets/clientscript/clientscript-static-resources.dou.md) |
| Best practices | [clientscript-best-practices.dou.md](../assets/clientscript/clientscript-best-practices.dou.md) |
| Debug / troubleshoot | [clientscript-troubleshooting.dou.md](../assets/clientscript/clientscript-troubleshooting.dou.md) |
| Operational FAQs | [clientscript-faqs.dou.md](../assets/clientscript/clientscript-faqs.dou.md) |
| Mobile event matrix | [clientscript-mobile.dou.md](../assets/clientscript/clientscript-mobile.dou.md) |

### Use-Case Samples

| Task | Read This File |
|---|---|
| Insurance — onChange validation cascade | [clientscript-insurance.dou.md](../assets/clientscript/clientscript-insurance.dou.md) |
| Manufacturing — fetch + read-only + static-resource | [clientscript-manufacturing.dou.md](../assets/clientscript/clientscript-manufacturing.dou.md) |
| Healthcare — 5-pattern bundle | [clientscript-healthcare.dou.md](../assets/clientscript/clientscript-healthcare.dou.md) |

### Event Dictionary

| Task | Read This File |
|---|---|
| Create / Edit / Clone (Standard) events | [eventdict-create-edit-clone-standard.dou.md](../assets/clientscript/event-dictionary/eventdict-create-edit-clone-standard.dou.md) |
| Detail Page (Standard) events | [eventdict-detail-standard.dou.md](../assets/clientscript/event-dictionary/eventdict-detail-standard.dou.md) |
| List Page (Standard) events | [eventdict-list-standard.dou.md](../assets/clientscript/event-dictionary/eventdict-list-standard.dou.md) |
| Quick Create popup events | [eventdict-quick-create.dou.md](../assets/clientscript/event-dictionary/eventdict-quick-create.dou.md) |
| Create / Edit / Clone (Canvas) events | [eventdict-create-edit-clone-canvas.dou.md](../assets/clientscript/event-dictionary/eventdict-create-edit-clone-canvas.dou.md) |
| Detail Page (Canvas) events | [eventdict-detail-canvas.dou.md](../assets/clientscript/event-dictionary/eventdict-detail-canvas.dou.md) |
| List Page (Canvas) events | [eventdict-list-canvas.dou.md](../assets/clientscript/event-dictionary/eventdict-list-canvas.dou.md) |
| Wizard Create / Edit events | [eventdict-create-edit-wizard.dou.md](../assets/clientscript/event-dictionary/eventdict-create-edit-wizard.dou.md) |

### Client APIs (ZDK)

| Task | Read This File |
|---|---|
| `ZDK.Page.*` — page accessors | [page.dou.md](../assets/clientscript/client-apis/page.dou.md) |
| `ZDK.Client.*` — dialogs / nav / loader | [client.dou.md](../assets/clientscript/client-apis/client.dou.md) |
| `ZDK.HTTP.request` — external HTTP | [http.dou.md](../assets/clientscript/client-apis/http.dou.md) |
| `ZDK.UI.*` — canvas freeze / scroll | [ui.dou.md](../assets/clientscript/client-apis/ui.dou.md) |
| Field object — read / write / state | [field.dou.md](../assets/clientscript/client-apis/field.dou.md) |
| Subform — bulk ops | [subform.dou.md](../assets/clientscript/client-apis/subform.dou.md) |
| Subform row | [subformrow.dou.md](../assets/clientscript/client-apis/subformrow.dou.md) |
| Subform cell | [subformcell.dou.md](../assets/clientscript/client-apis/subformcell.dou.md) |
| Subform field definition | [subformfield.dou.md](../assets/clientscript/client-apis/subformfield.dou.md) |
| Blueprint transition | [blueprinttransition.dou.md](../assets/clientscript/client-apis/blueprinttransition.dou.md) |
| Page Button | [button.dou.md](../assets/clientscript/client-apis/button.dou.md) |
| Custom Link | [link.dou.md](../assets/clientscript/client-apis/link.dou.md) |
| Form — bulk read / write | [form.dou.md](../assets/clientscript/client-apis/form.dou.md) |
| Page Component | [component.dou.md](../assets/clientscript/client-apis/component.dou.md) |
| List view scripting | [list.dou.md](../assets/clientscript/client-apis/list.dou.md) |
| Flyout | [flyout.dou.md](../assets/clientscript/client-apis/flyout.dou.md) |
| `ZDK.HTTP.request` Response object | [response.dou.md](../assets/clientscript/client-apis/response.dou.md) |
| Canvas UI element | [uielement.dou.md](../assets/clientscript/client-apis/uielement.dou.md) |
| `$Crm` — user / org / DC | [crm.dou.md](../assets/clientscript/client-apis/crm.dou.md) |
| `$Client` — client context | [client-util.dou.md](../assets/clientscript/client-apis/client-util.dou.md) |
| `$Page` — page context | [page-util.dou.md](../assets/clientscript/client-apis/page-util.dou.md) |

### Web APIs (ZDK.Apps.CRM)

| Task | Read This File |
|---|---|
| Module CRUD / search / convert | [clientscript-webapi-modules.dou.md](../assets/clientscript/web-apis/clientscript-webapi-modules.dou.md) |
| Record-instance methods | [clientscript-webapi-records.dou.md](../assets/clientscript/web-apis/clientscript-webapi-records.dou.md) |
| Users API | [clientscript-webapi-users.dou.md](../assets/clientscript/web-apis/clientscript-webapi-users.dou.md) |
| Org / currencies | [clientscript-webapi-org.dou.md](../assets/clientscript/web-apis/clientscript-webapi-org.dou.md) |
| Execute a Deluge Function | [clientscript-webapi-functions.dou.md](../assets/clientscript/web-apis/clientscript-webapi-functions.dou.md) |
| Connection-based egress | [clientscript-webapi-connections.dou.md](../assets/clientscript/web-apis/clientscript-webapi-connections.dou.md) |
| Settings metadata | [clientscript-webapi-settings.dou.md](../assets/clientscript/web-apis/clientscript-webapi-settings.dou.md) |

### ZRC

| Task | Read This File |
|---|---|
| `zrc` client (CRM / Connection / external) | [clientscript-zrc.dou.md](../assets/clientscript/zrc/clientscript-zrc.dou.md) |


> **About `zohocrm.dev`**: `https://www.zohocrm.dev/` is Zoho CRM’s new **Developer Space** — a dedicated developer portal that is itself in Early Access. The "Early Access" label on its pages refers to the portal, not the features. All APIs and SDK surfaces documented there (ZRC, ZDK Client API, Web API v2, etc.) are **already live and available in production**.

