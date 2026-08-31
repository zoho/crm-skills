FILE_PURPOSE: Read when toggling Mobile Compatibility on a Widget so it renders in the Zoho CRM mobile app for the five supported Widget types.
SOURCE_DOC: widgets/mobile-compatibility.md
TRIGGER_KEYWORDS: Mobile Compatibility, Related List, Web tab, Blueprint, Wizard, association popup, extension widget, mobile app

TECHNICAL_CONSTRAINTS:
- Mobile Compatibility is a per-Widget-definition toggle at the bottom of the Widget create / edit pop-up; off by default.
- Supported Widget types (5 only): Related List, Web tab, Button, Blueprint, Wizard. Dashboard / Signal / Settings do not expose the toggle and render desktop-only.
- Toggle flips a CRM-side flag only — bundle assets are unchanged; the developer is responsible for mobile-fit CSS / viewport / touch-target work.
- Mobile rendering reuses the same iframe + JS SDK runtime as desktop — `ZOHO.embeddedApp.*` and `ZOHO.CRM.*` surfaces remain available (see [widgets-jssdk-events.dou.md](./jssdk/widgets-jssdk-events.dou.md)).
- Extension-based Widgets are excluded from mobile-compat support even when their Widget Type is in the supported list.
- Decision is per-Widget-definition — a single definition cannot be marked compatible for one host component and incompatible for another; split into two Widgets when divergent mobile UX is needed.
- Flag is read at Widget-association time — flipping later requires re-saving every existing association to take effect.
- Mobile-incompatible Widgets are marked with an icon in the component's Widget association popup.
- Hosting mode (Internal `.zip` / External URL) is shared with desktop — there is no separate mobile artefact (see [widgets-usage.dou.md](./widgets-usage.dou.md)).
- Edition cap, profile gating, and sandbox-scoping are inherited from [widgets-overview.dou.md](./widgets-overview.dou.md).
- Toggle state is preserved across Widget edits as long as Widget Type stays in the supported set; changing type to Dashboard / Signal / Settings clears the toggle silently.
- Mobile-compat decision affects only whether the Widget is offered for selection in the mobile app association picker; once offered, rendering quality is bounded by the Widget developer's CSS.

REQUIRED_PARAMETERS:
- Toggle — `Mobile Compatibility` checkbox in the Widget create / edit pop-up; available only when Widget Type ∈ {Related List, Web tab, Button, Blueprint, Wizard}.
- No API documented to flip mobile compatibility — UI-only.
- Adapt the Widget UI (viewport meta, touch targets, layout breakpoints) and verify on a representative device via the CRM mobile app before declaring the toggle production-ready.

UI_ONLY_ACTIONS:
- Set on a new Widget: `Setup → Developer Hub → Widgets → Create your First Widget → fill fields → enable Mobile Compatibility → Save`. Note: No API equivalent — UI-only.
- Toggle on an existing Widget: `Setup → Developer Hub → Widgets → {Widget} → Edit → enable / clear Mobile Compatibility → Save → re-save each existing association`. Note: No API equivalent — UI-only.
- Identify mobile-incompatible Widgets during association: an icon flags them in the host component's Widget association popup. Note: UI-only indicator.

CRITICAL_FAILURE_MODES:
- Toggle left disabled on a Related List / Web tab / Button / Blueprint / Wizard Widget: Widget does not appear in the CRM mobile app — no error surfaces in the desktop UI. (silent no-fire)
- Toggle expected on Dashboard / Signal / Settings: option not exposed — those types are desktop-only regardless.
- Extension-based Widget assumed mobile-compatible because its type is supported: mobile-compat does not apply to extension Widgets.
- Toggle flipped via Edit but existing associations not re-saved: mobile rendering remains disabled until each association is re-saved.
- Bundle re-upload skipped after viewport / CSS fixes: end-users still see the pre-fix bundle — re-upload `.zip` (Internal) or redeploy URL (External).
- Runtime branching driven by user-agent sniffing instead of `PageLoad` payload + viewport queries: unreliable inside CRM mobile WebViews.
- Display labels referenced inside mobile-only code branches (e.g. layout name string compares): same `label-vs-api-name` hazard as desktop (see [widgets-jssdk-events.dou.md](./jssdk/widgets-jssdk-events.dou.md)).
- Desktop-only browser APIs (drag-and-drop file pickers, hover-only menus) used inside a mobile-compat Widget: renders without function on touch devices — feature-detect at runtime.
- Bundle size acceptable on desktop but stalling on mobile networks: profile and trim — the toggle does not implicitly optimize transport.
- Widget Type changed from a supported value to Dashboard / Signal / Settings: mobile-compat flag is cleared silently — audit after type changes.
- Mobile-app version older than the CRM-supported minimum: even a mobile-compat Widget fails to render — confirm the mobile-app version against the CRM-supported list.
- New host-component association created after the Widget was made mobile-compatible but flag forgotten on later type change: the association silently loses mobile rendering — re-audit associations after any type change.
- `PageLoad` payload not branched on for mobile-specific layout: desktop layout renders on mobile and looks broken — inherit viewport detection from the payload + CSS media queries.
- Mobile-compat Widget association added to a Wizard step gated by a desktop-only field: the step is unreachable on mobile — keep step gating consistent across surfaces.
- `ZOHO.CRM.UI.*` Popup / Detail surfaces invoked from mobile: rendering uses the mobile-app shell — confirm the surface is supported on the active mobile-app version before relying on it.
- Mobile-compat Widget association added to a Custom Button placement gated by a desktop-only ClientScript: the button hides on mobile — audit the ClientScript binding alongside.
- Mobile-compat flag re-enabled on a previously cleared Widget after a Type revert: existing associations need re-saving even though the toggle is on.
- Mobile-compat audit performed only at deploy time: source CSS regressions later silently reduce mobile usability — add a regression check to every Widget pack.
- Mobile-compat toggle saved while the host association browser tab is stale: subsequent edits in the stale tab overwrite the flag back to off — refresh before further edits.
- Mobile-compat coverage assumed for native-mobile push notifications opened from outside the CRM app: the iframe context is not guaranteed — design fallbacks for cold opens.
- Mobile-compat checked in vendor `iframe` test harnesses only: real device chrome (touch / soft keyboard / safe-area insets) still ships bugs — test on physical devices before release.
