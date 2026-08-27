FILE_PURPOSE: Read when reading global CRM context inside a Client Script — current user (role / profile / type), environment (production / sandbox), deployment DC (US / EU / CN / JP / IN / AU), or org metadata — via the `$Crm` utility.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/$Crm
TRIGGER_KEYWORDS: $Crm.user, $Crm.environment, $Crm.deployment, $Crm.org, Regular User, Client Portal User, production sandbox, US EU CN JP IN AU

TECHNICAL_CONSTRAINTS:
- `$Crm` is a global utility namespace; properties are accessed as `$Crm.<prop>` (source examples use property-access syntax, not method-call syntax — e.g. `$Crm.user`, `$Crm.environment`). The source signatures `(){Object}` / `(){string}` suggest method form, but every example accesses as a property.
- `$Crm.user` returns an Object describing the presently logged-in user. **Shape differs by user type:**
  - **Regular User** keys: `id`, `zuid`, `full_name`, `first_name`, `email`, `last_name`, `type` (`"Regular User"`), `date_format`, `role: {id, name}`, `profile: {id, name}`.
  - **Client Portal User** keys: `id`, `zuid`, `full_name`, `first_name`, `email`, `last_name`, `date_format`, `type` (`"Client Portal User"`), `role: {id, name}` (e.g. `{name:"Portal User"}`), `profile: {id, name}` (e.g. `{name:"ClientPortal"}`). **Portal User output in source does not include `date_format` in the same position but does include it — verify ordering not significant.**
- `$Crm.environment` returns one of the literal strings `'production'` | `'sandbox'`.
- `$Crm.deployment` returns one of the literal DC tokens `'US'` | `'EU'` | `'CN'` | `'JP'` | `'IN'` | `'AU'`.
- `$Crm.org` returns an Object: `{ type: String, domain_name: String, name: String, id: String }`. Source example: `{ type: "production", domain_name: "org77591XXXX", name: "Zoho", id: "77591XXXX" }`.

REQUIRED_PARAMETERS:
- `$Crm.user` — no invocation; property-access returns Object.
- `$Crm.environment` — no invocation; property-access returns string.
- `$Crm.deployment` — no invocation; property-access returns string.
- `$Crm.org` — no invocation; property-access returns Object.

UI_ONLY_ACTIONS:
- Sandbox / production environment switching is a Setup → Developer Space → Sandbox action. The script reads the current value via `$Crm.environment` but cannot switch environments.
- DC residency / data-centre assignment is set at org-provisioning time. `$Crm.deployment` reads it; there is no API equivalent to change it.

CRITICAL_FAILURE_MODES:
- **`$Crm.deployment` token gates base-URL construction** — code that hard-codes `https://www.zohoapis.com` (US) breaks for EU / IN / AU / etc. users. Build base URLs from `$Crm.deployment` (e.g. `zohoapis.eu`, `zohoapis.in`). (DC-mismatch)
- **`$Crm.environment === 'sandbox'` flag must gate destructive operations** — production / sandbox share the same script body; a script that always hits prod webhooks misroutes from sandbox.
- **User-type branching: `$Crm.user.type`** — `'Regular User'` vs `'Client Portal User'` exposes different navigation, profiles, and module visibility. A script that assumes `'Regular User'` shape silently fails for portal users (some keys may be absent / different).
- **`$Crm.user.profile.name`** is a display label, not an API-stable token — string-compare against `"Administrator"` etc. breaks under profile rename. Compare against `profile.id` for stability. (label-vs-api-name)
- **`$Crm.user.role.name`** is also a display label — same caveat as profile. (label-vs-api-name)
- **`$Crm.org.domain_name`** is the org subdomain (e.g. `org77591XXXX`), not a full URL — concatenation with hard-coded prefix is required.
- **Portal-User `$Crm.user`** output in source omits some keys present for Regular User (no `date_format` shown in the Portal block snippet — though it may be present at runtime). Defensive `??` / `hasOwnProperty` checks recommended.
- **Property-vs-method ambiguity** — if `$Crm.user` is actually a getter that fires on every access, repeated reads in a tight loop may incur cost; cache the value.
