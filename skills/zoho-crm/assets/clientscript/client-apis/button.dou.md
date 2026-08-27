FILE_PURPOSE: Read when scripting against a page Button object obtained via `ZDK.Page.getButton(api_name)` or `ZDK.Page.getButtons()` to read button metadata or programmatically click / enable / disable / relabel a button.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Button
TRIGGER_KEYWORDS: ZDK.Page.getButton, ZDK.Page.getButtons, Button.click, Button.disable, Button.enable, Button.setLabel, Button.getApiName, Button.getType, record_save

TECHNICAL_CONSTRAINTS:
- Button instances are obtained only via `ZDK.Page.getButton(api_name)` (single, by API name) or `ZDK.Page.getButtons()` (Array of all buttons on the current page) — Button is not directly constructible.
- `getType()` returns one of the literal strings `'system'` or `'custom'` (source `Output: system or custom`).
- `getApiName()` returns the button's API name (e.g. `record_save`); `getLabel()` returns the displayed label (e.g. `Save`). These are distinct values — never substitute one for the other when re-acquiring the button.
- `getId()` returns a numeric-string handle (source example output: `1101122131`). Treat as opaque.
- `click()`, `disable()`, `enable()`, `setLabel(label)` are mutator calls and return nothing in the source signature.

REQUIRED_PARAMETERS:
- `ZDK.Page.getButton(api_name)` — `api_name: String` — the button's API name (e.g. `'record_save'`). Source example uses the literal `'record_save'`.
- `ZDK.Page.getButtons()` — no params; returns `Array<Button>`.
- `getId() {String}` — no params; returns String id.
- `getType() {String}` — no params; returns `'system'` | `'custom'`.
- `getLabel() {String}` — no params; returns displayed label.
- `getApiName() {String}` — no params; returns API name.
- `click()` — no params; initiates the button's click event.
- `disable()` — no params; disables the button.
- `enable()` — no params; enables the button.
- `setLabel(label)` — `label: String` — new label text. Source example: `save_btn.setLabel('Approve & Save')`.

UI_ONLY_ACTIONS:
- Defining a Custom Button (its API name, position, profile visibility) is a Setup → Customization → Modules and Fields → <Module> → Links and Buttons action. The Client API consumes the API name but does not create the button. No API equivalent for Custom Button creation from inside Client Script.

CRITICAL_FAILURE_MODES:
- **`getButton(api_name)` requires the API name, not the label** — passing the display label (e.g. `'Save'` instead of `'record_save'`) returns nothing / fails to resolve the button. (label-vs-api-name)
- **`setLabel()` does not change the API name** — re-acquiring the button after `setLabel('Approve & Save')` still requires the original API name `'record_save'`. (label-vs-api-name)
- **`getButtons()` ordering is not documented** — code that indexes `buttonObj[0]` (source's own pattern) is order-dependent and silently breaks if Setup-side button order changes.
- **`click()` fires the full click pipeline** — any `onClick` event handlers, validation, or save flow attached to the button run; calling `click()` inside an `onClick` listener for the same button risks unbounded recursion. (recursion)
- **`disable()` / `enable()` operate on the live DOM button** — state is not persisted; a re-render of the page (navigation, refresh) reverts the button to its Setup-defined state.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getId` | Create/Edit/Clone, Detail, List | Detail, Create/Edit/Clone, List | Create/Edit |
| `getType` | Create/Edit/Clone, Detail, List | Detail, Create/Edit/Clone, List | Create/Edit |
| `getLabel` | Create/Edit/Clone, Detail, List | Detail, Create/Edit/Clone, List | Create/Edit |
| `getApiName` | Create/Edit/Clone, Detail, List | List, Detail, Create/Edit/Clone | Create/Edit |
| `click` | Create/Edit/Clone, Detail, List | List, Detail, Create/Edit/Clone | Create/Edit |
| `disable` | Create/Edit/Clone, Detail, List | List, Detail, Create/Edit/Clone | Create/Edit |
| `enable` | Create/Edit/Clone, Detail, List | List, Detail, Create/Edit/Clone | Create/Edit |
| `setLabel` | Create/Edit/Clone, Detail, List | List, Detail, Create/Edit/Clone | Create/Edit |
