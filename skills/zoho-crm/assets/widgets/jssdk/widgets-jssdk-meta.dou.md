FILE_PURPOSE: Read when fetching CRM module / field / layout / custom-view / related-list / assignment-rule metadata from a Widget via `ZOHO.CRM.META.*`.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_META
TRIGGER_KEYWORDS: ZOHO.CRM.META, getModules, getFields, getLayouts, getCustomViews, getRelatedList, getAssignmentRules, module SysRefName, field API name

TECHNICAL_CONSTRAINTS:
- All `META.*` methods return Promises resolved with the matching v2 metadata envelope (`fields[] | modules[] | layouts[] | related_lists[] | custom_views[] | assignment_rules[]`).
- `config.Entity` is the module's **SysRefName** — for stock modules this matches the API name (`Leads`, `Contacts`), for custom modules it is the `CustomModule1`-style identifier exposed in Setup → Modules.
- `getModules()` takes no arguments and lists every module visible to the logged-in user, including custom and disabled-by-profile modules with `creatable / deletable / editable` flags.
- `getFields(config)` returns one entry per field with `api_name`, `field_label`, `data_type`, `custom_field`, `visible`, and lookup metadata for lookup / multiselect-lookup fields.
- `getLayouts(config)` lists all module layouts; `config.LayoutId` (string) optional — when supplied, returns the specific layout's section + field tree.
- `getCustomViews(config)` lists views; `config.Id` (string) optional — when supplied, returns the specific view's criteria + fields.
- `getRelatedList(config)` returns each related list with `api_name`, `display_label`, `visible`, `type` (`default | lookup | custom`), and `href` template containing `{ENTITYID}` placeholder.
- `getAssignmentRules(config)` returns rules scoped to `config.Entity`.
- All META calls execute under logged-in user auth — profile-restricted modules / fields / layouts are filtered from the response.

REQUIRED_PARAMETERS:
- `getModules()` — no args.
- `getFields({ Entity })` — `Entity` mandatory string (SysRefName).
- `getLayouts({ Entity, LayoutId? })`.
- `getCustomViews({ Entity, Id? })`.
- `getRelatedList({ Entity })`.
- `getAssignmentRules({ Entity })`.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- `config.Entity` populated with the module display label (`"Contact"`, `"Lead"`) instead of the SysRefName / API name (`Contacts`, `Leads`): returns `INVALID_MODULE` or empty — `label-vs-api-name`.
- `getFields` consumer keys downstream record writes by `field_label` instead of `api_name`: write succeeds with the field unset — always index on `api_name`.
- `getLayouts` invoked without `LayoutId` when caller needs the active layout for the current record: response lists all layouts — cross-reference the record's `Layout.id` via [widgets-jssdk-api.dou.md](./widgets-jssdk-api.dou.md) `getRecord` first.
- `getRelatedList` `href` template used verbatim: `{ENTITYID}` is a literal placeholder requiring substitution — replace before navigating.
- `getCustomViews` `Id` populated with the view display name instead of the numeric view ID: returns empty / error — `label-vs-api-name`.
- Cached `getModules` / `getFields` result reused after the org admin edited a layout or field: stale field list keys writes against removed fields — re-fetch on every Widget mount or invalidate on `ContextUpdate`.
- `getFields` response field with `visible: false` written by the caller anyway: write succeeds at the API layer while the user cannot see the field — surface visibility check before exposing it in the Widget UI.
- Lookup-type field metadata used to resolve the related module by `field_label` instead of the lookup `module.api_name` inside the field entry: subsequent `getRecord` against wrong module silently returns 404.
- `getAssignmentRules` returned list filtered by user-profile permissions — rule visible to admins is absent for non-admin Widget viewers; do not assume `rules.length === total`.
- Custom-module SysRefName guessed from the plural label (`Projects` → `Projects`) when the actual SysRefName is `CustomModule1`: API rejects — read from `getModules()` once and cache the mapping.
- `getLayouts` response section / field tree iterated without checking `subform` / `lookup` nested layouts: nested sections silently dropped from the rendered form.
- Translation-enabled org: `field_label` value is locale-dependent and changes per logged-in user — never key UI logic on the label, only on `api_name`.
- `getModules` ignored `editable`, `deletable`, `creatable` flags: caller exposes a write action on a read-only module — honour the flags.
- `getFields` `data_type` of `lookup` vs `userlookup` vs `ownerlookup` confused: each requires a different write-payload shape — branch on `data_type` before composing writes.
- Subform metadata read from `getFields` parent-module response: subform fields live under their own module — call `getFields` again for the subform-module API name.
- Caching `getRelatedList` response when admin reordered or hid related lists in Setup: stale list — invalidate per Widget mount.
- `getCustomViews` returned view criteria interpreted as the search-API criteria: shape differs — use the search-API endpoint for runtime filtering, not the view's stored criteria.
- `getLayouts` `LayoutId` populated with the layout display name: API rejects — use the numeric ID.
- `getAssignmentRules` result interpreted as runtime assignment: rules apply server-side on insert / update — the Widget cannot pre-assign.
- Lookup-field metadata `module.api_name` substituted with `module.singular_label`: subsequent `getRecord` against wrong module 404s.
- `getModules` `api_name` and SysRefName treated as always equal: custom modules diverge (e.g. SysRefName `CustomModule1`, `api_name` `Projects`) — use the field the downstream call requires.
- Field `pick_list_values` order assumed stable across calls: admin reordering re-orders the array — sort by `display_value` if order matters.
- `getFields` for a module the user lacks read access to: returns 403 — catch and fall back to a feature-disabled UI state.
- Layout-section field assumed visible because the field itself is `visible: true`: the section's `visible` flag also gates rendering — honour both.
