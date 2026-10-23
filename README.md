# Zoho CRM Agent Skills

A collection of portable Agent Skills for building, automating, and working with Zoho CRM using AI coding agents.

These skills provide domain-specific knowledge and orchestration logic that help compatible AI agents select the right Zoho CRM development tool, generate implementation-ready code, and validate the result.

## Available Skills

### zoho-crm

The zoho-crm skill provides an orchestration layer for Zoho CRM v8.0 developer capabilities.

It helps AI agents work across:

* REST APIs
* Deluge Functions
* ClientScript
* Widgets
* COQL
* Queries Workbench
* Connections

The skill combines routing logic, primitive selection, code generation, and validation with authoritative reference material for each CRM developer capability.

Learn more about the zoho-crm skill from its [README](/skills/zoho-crm/README.md).

## Antigravity Plugin

This repository also ships as a plugin for Antigravity. The plugin bundles the zoho-crm skill together with rules, reviewer agents, and a Zoho MCP server configuration, so the agent can write Zoho CRM code and work with live CRM data in one setup.

| Component | Path | Purpose |
| --- | --- | --- |
| Plugin manifest | [plugin.json](/plugin.json) | Plugin name, version, description, logo, suggested prompts, and license. |
| Skill | [skills/zoho-crm/](/skills/zoho-crm) | The zoho-crm orchestration skill and its reference material. |
| Rules | [rules/zoho-crm.md](/rules/zoho-crm.md) | Common rules applied by model decision: DOU as source of truth, API names, no invented names, placeholder secrets, error handling, and honest validation. |
| Agents | [agents/](/agents) | Read-only reviewers the main agent delegates to before presenting code. |
| MCP config | [mcp_config.json](/mcp_config.json) | Connects the `ZohoMCP` server for live CRM data. |
| Assets | [assets/](/assets) | Plugin logo. |

### Agents

| Agent | Reviews |
| --- | --- |
| `zoho-crm-code-reviewer` | Deluge functions, COQL queries, and CRM REST API requests. |
| `zoho-crm-clientscript-validator` | ClientScript code, including ZDK calls and runtime rules. |
| `zoho-crm-widget-validator` | Widget code, including JS SDK calls, bootstrap, egress, and packaging rules. |

The agents check code against the bundled docs. They do not rewrite or run it, and they have no write, MCP, or subagent tools.

### MCP Server

[mcp_config.json](/mcp_config.json) registers a `ZohoMCP` server:

```json
{
  "mcpServers": {
    "ZohoMCP": {
      "serverUrl": "https://crm.zohomcp.in/mcp/message"
    }
  }
}
```

Update `serverUrl` to point to your own Zoho MCP server if it differs. Authenticate through the MCP client; never put credentials in this file.

## Repository Structure

```text
crm-skills/
├── plugin.json
├── mcp_config.json
├── LICENSE
├── README.md
├── agents/
│   ├── zoho-crm-code-reviewer.md
│   ├── zoho-crm-clientscript-validator.md
│   └── zoho-crm-widget-validator.md
├── assets/
│   └── logo.png
├── rules/
│   └── zoho-crm.md
└── skills/
    └── zoho-crm/
        ├── SKILL.md
        ├── README.md
        ├── references/
        │   ├── api/
        │   ├── functions/
        │   ├── clientscript/
        │   ├── widgets/
        │   ├── coql/
        │   ├── queries/
        │   └── connections/
        └── assets/
            ├── api/
            ├── functions/
            ├── clientscript/
            ├── widgets/
            ├── coql/
            ├── queries/
            └── connections/
```

Each skill is self-contained and can be installed independently into a compatible Agent Skill environment.

## Installation

### Skill

The recommended way to install a skill is using the skills CLI.

For example, to install zoho-crm:

```bash
npx skills add zoho/crm-skills 
```

Refer to the skill-specific README for installation options, supported agents, manual installation, upgrades, and troubleshooting.

### Antigravity Plugin

Clone the repository and install it as a plugin in Antigravity:

```bash
git clone https://github.com/zoho/crm-skills.git
```

Antigravity reads [plugin.json](/plugin.json) to register the skill, rules, agents, and MCP configuration. Try one of the suggested prompts, for example:

* Write a Deluge function that updates a Deal's stage when its related Task is closed
* Write a COQL query for all open Leads created this month, with their owner names
* Create a ClientScript that hides the Fax field on Contacts when Lead Source is Web

## Versioning

Each skill maintains its own version in the YAML frontmatter of its SKILL.md.

For example:

```yaml
---
name: zoho-crm
description: 'Zoho CRM v8.0 orchestration layer...'
metadata:
  version: "0.0.1"
---
```

As the repository grows, each skill may evolve independently and follow semantic versioning.

The Antigravity plugin is versioned separately in [plugin.json](/plugin.json) (currently `1.0.0`).

## License

Licensed under the Apache License 2.0. See [LICENSE](/LICENSE).