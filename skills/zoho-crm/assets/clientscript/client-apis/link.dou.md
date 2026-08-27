FILE_PURPOSE: Read when scripting against a page Link object obtained via `ZDK.Page.getLinks()` to read a Custom Link's id / name or programmatically click / enable / disable it.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Link
TRIGGER_KEYWORDS: ZDK.Page.getLinks, Link.getId, Link.getName, Link.click, Link.disable, Link.enable, custom link

TECHNICAL_CONSTRAINTS:
- Link instances are obtained via `ZDK.Page.getLinks()` (Array of all links on the current page). Source does not document a single-link accessor by name.
- `getId()` returns a numeric-string handle (source example output: `11021234562`). Treat as opaque.
- `getName()` returns the link's name token (source example output: `my_link`).
- `click()`, `disable()`, `enable()` are mutator calls and return nothing in the source signature.

REQUIRED_PARAMETERS:
- `ZDK.Page.getLinks()` — no params; returns `Array<Link>`.
- `getId() {String}` — no params; returns String id.
- `getName() {String}` — no params; returns the link's name token.
- `click()` — no params; initiates the link's click event.
- `disable()` — no params; disables the link.
- `enable()` — no params; enables the link.

UI_ONLY_ACTIONS:
- Creating / configuring a Custom Link (its name, URL pattern, profile visibility, merge-fields) is a Setup → Customization → Modules and Fields → <Module> → Links and Buttons action. The Client API consumes the link object but does not create it. No API equivalent for Custom Link creation from inside Client Script.

CRITICAL_FAILURE_MODES:
- **`getLinks()` ordering is not documented** — code that indexes `linkObj[0]` (source's own pattern) is order-dependent and silently breaks if Setup-side link order changes.
- **`click()` fires the full link-click pipeline** — for a custom link that navigates / opens a URL, the navigation happens. Calling `click()` inside an `onClick` handler for the same link risks unbounded recursion. (recursion)
- **`disable()` / `enable()` operate on the live DOM link** — state is not persisted; a re-render of the page reverts the link to its Setup-defined state.
- **No per-link `getApiName()` documented** — if `getName()` returns the display label (not the API name), there is no way to re-acquire the same link by stable identifier across renders.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getId` | Detail | Detail, List | — |
| `getName` | Detail | Detail, List | — |
| `click` | Detail | Detail, List | — |
| `disable` | Detail | Detail, List | — |
| `enable` | Detail | Detail, List | — |
