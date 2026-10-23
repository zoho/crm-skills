---
trigger: model_decision
description: Apply common rules for Zoho CRM skILL, covering DOU, API names, security, errors, and validation.
---
- Treat DOU nodes as the source of truth. When information is ambiguous, fetch the webpage referenced in the relevant DOU page for clarification.
- Always use API names for API operations and coding requirements. Use display labels only for UI configuration steps.
- Never invent API names. Use the Modules and Fields APIs to retrieve valid module and field API names.
- Resolve ambiguity in the requested action, CRM entity, or execution context before implementation.
- Use placeholders for authentication details and other secrets in generated code. Never ask users to provide credentials.
- Account for errors and explain failures without concealing their causes.
- Follow the applicable tool’s validation requirements. Never claim that code was executed or validated unless it actually was.
