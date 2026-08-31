# Connections

> DOU nodes are authoritative — see [DOU Reference Nodes](#dou-reference-nodes) below.

Connections wire Zoho CRM to any third-party / Zoho service over **OAuth 2.0**, abstracted by a **link name**. Zoho stores, refreshes, and rotates tokens; your Deluge code just references the link name in `invokeUrl` (or as the `connections` arg in `zoho.crm.*`).

---

## Execution Instructions

1. Read the DOU setup node for the target service.
2. Provide the setup steps from the DOU.
3. Include the link name and the usage pattern for the calling primitive: `invokeurl` (Function), `ZDK.Apps.CRM.Connection.invoke` (ClientScript), `ZOHO.CRM.CONNECTION.invoke` (Widget legacy JS SDK), or `zrc.*` with `connection:` config (ClientScript ZRC — org-level enablement required; Widget ZRC — preferred); see [clientscript.md](./clientscript.md), [widgets-jssdk-egress.dou.md](../assets/widgets/jssdk/widgets-jssdk-egress.dou.md), and [widgets-zrc-reference.dou.md](../assets/widgets/widgets-zrc-reference.dou.md) for the respective contracts.

## When to Use a Connection

| Scenario | Use |
|----------|-----|
| `invokeUrl` to any external OAuth2 API (Slack, Mailchimp, Google, etc.) | **Connection** — pass link name in `invokeUrl`; see [functions.md](./functions.md) for usage |
| Calling Zoho CRM REST API from a function | **Connection** (Zoho OAuth) — preferred over hardcoded tokens; see [api.md](./api.md) for OAuth scopes |
| External HTTP call from a ClientScript | **Connection** — `ZDK.Apps.CRM.Connection.invoke` (standard) or `zrc.*` with `{ connection: '<link_name>' }` (ZRC — org-level enablement required); see [clientscript.md](./clientscript.md) |
| External HTTP call from a Widget | **Connection** — `ZOHO.CRM.CONNECTION.invoke` (legacy JS SDK) or `zrc.*` with `{ connection: '<link_name>' }` (ZRC — preferred); see [widgets.md](./widgets.md) |
| Internal CRM ops (`zoho.crm.create`, `getRecordById`, etc.) | No connection needed — built-ins auth implicitly |
| One-off / no-auth public endpoint | `invokeUrl` with no `connection` |

## Key Constants

| Key | Value |
|---|---|
| Redirect URI | `https://deluge.zoho.com/delugeauth/callback` |
| Setup path | `Setup → Developer Hub → Connections` |
| Zoho dev console | `https://accounts.zoho.com/developerconsole` |
| COQL scope | `ZohoCRM.coql.READ` AND `ZohoCRM.modules.{module}.READ` — both required; `coql.READ` alone → `OAUTH_SCOPE_MISMATCH` |

## Critical Gotcha

In `invokeurl`, **`connection:` must be a literal string**, not a variable. The `connections` parameter on `zoho.crm.*` built-ins **does** accept a STRING variable.

## DOU Reference Nodes

| Task | Read This File |
|---|---|
| Set up a Connection — register OAuth client, link name, authorize, reference in invokeUrl | [connections-setup.dou.md](../assets/connections/connections-setup.dou.md) |
