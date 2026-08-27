FILE_PURPOSE: Read when modelling a 5-pattern Healthcare Client Script bundle on Orders / Deals — dynamic lookup filter, widget Flyout, widget pop-up, List Page customization, and getInput pseudo-field pop-up.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/client-script-health-care.html
TRIGGER_KEYWORDS: setCriteria, createFlyout, openPopup, freezeColumns, maskField, getInput, getList, getSubform, $Crm.user

TECHNICAL_CONSTRAINTS:
- Sample modules — Orders (primary), Deals (Sample E), Instruments (lookup target).
- Sample fields (API names): `Type`, `Instruments_List` (subform), `Instrument_Name`, `Instrument_Category`, `Warehouse`, `Shipment_Charge`, `Shipping_Speed`, `Phone`, `Status`, `Description`.
- Dynamic lookup filter is set via `setCriteria(criteria_string, { filterOnSearch: true })` on the Subform's lookup field handle.
- Flyout rendering requires a Widget; `ZDK.Client.createFlyout(<name>, options)` declares the surface and `getFlyout(<name>).open({ api_name, type: 'widget' })` mounts the Widget by Widget API Name.
- Bi-directional Widget messaging: `getFlyout(<name>).notify({ data: ... }, { wait: true })` blocks until the Widget responds; the response is returned synchronously to the Client Script.
- Pop-up widget rendering — `ZDK.Client.openPopup({ id: <widget_id>, type: 'widget', ... }, { data: ZDK.Page.getForm().getValues() })` accepts the widget record ID and a payload.
- List Page customization uses `ZDK.Page.getList()` handle for `freezeColumns`, `style({record, field}, criteria_string)`, `maskField`, `getRecords()`.
- `getList().style(...)` accepts a criteria string in `((Field:operator:Value))` syntax for conditional formatting per row.
- `ZDK.Client.showConfirmation(<message>, <ok_label>, <cancel_label>)` renders inline Markdown inside `<message>` — Sample D embeds `[count + " orders](http://ordersite.com)` link, `_not approved yet_` italics, and `\n\n` paragraph breaks in the prompt text.
- `ZDK.Client.getInput([{type, label}], header, ok_text, cancel_text)` creates a pseudo-field pop-up; pseudo fields do not count against the module's field limit.

REQUIRED_PARAMETERS:
- Sample A (Dynamic lookup filter, Page `onChange` on Orders Create):
    · `ZDK.Page.getField('Type').getValue()` → category.
    · `ZDK.Page.getSubform("Instruments_List").getField("Instrument_Name")` → subform lookup handle.
    · `Product.setCriteria("(Instrument_Category:equals:"+Category+")", { filterOnSearch: true })`.
- Sample B (Flyout):
    · `ZDK.Client.createFlyout('myFlyout', { header, animation_type: 2, height: '400px', width: '420px', top: 'center', right: '0' })`.
    · `getFlyout('myFlyout').open({ api_name: 'flyout_for_warehouse', type: 'widget' })`.
    · `var response = getFlyout('myFlyout').notify({ data: value }, { wait: true })` (synchronous).
    · `getFlyout('myFlyout').close()`; then `Shipment_Charge` / `Shipping_Speed` / `Warehouse` field `setValue(response.<key>)`.
- Sample C (Pop-up Widget):
    · `ZDK.Client.openPopup({ id: '<widget_record_id>', type: 'widget', header, animation_type: 1, close_icon: false, height, width, left: 'center' }, { data: ZDK.Page.getForm().getValues() })` returns the response.
- Sample D (List View Customization, List Page Standard `onCustomViewLoad` on Orders):
    · `ZDK.Page.getList().freezeColumns(true)`.
    · `style({record:{backgroundColor}, field:{Status:{backgroundColor, foregroundColor, fontWeight}}}, "((Status:equals:Delivered))")` — repeat per Status value (Cancelled red, Approved blue).
    · `maskField('Phone', { length: 10, character: '*', reverse: false })`.
    · `getList().getRecords()` iteration to count `Status == "Created"` and trigger `ZDK.Client.showConfirmation("Hi " + $Crm.user.full_name + ", ...", 'Yes. Approve!', "No, Not now")` when count > 0.
- Sample E (Pseudo-field pop-up, Field `onChange` on Deals `Stage`):
    · `ZDK.Client.getInput([{ type: 'text', label: 'Comments' }], 'Deal', 'OK', 'Cancel')` returns the user input.
    · Append to `Description`: `notes_field.setValue(notes_field.getValue() + " " + value + "- " + notes_pop_up + ",")`.

UI_ONLY_ACTIONS:
- Create each sample script: `Setup → Developer Hub → Client Script → +New Script → Module = Orders | Deals → Page → Layout → Event → Next → IDE → Save and Close → Enable`. Note: No API equivalent — UI-only.
- Build the Flyout / Pop-up Widget: create the Widget under `Setup → Developer Hub → Widgets` and copy its API Name (Flyout) or record ID (Pop-up) into the Client Script. Note: Widget creation is documented under the Widgets routing rows.

CRITICAL_FAILURE_MODES:
- `setCriteria` operators are restricted — per FAQ #27, only `starts_with` and `equals` are supported (Sample A uses `equals`). Other operators silently fail. (filter-operator-binding)
- Quoted field API names in `getField` / `getSubform` (`Type`, `Instruments_List`, `Instrument_Name`, `Instrument_Category`, `Warehouse`, `Shipment_Charge`, `Shipping_Speed`, `Status`, `Phone`, `Description`) must match the target module exactly — using display labels returns no field. (label-vs-api-name)
- `Status` literal values in `style(...)` criteria strings (`Delivered` / `Cancelled` / `Approved` / `Created`) must match the Status pick-list API values exactly; pick-list label drift silently no-styles the rows.
- Flyout `notify({ wait: true })` blocks the Client Script — combined with the 10 s timeout, the Widget must respond within budget or the script halts. (timeout)
- Sample C's Pop-up Widget record ID `1982484000000482011` is per-org and per-widget; copying the literal into another tenant silently opens nothing.
- Pseudo fields from `getInput` exist only during script execution; calling `setValue` on a pseudo field outside the same script execution does nothing.
- Sample D source contains a stray closing paren in `if (x.Status == "Created"))` — copying the snippet verbatim breaks parse; remove the extra `)`.
- Sample D `getList().getRecords()` only returns records on the loaded view page; off-page records are not iterated, so the "overdue Created" count under-counts on large lists.
- `$Crm.user.full_name` is Portal-aware (returns the Portal user's name) — assume Portal context if Portal is enabled.
