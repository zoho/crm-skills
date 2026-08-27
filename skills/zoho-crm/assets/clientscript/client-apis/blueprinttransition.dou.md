FILE_PURPOSE: Read when reading or programmatically firing a Blueprint transition via the `BlueprintTransition` object returned by `ZDK.Page.getBlueprintTransitions()` / `getBlueprintTransitionByID(id)`.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/BlueprintTransition
TRIGGER_KEYWORDS: BlueprintTransition, getId, getName, initiate, blueprint, transition, Detail

TECHNICAL_CONSTRAINTS:
- Obtained via `ZDK.Page.getBlueprintTransitions()` (returns an array) or `ZDK.Page.getBlueprintTransitionByID(id)` (returns one).
- **`initiate()` programmatically triggers the transition** — equivalent to clicking the transition button in the Blueprint UI. Source example: `transObj[0].initiate()`.
- **`getId()` returns String** (source output example: `'11021234562'`).
- **`getName()` returns String** — the transition's **API name** (e.g. `'Convert_Lead'`), not the display label.
- No `before` / `after` hook accessors on the transition object — listener hookup happens via Detail-Standard event-dictionary `beforeTransition` / `afterTransition` events.

REQUIRED_PARAMETERS:
- `getId() → String` — no args.
- `getName() → String` — no args.
- `initiate()` — no args. Fires the transition.

UI_ONLY_ACTIONS:
- Blueprint authoring (states, transitions, before/during/after sections): `Setup → Automation → Blueprint → +Create Blueprint`. Note: No API equivalent — UI-only.
- Bind a Client Script to a Blueprint transition lifecycle: `Setup → Developer Hub → Client Script → Page = Detail Page → Event = beforeTransition / afterTransition`. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- **`initiate()` fires the transition synchronously from the user's perspective** — any `beforeTransition` interceptor listener (from event-dictionary Detail surfaces) can still `return false` and cancel. (interceptor-stack)
- **`initiate()` does not prompt the user for any "during" form fields** — if the transition has required during-fields, the standard UI prompt is bypassed and the transition may fail server-side.
- **`getName()` returns the transition's API name** (e.g. `Convert_Lead`), not the display label — switch-case on the display label fails. (label-vs-api-name)
- **Transition handle goes stale after `$Client.refresh()` / blueprint state change** — refetch via `ZDK.Page.getBlueprintTransitions()` after state changes.
- **No `cancel()` / `revert()` on BlueprintTransition** — only `initiate`. Reverting state requires server-side action.
- **`getBlueprintTransitionByID` parameter ambiguity** — `Page` doc signature shows `()` but example passes a String ID. 
- **Detail Canvas vs Standard event dictionaries differ on Blueprint hooks** — Detail Canvas exposes `beforeTransition`; legacy mobile matrix references `afterTransition` only on Standard. Cross-surface scripts diverge. (cross-surface-event-availability)

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `getId` | Detail | Detail | — |
| `getName` | Detail | Detail | — |
| `initiate` | Detail | Detail | — |
