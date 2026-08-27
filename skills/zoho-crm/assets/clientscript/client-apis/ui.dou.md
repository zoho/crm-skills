FILE_PURPOSE: Read when using `ZDK.UI.*` to freeze the page, scroll to a Canvas element, highlight an element, or fetch a UIElement handle on Canvas surfaces.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/UI
TRIGGER_KEYWORDS: ZDK.UI, freeze, scrollTo, highlight, getElementByID, UIElement, Canvas, element_id

TECHNICAL_CONSTRAINTS:
- `ZDK.UI` operates on **Canvas-page element IDs** — `scrollTo`, `highlight`, `getElementByID` all take an `element_id` String identifying a Canvas page element (the ID assigned to the element in Canvas Builder).
- `freeze(value)` is the only non-Canvas method — it freezes the entire page UI regardless of layout type.
- `highlight(config)` signature in source: `highlight(config)` but the example call is `ZDK.UI.highlight('div1', { time: 1000 })` — passing an element ID String first and a config object second.
- `getElementByID` returns a `UIElement` object (see separate UIElement node — not in this batch).

REQUIRED_PARAMETERS:
- `freeze(value)` — `value` Boolean. `true` = freeze UI; `false` = unfreeze. No return.
- `scrollTo(element_id)` — `element_id` String (ID of a Canvas-page element). No return.
- `highlight(config)` — source signature shows single `config` Object arg; example call passes element_id String + config Object. `config.time` = duration in ms (per example, `1000`).
- `getElementByID(element_id) → UIElement` — `element_id` String.

UI_ONLY_ACTIONS:
- Element-ID assignment for `scrollTo` / `highlight` / `getElementByID` happens in `Setup → Customization → Canvas → <canvas> → element → properties (ID field)`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **`element_id` must match an ID set in Canvas Builder** — calling `getElementByID('section1')` against a Standard layout (no Canvas) silently returns nothing. (canvas-only)
- **`freeze(true)` without a paired `freeze(false)` leaves the page locked** — always pair, even in error paths. (freeze-leak)
- **`scrollTo` / `highlight` on a non-Canvas page no-op silently** — there is no error event. (canvas-only-noop)
- **`highlight` signature ambiguity** — see flag above; calling with the wrong arg shape may silently no-op.
- **No `unhighlight` documented** — highlight clears after `config.time` ms; programmatic cancellation not exposed.
- **No keyboard / focus / accessibility hooks** documented on `ZDK.UI` — focus management requires Web-platform APIs and is not surfaced by Client Script.

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `freeze` | all page types | all page types | all page types |
| `scrollTo` | — | Detail | — |
| `highlight` | — | Detail | — |
| `getElementByID` | — | Detail | Create/Edit |
