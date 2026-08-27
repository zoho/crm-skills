FILE_PURPOSE: Read when picking `ZDK.Page.*` accessors to reach Fields, Subforms, Components, Form, List, Buttons, Links, Blueprint Transitions, or Tags on the current Client-Script page.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Page
TRIGGER_KEYWORDS: ZDK.Page, getField, getSubform, getComponent, getForm, getList, getButton, getBlueprintTransitions, addTag, removeTag

TECHNICAL_CONSTRAINTS:
- `ZDK.Page` is the page-scoped root accessor on Client Script — every method returns either a single domain object or an array of them; no method on `ZDK.Page` itself takes a write payload (writes happen on the returned objects).
- Component `name` is an enum (not a free string). Source-enumerated names: `list-custom-view` (custom view drop down on list view), `list-view-type` (view-select drop down on list view), `canvas-list-view` (canvas-list-view drop down on canvas listview page), `record-create-wizard` (wizard component on create / edit / draft page), `notes-editor` (notes component on detail / canvas-detail / list page).
- `addTag` / `removeTag` accept `<repeatable>` String varargs — single call: `addTag('tagname')`; multi-tag: `addTag('tagname1', 'tagname2', 'tagname3')`.
- `getTags()` returns array of objects shaped `{ name: <tag> }` — not a flat string array.
- **`getButtonByID` is the only method without a "Supported Pages" subsection in source** — implies universal availability (button IDs resolve on any page that hosts the button).

REQUIRED_PARAMETERS:
- `getField(api_name) → Field` — `api_name` is the field API name (not display label). Example: `ZDK.Page.getField('Last_Name')`.
- `getFields() → Field[]` — no args; returns all fields on the page.
- `getSubform(api_name) → Subform` — `api_name` is the subform API name. Example: `ZDK.Page.getSubform('CFSubform')`.
- `getComponent(name) → Component` — `name` is one of the 5 source-enumerated component names.
- `getComponents() → array` — no args; returns all components.
- `getForm() → Form` — no args; returns the page Form object.
- `getList() → List` — no args; returns the List-View object (list-page surfaces).
- `getButtonByID(id) → Button` — `id` is a String button ID. Example: `getButtonByID('118881188181')`.
- `getButton(api_name) → Button` — `api_name` is the button API name. Example: `getButton('record_save')` → `{ getId, getApiName, getType }`.
- `getButtons() → Button[]` — no args; returns all page buttons.
- `getLinkByID(id) → Link` — `id` is a String link ID.
- `getLinks() → Link[]` — no args.
- `getBlueprintTransitionByID(id) → BlueprintTransition` — fetch shows `id` arg in example (`'104567100090'`) though signature line displays `()`.
- `getBlueprintTransitions() → BlueprintTransition[]` — no args.
- `addTag(...tag_names)` — variadic String tag names. No return value documented.
- `removeTag(...tag_names)` — variadic String tag names. No return value documented.
- `getTags() → Array.object` — returns `[{ name }, ...]`.

UI_ONLY_ACTIONS:
- *(none in source)* — `ZDK.Page` is a script-side reader, not a UI-binding surface; binding is configured via Client Script setup (see `references/dou/clientscript/event-dictionary/` nodes).

CRITICAL_FAILURE_MODES:
- **`api_name` is the API name, not the display label** — `getField('Last_Name')` works; `getField('Last Name')` does not. (label-vs-api-name)
- **`getComponent(name)` outside the 5 source-enumerated names returns nothing useful** — silent miss on typos like `'noteseditor'` or `'wizard'`. (component-name-enum)
- **`getList()` only resolves on list-page surfaces** — calling on a Detail / Create / Edit / Quick-Create page returns nothing operational.
- **`getBlueprintTransitions()` only resolves on Detail-surface pages where Blueprint is bound** — Create / List / Quick-Create surfaces have no transitions.
- **`addTag` / `removeTag` operate on the current page record** — on Create / Edit surfaces before save, tag persistence depends on save; on Detail surfaces tags fire immediately.
- **`getButtonByID` vs `getButton(api_name)` are distinct accessors** — passing an API name to `getButtonByID` (or vice versa) silently returns nothing. (id-vs-api-name)
- **No `setTag` / `replaceTags`** — only add / remove; full-replace requires `getTags()` + diff + per-name remove + per-name add.
- **`Component` name strings are surface-coupled** — e.g. `record-create-wizard` only resolves on Create/Edit/Draft, `notes-editor` only on Detail / Canvas Detail / List. Cross-surface scripts silently miss. (component-surface-coupling)

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getField` | Detail, Create/Edit/Clone | Detail, Create/Edit/Clone | Create/Edit |
| `getFields` | Detail, Create/Edit/Clone | Detail, Create/Edit/Clone | Create/Edit |
| `getSubform` | Create/Edit/Clone | Create/Edit/Clone | Create/Edit |
| `getComponent` | List, Detail | Detail, List | Wizard |
| `getComponents` | List, Detail | Detail, List | Wizard |
| `getForm` | Detail, Create/Edit/Clone | Detail, Create/Edit/Clone | Create/Edit |
| `getList` | List | List | — |
| `getButtonByID` | all page types | all page types | all page types |
| `getButton` | all page types | all page types | all page types |
| `getButtons` | Create/Edit/Clone, Detail, List | Detail, Create/Edit/Clone, List | Wizard |
| `getLinkByID` | Detail | Detail, List | — |
| `getLinks` | Detail | Detail, List | — |
| `getBlueprintTransitionByID` | Detail | Detail | — |
| `getBlueprintTransitions` | Detail | Detail | — |
| `addTag` | Detail | Detail | — |
| `removeTag` | Detail | Detail | — |
| `getTags` | Detail | Detail | — |
