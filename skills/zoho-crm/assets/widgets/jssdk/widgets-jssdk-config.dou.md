FILE_PURPOSE: Read when fetching current-user, org, or user-preference context from a Widget via `ZOHO.CRM.CONFIG.*` to gate UI by user / org settings.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_CONFIG
TRIGGER_KEYWORDS: ZOHO.CRM.CONFIG, getCurrentUser, getOrgInfo, getUserPreference, org info, user locale, timezone, currency

TECHNICAL_CONSTRAINTS:
- Three methods exposed: `getCurrentUser()`, `getOrgInfo()`, `getUserPreference()` — all zero-arg, all return Promises.
- `getCurrentUser()` resolves with `{ users: [<user>] }` (array shape, single element) — index `users[0]` to access the record.
- User object fields include `id`, `email`, `role.{id,name}`, `language`, `locale`, `country_locale`, `name_format`, `default_tab_group`, plus address / signature / personal_account.
- `getOrgInfo()` resolves with `{ org: [<org>] }` — single-element array; access `org[0]`.
- Org object fields include `id`, `zgid`, `country`, `country_code`, `currency`, `currency_symbol`, `currency_locale`, `time_zone`, `company_name`, `primary_email`, `primary_zuid`, `license_details`, `mc_status`, `gapps_enabled`, `translation_enabled`.
- `time_zone` is IANA-format (e.g. `America/Los_Angeles`) and applies to **org-default** display — per-user preference overrides this for user-scoped output.
- `getUserPreference()` resolves with the logged-in user's per-account preferences (date format, time format, number format) — source does not enumerate exact payload fields.
- All three methods execute under logged-in user auth; no caller-supplied OAuth scope.
- Responses are point-in-time snapshots — org / user fields refreshed in Setup are visible only on the next call.

REQUIRED_PARAMETERS:
- `getCurrentUser()` — no args.
- `getOrgInfo()` — no args.
- `getUserPreference()` — no args.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- Consumer accesses the response as `data.user` / `data.org` instead of `data.users[0]` / `data.org[0]`: returns `undefined` silently — always destructure the array form.
- Caching `getCurrentUser()` across Widget reloads when admin changed role / profile: stale role gate exposes UI the user should no longer see — refresh on each mount.
- `time_zone` from `getOrgInfo()` applied to a per-user datetime calculation: misaligned with user's local timezone — prefer the user-level timezone when handling user-scoped display.
- `currency_symbol` from `getOrgInfo()` applied to a multi-currency record whose `Currency` field differs from org default: displays wrong symbol — read the record's `Currency` field via [widgets-jssdk-api.dou.md](./widgets-jssdk-api.dou.md) instead.
- `getCurrentUser()` invoked from a Widget hosted on a Settings location where no end-user context exists: response is the active admin's identity, not the record-owner — never use it as record-owner proxy.
- `language` / `locale` value from `getCurrentUser()` used to key cached field-label maps: labels change per locale; index on field API name from [widgets-jssdk-meta.dou.md](./widgets-jssdk-meta.dou.md) instead.
- `personal_account: false` interpreted as "is admin": flag indicates personal-account mode, not role privileges — gate on `role.name` / profile instead.
- `getUserPreference()` consumer assumes a fixed payload shape and accesses a key not returned for that user (e.g. user never set a date format): undefined access — coalesce with sensible defaults.
- `license_details` parsed without null-checking: trial / suspended orgs return null sub-keys — defensive read.
- `mc_status` (multi-currency) flag ignored when displaying amounts: single-currency org assumed but the user later enabled MC — re-read `getOrgInfo()` on Widget mount, not at boot.
- `getOrgInfo` `country_code` used to format phones: country can differ from user's actual country — prefer user-level country when formatting per-user output.
- `translation_enabled: true` ignored when caching field labels: labels are locale-dependent across users — never share label caches across sessions.
- `name_format` from `getCurrentUser` ignored when rendering names: per-user format (e.g. Salutation,First Name,Last Name) drives display order — honour it.
- `default_tab_group` interpreted as a permission gate: it is a UI layout preference, not an authorization signal — do not gate features on it.
- `gapps_enabled` flag treated as Google-Workspace-SSO enabled: flag indicates GApps integration; SSO is a separate org setting.
- `currency_locale` from `getOrgInfo` ignored when formatting amounts: `12,345.67` vs `12.345,67` flips per locale — use `Intl.NumberFormat` keyed on `currency_locale`.
- `getUserPreference` called before the Widget bootstrap completes: SDK returns the default-org preference set, not the user's — await `PageLoad` before reading.
- `role` object cached then compared by string equality after admin rename: stale comparison fails silently — compare by `role.id` not `role.name`.
- `primary_email` from `getOrgInfo` used as the from-address of a Widget-side email integration: org-primary differs from per-Function email-sender context — do not conflate.
- `signature` field read for the per-user email signature: HTML payload — sanitize before embedding in any Widget-rendered DOM.
- `personal_account` flag misread as `is_active`: a true value means personal-account mode is on, not that the user is the org admin.
- `language` `en_US` assumed across users: per-user override exists; localization keys must read the per-user language, not the org default.
- `zia_portal_id: null` treated as feature disabled: null indicates portal not yet provisioned — distinct from the Zia-feature license flag inside `license_details`.
- `time_zone` reused across two CRM orgs sharing one Widget bundle: each org returns its own — always re-fetch per session, never cache cross-tenant.
- `getCurrentUser` response `id` reused as the record-owner ID across modules: works only when the user has an Owner-mapped role — cross-check with module-level owner field.
- `email` field used as a unique key into a Widget-side cache: email changes are allowed in Setup — prefer `id`.
