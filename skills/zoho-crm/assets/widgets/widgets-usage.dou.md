FILE_PURPOSE: Read when hosting, registering, associating, downloading, or deleting a CRM Widget through Developer Hub Setup — and when picking among the eight Widget locations.
SOURCE_DOC: widgets/usage.md
TRIGGER_KEYWORDS: Internal Hosting, External Hosting, Index URL, Hosting = Zoho, Hosting = External, 25MB, Not Installed view, Blueprint transition, Web tab

TECHNICAL_CONSTRAINTS:
- Hosting modes — `Zoho` (Internal, uploaded `.zip` from `zet pack`) and `External` (developer-hosted HTTPS URL); both wired through `Setup → Developer Hub → Widgets`.
- Internal-hosting upload hard cap — `.zip` ≤ 25 MB; larger archives are rejected.
- Supported Widget locations (8): Dashboard, Web tab, Custom Button, Custom Related List, Wizard, Signal, Settings, Blueprint.
- Each saved Widget is bound to its host component (button / related list / web tab / wizard / blueprint transition / signal / dashboard / setting); Blueprint transitions accept exactly one Widget per transition.
- Download action exists only for Internal-hosted Widgets — External-hosted source is not stored by CRM.
- Bulk-delete affordance exists only in the `Not Installed` view of the Widgets list.
- Extension-installed Widgets cannot be deleted from the Widgets page directly — they are removed automatically when the parent extension is uninstalled from Marketplace.
- Edition cap, sandbox-scoping, and Developer Permissions prerequisite — see [widgets-overview.dou.md](./widgets-overview.dou.md).

REQUIRED_PARAMETERS:
- Widget creation fields (pop-up):
    · Name — string, mandatory.
    · Description — string, optional (metadata only; ignored at runtime).
    · Widget Type — one of {Dashboard, Web Tab, Custom Button, Custom Related List, Wizard, Signal, Settings, Blueprint}.
    · Hosting — `Zoho` | `External`.
    · For `Zoho`: upload `.zip` (≤ 25 MB) + Index URL (relative path to the entry HTML inside the archive).
    · For `External`: enter the externally hosted HTTPS URL.
    · Mobile Compatibility — optional toggle, applies to 5 of the 8 types (see [widgets-mobile-compatibility.dou.md](./widgets-mobile-compatibility.dou.md)).
- No REST API documented for create / update / delete of Widgets — every field is set in the Setup UI. **Exception**: creating and uploading a Widget is also supported via the **ZDK CLI** in **sandbox environments only**; ZDK CLI is not supported for production environments.
- Runtime invocation contract — Widget receives CRM context via `PageLoad` (see [widgets-jssdk-events.dou.md](./jssdk/widgets-jssdk-events.dou.md)).
- Association step — after Save, open the host component's Setup screen and select the saved Widget from its Widget picker.

UI_ONLY_ACTIONS:
- Add a Widget: `Setup → Developer Hub → Widgets → Create your First Widget → fill Name + Description + Widget Type + Hosting → (Internal: Upload .zip + Index URL · External: HTTPS URL) → Save`. Note: UI action in **production**; also supported via **ZDK CLI in sandbox** — ZDK CLI is not available for production environments.
- Download an Internal-hosted Widget: `Setup → Developer Hub → Widgets → hover the widget → settings icon → Download`. Note: No API equivalent; absent for External-hosted Widgets.
- Delete a single Widget: `Setup → Developer Hub → Widgets → hover the widget → settings icon → Delete`. Note: No API equivalent — UI-only.
- Bulk-delete Widgets: `Setup → Developer Hub → Widgets → switch to Not Installed view → tick checkboxes → click Delete at top`. Note: No API equivalent — UI-only.
- Associate a Widget with a location: open the host component (Custom Button / Related List / Web Tab / Wizard / Signal / Dashboard / Setting / Blueprint transition) and pick the saved Widget from its Widget selector. Note: No API equivalent — UI-only.
- Remove an extension-installed Widget: `Setup → Marketplace → uninstall the parent extension`. Note: No direct delete on the Widgets page.

CRITICAL_FAILURE_MODES:
- Delete attempted while the Widget is still associated with a component: deletion is blocked or breaks the host surface — remove every association first.
- Internal-hosting `.zip` > 25 MB: upload rejected — reduce assets or switch to External hosting.
- Index URL entered as an absolute URL instead of a path relative to the `.zip` root, or pointing at a path not present in the archive: Widget renders blank in CRM with no actionable error in Setup.
- External-hosting URL served over HTTP, redirected, self-signed TLS, or returning non-200: browser blocks the iframe; use a publicly trusted HTTPS endpoint.
- More than one Widget assigned to a single Blueprint transition: unsupported — exactly one Widget per transition.
- Bulk-delete attempted from a view other than `Not Installed`: the Delete affordance is hidden — switch view first.
- Hosting mode toggled (`External` ↔ `Zoho`) on an existing Widget without re-supplying the source: Widget continues referencing the previous artefact — re-upload / re-point.
- Mobile-incompatible Widget associated with a mobile-visible component without checking the indicator icon: mobile users see a UX gap — confirm flag (see [widgets-mobile-compatibility.dou.md](./widgets-mobile-compatibility.dou.md)).
- Internal `.zip` re-uploaded but Index URL not re-checked after entry-file rename: Widget renders blank — re-validate Index URL on every upload.
- Widget association added to a layout that the end-user's profile does not see: the placement is invisible to that profile — audit layout assignments alongside Developer Permissions (see [widgets-overview.dou.md](./widgets-overview.dou.md)).
- External URL behind a CORS or X-Frame-Options policy that disallows framing: iframe is blocked by the browser — host must permit framing by the CRM origin.
- Widget Type changed after Save: existing associations remain pointed at the prior Type's host surfaces and behave unpredictably — delete and re-create instead of editing Type in place.
- Index URL containing a query string or hash fragment: ignored or stripped by the Internal-hosting loader — keep Index URL as a plain relative path.
- Internal-hosted Widget Download used as a backup strategy: the export does not include CRM-side metadata (associations, Mobile Compatibility flag) — maintain the source project in version control instead.
