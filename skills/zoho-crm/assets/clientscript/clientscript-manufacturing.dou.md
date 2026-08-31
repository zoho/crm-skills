FILE_PURPOSE: Read when modelling a multi-pattern Client Script bundle — third-party fetch with Trusted-Domains, read-only auto-populate, confirmation dialog, static-resource shared validator, and lookup-field auto-population.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/client-script-manufacturing.html
TRIGGER_KEYWORDS: ZDK.Page.getField, ZDK.Page.getForm, ZDK.Client.showConfirmation, setReadOnly, Trusted Domains, fetch, Request module, Quantity_of_Products

TECHNICAL_CONSTRAINTS:
- Sample modules — `Accounts` (sellers + manufacturing units), `Products`, `Category` (custom module), `Request` (custom module).
- Sample fields used in scripts (all API names): `Seller_Location`, `Manufacturer_Location`, `Distance`, `Request_Name`, `Quantity_of_Products`, `Product`, `Category`.
- `Product` and `Category` are Lookup fields in the `Request` module.
- Third-party `fetch(...)` from a Client Script requires the target domain to be whitelisted in Trusted Domains.
- The "Quantity ≥ 100" validation is enforced in two scripts — Field `onChange` on `Quantity_of_Products` AND Page `onSave` — both call the shared `quantityCheck(...)` static resource.
- Lookup-field auto-population accepts a `{ "id": "<record_id>", "name": "<display>" }` object via `setValue`.
- Page `onChange` (or Field `onChange`) is interchangeable for many of these patterns — Field `onChange` runs only for the specific field; Page `onChange` runs for every field change on the page.

REQUIRED_PARAMETERS:
- Sample A — Distance auto-population via third-party API:
    · Event: Page `onChange` on Create Page of `Request`; gated by `field_name === "Seller_Location" || field_name === "Manufacturer_Location"`.
    · Calls: `ZDK.Page.getField("Distance").setReadOnly(true)`; `ZDK.Page.getForm().getValues()`; `fetch("https://api.***/maps/api/dist**/json?origins=…&destinations=…&key=…")`; on resolution, `distance.setValue(data.rows[0].elements[0].distance.text)`.
- Sample B — `Request_Name` read-only auto-populate:
    · Event: Page `onLoad` on Create Page of `Request`.
    · Calls: `reqName_field.setValue("REQ-" + dd + "-" + mm + "-" + yyyy)`; `reqName_field.setReadOnly(true)`.
- Sample C — Quantity validator (Static Resource `quantityCheck(quantity)` shared across two scripts):
    · JS file body: `if (quantity < 100) { quantity_field.showError("Minimum Quantity is 100"); }`.
    · Script 1 — Field `onChange` on `Quantity_of_Products`: `quantityCheck(value);`.
    · Script 2 — Page `onSave`: read via `ZDK.Page.getField("Quantity_of_Products")` then `quantityCheck(qty_field);`.
- Sample D — Confirmation on save:
    · Event: Page `onSave` on Create Page of `Request`.
    · Single-arg form: `ZDK.Client.showConfirmation('Your Request is submitted and will be shipped within 4 days.');`.
    · Two-button form: `var isProceed = ZDK.Client.showConfirmation('…', 'Proceed', 'Cancel'); if (isProceed) { return true; } else { return false; }` — `return false` cancels the save.
- Sample E — Auto-populate `Category` lookup from `Product` lookup:
    · Event: Field `onChange` on `Product` (or Page `onChange` gated on `field_name === 'Product'`).
    · Logic: branch on `value.name` ∈ {Airbag sensor, Light sensor, Fuel level sensor} ⇒ Category = Sensors id; ∈ {Ignition Switch, Thermostat, Battery} ⇒ Category = Electrical Switches id.
    · Call: `ZDK.Page.getField('Category').setValue({ "id": "<lookup_id>", "name": "<display>" });` — lookup IDs are org-specific.

UI_ONLY_ACTIONS:
- Whitelist the third-party API host: `Setup → Developer Space → Trusted Domains → add domain` before running Sample A. Note: No API equivalent — UI-only.
- Create each of the five sample scripts via `Setup → Developer Hub → Client Script → +New Script → Module = Request → Page = Create Page → Layout → Event Type / Field → Next → IDE → Save and Close → Enable`. Note: No API equivalent — UI-only.
- Upload the `quantityCheck` static resource: `Setup → Developer Hub → Client Script → Static Resources tab → New Resource → choose .js file → Save`, then add to both Quantity scripts via the right-pane Static Resources panel. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- `fetch(...)` to a domain not present in Trusted Domains is blocked at request time; the promise rejects and `distance.setValue` never runs. (trusted-domain)
- Lookup `setValue({"id": "…", "name": "…"})` IDs are per-org — copying the sample IDs `4967860000001049208` / `4967860000001049217` into another org sets an invalid lookup.
- Sample A's `fetch` call returns immediately; the `.then(...).then(...)` chain runs after the Client Script handler returns — long-latency APIs risk exceeding the 10 s execution budget (see [clientscript-best-practices.dou.md](./clientscript-best-practices.dou.md) for the loader pattern).
- `Product` and `Category` are Lookup fields — `value` inside `onChange` is a `{ id, name }` object, not a string; using `value === 'Airbag sensor'` silently fails.
- The `quantityCheck` static resource references `quantity_field` without defining it — the calling script must define `quantity_field = ZDK.Page.getField("Quantity_of_Products")` in the enclosing scope, else `showError` throws.
- Two scripts (Field `onChange` and Page `onSave`) sharing the same validator double-fire on Save — by design, but be aware of order via Reorder (see [clientscript-best-practices.dou.md](./clientscript-best-practices.dou.md)).
- `setReadOnly(true)` enforced in the script does not survive a layout change — opening the record under a non-bound layout leaves Distance / Request_Name editable. (layout-binding)
- Field API names quoted in samples must exist verbatim in the target `Request` module before activation; renames silently no-op `getField`. (label-vs-api-name)
