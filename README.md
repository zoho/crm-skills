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

## Repository Structure

```text
crm-skills/
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

The recommended way to install a skill is using the skills CLI.

For example, to install zoho-crm:

```bash
npx skills add zoho/crm-skills 
```

Refer to the skill-specific README for installation options, supported agents, manual installation, upgrades, and troubleshooting.

## Versioning

Each skill maintains its own version in the YAML frontmatter of its SKILL.md.

For example:

---
name: zoho-crm
description: 'Zoho CRM v8.0 orchestration layer...'
metadata:
  version: "0.0.1"
---

As the repository grows, each skill may evolve independently and follow semantic versioning.