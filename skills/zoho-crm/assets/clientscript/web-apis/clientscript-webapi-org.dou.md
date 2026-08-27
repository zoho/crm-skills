FILE_PURPOSE: Read when fetching org metadata, enabling multi-currency, or managing currency catalogue (home + active currencies) from a ClientScript via `ZDK.Apps.CRM.Org`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/webapi_v2/Org
TRIGGER_KEYWORDS: ZDK.Apps.CRM.Org.fetch, enableMultiCurrency, updateHomeCurrency, fetchCurrencies, fetchCurrencyById, createCurrencies, updateCurrencies, updateCurrencyById, Models.Currencies

TECHNICAL_CONSTRAINTS:
- Surface is `ZDK.Apps.CRM.Org` — single facade for org-level reads and the currency catalogue.
- `fetch` wraps `zoho.com/crm/developer/docs/api/v2/get-org-data.html`.
- `enableMultiCurrency` wraps `enable-multi-currency.html`.
- `updateHomeCurrency` wraps `update-home-currency.html`.
- `fetchCurrencies` / `fetchCurrencyById` wrap `get-currencies-data.html`.
- `createCurrencies` wraps `add-currencies.html`.
- `updateCurrencies` / `updateCurrencyById` wrap `update-currencies.html`.
- Calls are synchronous from script perspective — return value is the `Org` / `Currencies` object or array directly.
- `Currencies` model built via `new ZDK.Apps.CRM.Org.Models.Currencies()`.
- `Currencies` scalar fields: `prefix_symbol` (boolean), `name`, `iso_code`, `symbol`, `exchange_rate` (string).
- `Currencies.format` is a map: `decimal_separator`, `thousand_separator`, `decimal_places` (stringified number per sample).
- `enableMultiCurrency` is a one-time-per-org operation server-side.
- Once multi-currency is enabled, the home-currency mutation surface is `updateHomeCurrency`.
- Additional active currencies after enable are added via `createCurrencies`.
- Source does not enumerate OAuth scope, admin-privilege gating, edition gating, or rate-limit caps for these helpers.

REQUIRED_PARAMETERS:
- Source samples (verbatim) live at SOURCE_DOC under each method heading; re-fetch when authoring a `Currencies` payload or the `format` map.
- `fetch()` — no args; returns single `Org` object.
- `enableMultiCurrency(Currency: Currencies)` — returns `CRMResponses`.
- `enableMultiCurrency` required `Currencies` fields per sample: `prefix_symbol` (boolean), `name`, `iso_code`, `symbol`, `exchange_rate`, `format` map.
- `updateHomeCurrency(Currency: Currencies)` — returns `CRMResponses`.
- `updateHomeCurrency` payload must carry `id` of the existing home currency (seed from `fetchCurrencyById`).
- `fetchCurrencies()` — returns array of `Currencies`.
- `fetchCurrencyById(id: String)` — returns single `Currencies` instance.
- `createCurrencies(arrayOfObjects: Array<Currencies>)` — array form required; returns array.
- `createCurrencies` element fields per sample: `name`, `iso_code`, `symbol`, `exchange_rate`, `format`, `prefix_symbol`.
- `updateCurrencies()` — source signature has no formal arg list; sample passes `[currency]` array of mutated `fetchCurrencyById` results. Returns array.
- `updateCurrencies` elements must carry `id`.
- `updateCurrencyById(Currency: Currencies, currency_id: String)` — explicit id form; returns `CRMResponses`.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- `enableMultiCurrency` invoked on an org that already has multi-currency enabled → server-side rejects (already-enabled).
- Guard `enableMultiCurrency` with a `fetch()` check on the org's `multi_currency` flag before calling.
- `updateHomeCurrency` payload lacking `id` of the existing home currency → API returns invalid-id; do not pass a fresh `Models.Currencies()`.
- If the helper validates field names strictly, a typoed prefix-symbol key is silently dropped and the CRM-side prefix toggle does not change.
- `createCurrencies` called with a single object (non-array) → signature expects `Array<Currencies>`; helper may reject or silently coerce. Wrap in `[…]`.
- `format.decimal_places` provided as integer instead of stringified number → CRM rejects with type-mismatch on some clusters; pass `"2"` per source sample.
- ClientScript invoker without org-admin privileges → org / currency mutation calls return permission-denied server-side even though the surface is exposed.
- Source does not document a `trigger` knob — org / currency mutations fire any configured downstream automation (e.g. currency-change workflows on Deals) without suppression — `automation-interaction`.
- Source does not enumerate error codes.
- Inspect returned response object's `.status` / `.code` / `.message` and consult the linked `Reference API` endpoint per method.
