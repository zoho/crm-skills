FILE_PURPOSE: Read when manipulating an individual Canvas UI element (text / image / tab / related-list / generic) obtained via `ZDK.UI.getElementByID(id)` — toggle visibility, add / remove tooltip, apply CSS, freeze, set read-only, set text content, set image, or activate a tab.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/UIElement
TRIGGER_KEYWORDS: ZDK.UI.getElementByID, UIElement.setVisibility, UIElement.addToolTip, UIElement.removeToolTip, UIElement.addStyle, UIElement.freeze, UIElement.setReadOnly, UIElement.setContent, UIElement.setImage, UIElement.setActive

TECHNICAL_CONSTRAINTS:
- UIElement instances are obtained via `ZDK.UI.getElementByID(id)` (see [ui.dou.md](./ui.dou.md)) where `id` is the Canvas-element id assigned in Canvas Builder.
- `setVisibility()` — source signature shows no documented param, but contextually (sibling pattern `setVisibility(true|false)`) takes a Boolean. Source example passes `true`.
- `addToolTip(config)` — `config: Object`. Source example key: `text: String` (tooltip text). Source does not enumerate other config keys.
- `removeToolTip()` — no params; removes the tooltip.
- `addStyle(config)` — `config: Object` keyed by CSS property name (kebab-case **and** camelCase mixed in source example: `'background-color': 'red'`, `color: 'white'`, `'border-radius': '40px'`). Values are CSS-property strings.
- `freeze(value)` — `value: Boolean` (`true` | `false`) — freezes the element.
- `setReadOnly(value)` — `value: Boolean` — "Removes write actions from the given related list" (source verbatim — read-only applies to related-list elements).
- `setContent(value)` — `value: string` — sets text content. **Text elements only** (source: "Set text content for the text element").
- `setImage(value)` — `value: object` — sets the image. Source documents two object shapes: `{ type: "url", url: "https://..." }` and `{ type: "userId", userId: "111222333444555" }`. **Image elements only** (source: "Set image for the image element").
- `setActive()` — no params — sets the active tab in a container. **Tab elements only** (source: "Set active tab in a container").

REQUIRED_PARAMETERS:
- `setVisibility(value)` — `value: Boolean` (inferred from example).
- `addToolTip(config)` — `config: { text: String }`.
- `removeToolTip()` — no params.
- `addStyle(config)` — `config: Object` of CSS-property → CSS-value pairs.
- `freeze(value)` — `value: Boolean`.
- `setReadOnly(value)` — `value: Boolean` — related-list elements only.
- `setContent(value)` — `value: string` — text elements only.
- `setImage(value)` — `value: { type: "url", url: String } | { type: "userId", userId: String }` — image elements only.
- `setActive()` — no params — tab elements only.

UI_ONLY_ACTIONS:
- Defining the Canvas element itself (its element id, type, default styling, position) is a Setup → Customization → Canvas → <View> action. The UIElement API mutates the rendered element by id but does not create / register it.

CRITICAL_FAILURE_MODES:
- **`getElementByID(id)` requires the Canvas-element id verbatim** — Canvas Builder ids are user-assigned strings (source examples: `'myElem'`, `'txt1'`, `'tab1'`); a typo returns nothing. (label-vs-api-name)
- **`setContent` on a non-text element silently no-ops** — source restricts to text elements; passing the id of an image / tab / generic element returns no error but does not update content.
- **`setImage` on a non-image element silently no-ops** — same pattern.
- **`setActive()` on a non-tab element silently no-ops** — same pattern.
- **`setReadOnly` is documented only for related-list elements** — calling it on a non-related-list UIElement has undocumented behaviour.
- **`setImage({type:"userId", userId:"..."})` requires a CRM user id (zuid-style)** — passing a record id fails to resolve the user avatar. (label-vs-api-name)
- **`addStyle` config keys mix kebab-case and camelCase in source** — `'background-color'` and `'border-radius'` are quoted (kebab-case) while `color` is unquoted (single token). Stick to the CSS-property kebab-case form for multi-word properties.
- **`freeze(true)` does not remove the element from the tab order** — kept frozen but still focusable; combine with `setVisibility(false)` for full removal from interaction.
- **Element state is not persisted** — `addStyle`, `freeze`, `setVisibility`, `setContent` etc. apply to the live DOM only; a re-render reverts to the Canvas-defined state.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `setVisibility` | — | Detail | Create/Edit |
| `addToolTip` | — | Detail | — |
| `removeToolTip` | — | Detail | — |
| `addStyle` | — | Detail | — |
| `freeze` | — | Detail | — |
| `setReadOnly` | — | Detail | — |
| `setContent` | — | Detail | Create/Edit |
| `setImage` | — | Detail | — |
| `setActive` | — | Detail | — |
