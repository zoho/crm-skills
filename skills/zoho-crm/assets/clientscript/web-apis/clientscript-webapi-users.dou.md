FILE_PURPOSE: Read when fetching, creating, updating, or deleting CRM org users from a ClientScript via the `ZDK.Apps.CRM.Users` Web API v2 facade.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/webapi_v2/Users
TRIGGER_KEYWORDS: ZDK.Apps.CRM.Users.fetch, ZDK.Apps.CRM.Users.fetchById, ZDK.Apps.CRM.Users.create, ZDK.Apps.CRM.Users.update, ZDK.Apps.CRM.Users.deleteById, Models.Users, profile, role

TECHNICAL_CONSTRAINTS:
- Surface is `ZDK.Apps.CRM.Users` — single facade.
- No per-user instance method namespace documented beyond field reads on the returned `Users` object.
- `fetch` wraps `zoho.com/crm/developer/docs/api/v2/get-users.html`.
- `create` wraps `add-user.html`.
- `update` wraps `update-user.html`.
- `deleteById` wraps `delete-user.html`.
- Calls are synchronous from script perspective.
- Return value is the user object / array directly — not a Promise.
- Source documents only five methods (`fetch`, `fetchById`, `create`, `update`, `deleteById`); admin-side bulk operations and reactivation are not in scope of this page.
- New `Users` instance constructed via `new ZDK.Apps.CRM.Users.Models.Users()`.
- User fields exposed as snake_case scalars: `first_name`, `last_name`, `email`, `profile`, `role`.
- `profile` and `role` are id strings, not names.
- Source does not enumerate OAuth scope, admin-privilege gating, edition gating, or rate-limit caps for these helpers.
- Source page lists exactly five methods on this surface; reactivation / activation toggles and `type=AllUsers|ActiveUsers|...` filter are not documented here.
- `fetch` return order is not documented — do not rely on the array being sorted by `id`, `email`, or `last_name`.
- The `Models.Users` constructor exposes only the five fields used in the source sample; additional user attributes documented in `add-user.html` may or may not be settable through this constructor.
- Source page does not document a paginated `fetch(page?, per_page?)` overload — the array returned by `fetch()` may already be truncated by the underlying endpoint's default page size.

REQUIRED_PARAMETERS:
- Source samples (verbatim) live at SOURCE_DOC under each method heading; re-fetch when authoring a `Users` model payload with fields beyond the five named below.
- `fetch()` — no args; returns array of `Users`.
- `fetch()` — source does not document paging or a `type` filter on this facade.
- `fetchById(id: String)` — returns single `Users` instance.
- `create(arrayOfObjects: Array<Users> | singleObject)` — payload built from `new ZDK.Apps.CRM.Users.Models.Users()`; returns array.
- `create` required fields per sample: `first_name`, `last_name`, `email`, `profile` (profile id string), `role` (role id string).
- `update(arrayOfObjects: Array<Users> | singleObject)` — payload seeded from `fetchById` then mutated.
- `update` requires `id` on each payload object (set by the prior `fetchById`).
- `deleteById(id: String)` — returns array.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- `profile` supplied as display name (`"Administrator"`) instead of profile id string → CRM rejects with invalid-id / not-found — `label-vs-api-name`.
- `role` supplied as display name (`"CEO"`) instead of role id string → CRM rejects with invalid-id / not-found — `label-vs-api-name`.
- Resolve `profile` ids via [clientscript-webapi-settings.dou.md](./clientscript-webapi-settings.dou.md) `fetchProfiles`.
- Resolve `role` ids via [clientscript-webapi-settings.dou.md](./clientscript-webapi-settings.dou.md) `fetchRolesById`.
- `create` payload missing any of `first_name` / `last_name` / `email` / `profile` / `role` (per source sample) → API returns mandatory-field error.
- `create` helpers do not default missing required fields.
- `create` with `email` already assigned to another org user → API returns duplicate-user error.
- `update` payload built from `new …Models.Users()` instead of a `fetchById` result → missing `id` → API rejects.
- `deleteById` against the last admin user / current-session user → CRM blocks deletion server-side; surface as failure response.
- ClientScript invoker without admin-level CRM privileges → user-mutation calls return permission-denied even though `ZDK.Apps.CRM.Users.*` is in scope.
- Source does not document a `trigger` knob or workflow suppression — user create / update / delete fires whatever user-event automation the org has configured — `automation-interaction`.
- Source does not enumerate error codes; inspect returned response object's `.status` / `.code` / `.message`.
- Consult the linked `Reference API` endpoint per method for the wire-level error catalogue.
