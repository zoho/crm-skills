---
name: zoho-crm
description: 'Zoho CRM v8.0 orchestration layer — primitive selection, code generation, and validation across all CRM developer tools: REST API, Deluge Functions, ClientScript, Widgets, COQL, Queries Workbench, and Connections. Works whether or not MCP tools are connected. Trigger on "Zoho CRM", "Deluge script", "ClientScript", "COQL", "CRM widget", "zoho.crm.*", "invokeurl", "CRM automation", "CRM integration", "CRM query", "Queries Workbench", "Blueprint", "Workflow Rule", or any CRM module operation. Do NOT use for Catalyst, Zoho Creator, or other Zoho products — use the appropriate product skill instead.' 
argument-hint: 'Describe your Zoho CRM use case (e.g. "fetch all open leads", "write a Deluge script to update a field", "create a ClientScript for a custom button")'
metadata: 
  version: "0.0.1"
---

# zoho-crm

## Purpose

Given any use case, this skill:
1. Selects the right primitive, loads the relevant DOU nodes / reference docs
2. Produces the solution (via MCP tools if connected, or as exact payloads) and validates the output

## When to Use

| Use case | Subskill |
|----------|----------|
| Read, create, update, delete CRM records via HTTP | [API](./references/api.md) |
| Write server-side automation / custom functions | [Functions / Deluge](./references/functions.md) |
| Add UI logic to record pages / list views | [ClientScript](./references/clientscript.md) |
| Build embedded UI components | [Widgets](./references/widgets.md) |
| Build a saved query bound to a Canvas view, Kiosk, or Custom Related List (UI-authored in Workbench) | [Queries](./references/queries.md) |
| Query CRM data using COQL (CRM Object Query Language) | [COQL](./references/coql.md) |
| Connect to external services via OAuth | [Connections](./references/connections.md) |

## Step-by-Step Reasoning Flow

### Step 1 — Understand the Goal

| Dimension | Extract | Examples |
|---|---|---|
| Action | What should happen? | fetch, create, update, trigger, display, query |
| Entity | Which CRM module or object? | Leads, Contacts, Deals, custom modules |
| Context | Where does this run? | server-side, UI page, scheduled, event-triggered |

> **Gate**: If any dimension above cannot be unambiguously inferred from a single reasonable interpretation — stop and ask before proceeding to Step 2. Ask only what is necessary; omit optional parameters with clear defaults.

### Step 2 — Select the Right Primitive

Use the **decision matrix** below as the primary routing source. If the use case doesn't match any row, apply the layer rule: **server-side** (no browser access needed) → Function / REST API / COQL / Queries; **browser-side** → Widget / Client Script.

#### Decision matrix — need → use

**Server-side**

| Need | Use |
|---|---|
| Run Deluge backend code in CRM — process records, perform CRUD operations, call Zoho CRM APIs, send emails/SMS, or execute any server-side business logic | **Function** — trigger via Workflow Rule, Blueprint, Schedule, Button, Validation Rule, or Serverless Endpoint |
| Call an external (non-Zoho) API and write the result to CRM | **Function** via Workflow Rule or Button (use a named Connection for auth) |
| Expose custom Deluge logic as REST API for external systems | **Function** via Serverless Endpoint |
| Run a cron job inside CRM | **Function** via Scheduled Function |
| Convert a Custom Related List to a Function | **Function** via `related_list.*` category — the only category that renders data directly on a record detail page; do not clarify unless a different trigger type (button, workflow, API endpoint) is explicitly stated |
| Read / create / update / delete CRM records, or any CRM-specific operation, from an external system or script | **REST API** |
| Fetch CRM data programmatically from Deluge, external API callers, or ad-hoc code | **COQL** |
| Display query-driven data in a Canvas, Kiosk, or Custom Related List | **Queries** (build in Workbench UI — `Setup → Developer Hub → Queries`) |
| Authenticate to an external OAuth service from a Function or ClientScript | **Connections** (create in `Setup → Developer Hub → Connections`; reference by link name in `invokeurl` or `ZDK.Apps.CRM.Connection.invoke`) |

**Browser-side**

| Need | Use |
|---|---|
| Render or embed custom HTML or a third-party UI component inside CRM | **Widget** |
| Hide a field based on another field's value, or any other web UI customization on a record page | **Client Script** |
| Validate field input before saving a record in CRM web UI | **Client Script** (instant UI feedback) or **Function** via Validation Rule (server-side enforcement) — default to **Client Script** unless the user explicitly requires server-side enforcement |
| Show a confirmation dialog before a button action in web UI | **Client Script** (dialog) + **Function** (backend action) |

> **Tiebreaker**: Default to the first listed option; override only if the user's context explicitly favors the second.

> **Check**: Confirm the selected primitive matches Action + Entity + Context from Step 1. If not — re-check the matrix or loop back to clarification.

> **Universal constraint**: Use API names for all module and field references — never display labels.

## Authoritative Sources Hierarchy

**When in doubt about syntax, signatures, or limits, consult sources in this order** (not by preference or recollection):

1. **DOU Nodes** (`assets/`) — Current method signatures, parameters, return types, and critical failure modes. **Use this first for code generation.**
2. **Official Zoho Public Docs** (zoho.com/deluge/help/, zoho.com/crm/api/) — When a DOU node is partial or missing.
3. **Reference files + inline examples** (api.md, functions.md, etc.) — Curated summaries; may lag behind DOU or official docs.
4. **Recalled knowledge** — Lowest trust; always cross-check against DOU.

> **Critical Rule**: Reference files are curated summaries, not authoritative. DOU nodes are the ground truth. If a reference file example conflicts with a DOU node, the DOU node wins.

### Step 3 — Load the Reference for the Selected Primitive

Open the reference file for the primitive matched in the "When to Use" table above and follow its **Execution Instructions**. (Special case: if the primitive is **Queries** with source type COQL, also open [references/coql.md](./references/coql.md).)

> If a reference file is inaccessible, inform the user, state which file is missing, and do not generate code that depends on its contents.

### Steps 4–5 — Execute and Validate

Follow the **Execution Instructions** in the reference file from Step 3. After presenting the solution, run its **Validation Checklist**; surface errors with plain-language explanations and suggest follow-up steps if the goal is only partially met.

## Auth & Scope Reference

**Always derive scopes from the OAS spec file** (per [api.md](./references/api.md) Step 6, `security` field at operation level). For all standard scopes, use the OAS spec — the table below covers the non-obvious cases only.

| Scope | Note |
|-------|------|
| `ZohoCRM.coql.READ` and `ZohoCRM.modules.{module}.READ` | COQL queries — **two separate scopes required**; `coql.READ` alone → `OAUTH_SCOPE_MISMATCH` |

Base URL: `https://www.zohoapis.com/crm/v8/`