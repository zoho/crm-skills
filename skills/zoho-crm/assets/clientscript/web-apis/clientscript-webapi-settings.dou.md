FILE_PURPOSE: Read when fetching tags / roles / profiles / territories / module metadata / fields / layouts / related-lists / custom-views / org variables / variable-groups / assignment-rules / approval-process from a ClientScript via `ZDK.Apps.CRM.Settings`, or mutating tags or org variables.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/webapi_v2/Settings
TRIGGER_KEYWORDS: ZDK.Apps.CRM.Settings.fetchTags, createTags, mergeTags, fetchRoles, fetchProfiles, fetchTerritories, fetchAllModules, fetchFields, fetchLayouts, fetchRelatedLists, fetchCustomViews, fetchVariables, fetchVariableGroups, fetchAssignmentRules, fetchApprovalProcess, Models.Tags, Models.Variables

TECHNICAL_CONSTRAINTS:
- Surface is `ZDK.Apps.CRM.Settings` — a single facade aggregating metadata reads for tags, roles, profiles, territories, modules, fields, layouts, related-lists, custom-views, org variables, variable-groups, assignment-rules, and approval-process; plus mutating helpers for tags and org variables.
- Each method wraps a Zoho CRM v2 REST endpoint per source: `get-tag-list.html`, `create-tag.html`, `update-tags.html`, `delete-tag.html`, `tag-record-count.html`, `merge-tags.html`, `get-roles.html`, `get-profiles.html`, `territories.html`, `module-meta.html`, `field-meta.html`, `layouts-meta.html`, `related-list-meta.html`, `custom-view-meta.html`, `get-variables.html`, `delete-variable.html`, `create-variables.html`, `update-variables.html`, `get-variable-group.html`. `fetchAssignmentRules*` and `fetchApprovalProcess*` are documented without `Reference API` links on this page.
- Calls are synchronous from script perspective — return value is the object / array directly.
- Module-scoped tag operations require both the `Tags` payload and the module's API name as a second arg (e.g. `"Leads"`); never the display label.
- Layout / related-list / custom-view / field / assignment-rule reads are scoped per module — pass the module API name.
- `Variables` model built via `new ZDK.Apps.CRM.Settings.Models.Variables()`; required fields per sample: `api_name`, `name`, `value`, `type` (e.g. `"text"`), `variable_group { name }`.
- Source does not enumerate OAuth scope, edition gating, or rate-limit caps for these helpers.

REQUIRED_PARAMETERS:
- Source samples (verbatim) live at SOURCE_DOC under each method heading — re-fetch when authoring a `Tags` / `Variables` payload or when the response shape (e.g. `roles[i].name`, `modules[i].api_name`, `fields[i].api_name`) matters.
- Tags:
    - `fetchTags(api_name: String)` — module API name; returns array of `Tags`.
    - `createTags(arrayOfObjects: Array<Tags> | singleObject, api_name: String)` — `Tags` payload built from `new …Models.Tags()` with `name`.
    - `updateTags(arrayOfObjects, api_name)` and explicit-id form `updateTagsById(Object: Tags, tag_id: String, api_name: String)`.
    - `deleteTagsById(tag_id: String, api_name: String)`.
    - `fetchTagsCount(tag_id: String, api_name: String)` — returns numeric total records tagged.
    - `mergeTags(conflicting_tag_id: String, tag_id: String)` — merges the conflicting tag into the target tag.
- Roles / Profiles / Territories:
    - `fetchRoles()` · `fetchRolesById(id: String)`.
    - `fetchProfiles()` · `fetchProfilesById(id: String)`.
    - `fetchTerritories()` — array; no by-id variant on this page.
- Module metadata:
    - `fetchAllModules()` — array of modules; each carries `api_name`.
    - `fetchFields(module_name: String)` — array of fields with `api_name`.
    - `fetchLayouts(module_name: String)` · `fetchLayoutsById(id: String, module_name: String)`.
    - `fetchRelatedLists(module_name: String)`.
    - `fetchCustomViews(module_name: String)` · `fetchCustomViewsById(id: String, module_name: String)`.
- Org variables:
    - `fetchVariables()` · `fetchVariablesById(id: String)`.
    - `createVariables(array_of_variable_objects: Array<Variables>)` — required fields `api_name`, `name`, `value`, `type`, `variable_group {name}`.
    - `updateVariables(array_of_variable_objects)` and explicit-id form `updateVariablesById(object: Variables, id: String)`.
    - `deleteVariablesByIds(ids: Array<String>)` and singular `deleteVariablesById(id: String)`.
    - `fetchVariableGroups(group_name_or_id: String)` — accepts either the group's name or id.
- Assignment rules / approval process:
    - `fetchAssignmentRules()` · `fetchAssignmentRulesByModule(module: String)`.
    - `fetchApprovalProcess()` · `fetchApprovalProcessById(id: String)`.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- `api_name` / `module_name` / `module` arg passed as display label (`"Lead"`, `"Price Books"`) instead of module API name (`"Leads"`, `"Price_Books"`) → metadata helpers return empty array / not-found; tag mutations are silently scoped to nothing — `label-vs-api-name`.
- `Variables` `api_name` collision with an existing org variable → `createVariables` returns duplicate-api-name; pre-check via `fetchVariables`.
- `Variables.variable_group` reference to a non-existent group name → CRM returns invalid-group; create the group first via UI.
- `mergeTags(conflicting_tag_id, tag_id)` argument ordering reversed → conflicting tag becomes the target; records re-tag under the wrong tag and the originally-intended target is deleted.
- `deleteTagsById` invoked on a tag still in use → CRM may either reject or cascade-untag depending on org policy; verify with `fetchTagsCount` first.
- `fetchLayoutsById` / `fetchCustomViewsById` arg order — `(id, module_name)` not `(module_name, id)` — reversing them silently returns not-found.
- `updateTags` / `updateVariables` payload not seeded from a `fetch*` result → missing `id` → API rejects update.
- `fetchAssignmentRules*` and `fetchApprovalProcess*` — source does not link a `Reference API` doc; response shape is undocumented on this page.
- ClientScript invoker without admin / setup-modify privileges → mutating helpers (`createTags`, `updateTags`, `deleteTagsById`, `mergeTags`, `createVariables`, `updateVariables`, `deleteVariables*`) return permission-denied server-side.
- Source does not document a `trigger` knob — tag / variable mutations fire any configured downstream automation without suppression — `automation-interaction`.
- Source does not enumerate error codes; inspect returned `CRMResponses` `.status` / `.code` / `.message` and the linked `Reference API` endpoint per method.
