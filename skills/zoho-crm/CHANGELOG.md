# Changelog

All notable changes to this project will be documented in this file.

## [0.0.2] — 2026-09-18

### Added

- Added `clientscript-event-type-matrix.dou.md` with a unified **Page → Type → Events** lookup for all 8 ClientScript page surfaces, including Type configuration sources and Field selectors.
- Added `(Type: ...)` annotations to all ClientScript event documentation.

### Fixed

- Corrected `clientscript-creation.dou.md` to reflect Page-specific Type options and clarify Commands, Wizard, and Subform Event behavior.
- Updated `references/clientscript.md` to require Type + Event in ClientScript responses.
- Restricted generated ClientScript code from using top-level `function` wrappers or module-level globals. Named functions must be defined in Static Resource `.js` files.

## [0.0.1] — 2026-08-24

### Added

- Initial release covering all 7 CRM developer primitives: REST API, Deluge Functions, ClientScript, Widgets, COQL, Queries Workbench, and Connections.
- Targets Zoho CRM API v8.0.
- 5-step reasoning flow for primitive selection, code generation, and validation.
- DOU node inventory for authoritative method signatures, parameters, and failure modes.
- Works with or without MCP tools connected.
