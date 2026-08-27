FILE_PURPOSE: Read when manipulating a page-level Component (custom-view picker, wizard screen, picklist-style page component) obtained via `ZDK.Page.getComponent(api_name)` — read / set value, toggle visibility, read / write options, or transition wizard screens.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Component
TRIGGER_KEYWORDS: ZDK.Page.getComponent, Component.setValue, Component.getValue, Component.setVisibility, Component.getOptions, Component.setOptions, Component.transitionTo, list-custom-view, record-create-wizard

TECHNICAL_CONSTRAINTS:
- Component instances are obtained via `ZDK.Page.getComponent(api_name)`. Source examples use `"list-custom-view"` (Custom-View picker on a List page) and `"record-create-wizard"` (Wizard screen container on a Create page).
- `setValue(value)` accepts a String — source `list-custom-view` example passes the Custom View's id String (`"4312588000000087501"`).
- `getValue()` returns the component's current value. Source does not document the return type.
- `setVisibility(value)` — `value: boolean` (`true` | `false`).
- `getOptions()` returns the component's current option list. Source does not document the shape.
- `setOptions(options)` — `options: Array` of option Objects. Source example uses `[{ id: "111113000000042834" }, { id: "111113000000042894" }]` — option objects keyed by `id`.
- `transitionTo(api_name)` — applies to wizard-style components. Source example: `ZDK.Page.getComponent("record-create-wizard").transitionTo('Car_Loan')` — transitions to the wizard screen whose API name is `Car_Loan`.

REQUIRED_PARAMETERS:
- `ZDK.Page.getComponent(api_name)` — `api_name: String` — the component's API name (source examples: `"list-custom-view"`, `"record-create-wizard"`).
- `setValue(value)` — `value: String` — component value.
- `getValue()` — no params.
- `setVisibility(value)` — `value: boolean` — `true` shows, `false` hides.
- `getOptions()` — no params.
- `setOptions(options)` — `options: Array` of option Objects (`{ id: String }` per source).
- `transitionTo(api_name)` — `api_name: String` — API name of the destination screen (wizard component only).

UI_ONLY_ACTIONS:
- Defining a Wizard, its screens, and each screen's API name is a Setup → Customization → Wizards action. The Client API drives transitions between existing screens; it does not create them.
- Defining Custom Views (the list of options the `list-custom-view` component exposes) is a Setup → Customization → Modules and Fields → <Module> → Custom Views action.

CRITICAL_FAILURE_MODES:
- **`getComponent(api_name)` requires the component's API name verbatim** — passing the display label or a typo returns nothing. Source's literal `"list-custom-view"` and `"record-create-wizard"` are dash-separated lowercase tokens. (label-vs-api-name)
- **`transitionTo(api_name)` requires the screen's API name, not its display title** — Wizard screens have separate display title and API name in Setup; using the title silently no-ops. (label-vs-api-name)
- **`setValue` on `list-custom-view` requires the Custom View id (numeric String)**, not its name — source example passes `"4312588000000087501"`, not the view's title. (label-vs-api-name)
- **`setOptions` replaces the option list with the provided Array** — partial-option patching drops omitted options.
- **`setVisibility(false)` on a required wizard component does not bypass mandatory validation** — hiding a component that the layout / wizard step marks required leaves the form unsubmittable. (layout-binding)
- **`transitionTo` fires the wizard's transition pipeline** — any `onChange` / before-transition handlers on the target screen run; calling `transitionTo` inside such a handler for the same screen risks unbounded recursion. (recursion)

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `setValue` | List, Detail | Detail, List | — |
| `getValue` | List, Detail | Detail, List | — |
| `setVisibility` | List | List | — |
| `getOptions` | List | List | — |
| `setOptions` | List | List | — |
| `transitionTo` | — | — | Create/Edit |
