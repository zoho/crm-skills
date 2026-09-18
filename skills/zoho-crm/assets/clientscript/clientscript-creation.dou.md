FILE_PURPOSE: Read when creating a Client Script via Setup or the in-record sidebar — confirming required pop-up fields, Event Details split, IDE handoff, and post-save activation toggle.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/creation.html
TRIGGER_KEYWORDS: New Script, Developer Hub, Client Script setup page, Category Module, Category Commands, onLoad, onChange, onSave, ZDK Library

TECHNICAL_CONSTRAINTS:
- Two authoring entry points — Setup page (`Setup → Developer Hub → Client Script → +New Script`) and the right-most Client Script panel on any create / clone / edit record page.
- Module list in the Create Script pop-up: Leads, Contacts, Accounts, Deals, Products, Quotes, Sales Orders, Purchase Orders, Invoices, Campaigns, Vendors, Price Books, Cases, Solutions, Custom Module.
- Layout selector — Standard or any custom layout; one Client Script binds to one selected layout.
- Page selector for in-Setup creation supports: Create Page, Clone Page, Edit Page.
- Event Details "Type" dropdown — available options depend on the selected Page; see [clientscript-event-type-matrix.dou.md](./clientscript-event-type-matrix.dou.md) for the full per-page Type/Event/selector matrix (this replaces the outdated "page | field only" claim previously here). Type does **not** apply to Category = Commands scripts at all — no Page/Type/Event fields exist for Commands (see [clientscript-commands.dou.md](./clientscript-commands.dou.md)). Wizard Create/Edit pages require choosing which Wizard in the Page Details section (`Page = Create/Edit Page (Wizard) → Wizard = <name>`) — this happens *before* Type is even shown, analogous to Layout, not a Type-dependent field. Subform Event has no creation-time subform picker — the target subform is chosen in code via `ZDK.Page.getSubform(<api_name>)`.
- IDE handoff — clicking Next opens the Client Script IDE; the script is not persisted until Save and Close.
- Post-save state — Client Script setup page lists Name, size, last-modified user, and status (enabled / disabled); enable via the toggle.
- ZDK Library — dot-notation SDK exposed in the IDE Information panel; click the help icon in Library to open ZDK docs.

REQUIRED_PARAMETERS:
- Create Script pop-up fields (Setup flow): Name, Description, Category (Module | Commands), Page, Module, Layout, (Wizard — only when Page = Create/Edit Page (Wizard), chosen here in Page Details before Type is shown), then Event Details → Type (see [clientscript-event-type-matrix.dou.md](./clientscript-event-type-matrix.dou.md) for the complete per-Page list of values) → Event, plus Field (only when Type = Field Event — the sole genuine post-Type Event-Details selector, confirmed via this source doc's literal section-ordering).
- Create Script pop-up fields (in-record flow): page details (Page, Module, Layout) pre-populated by the system; caller supplies Name, Description, Event Details, then Next → IDE → Save and Close.
- Activation — toggle the per-script status from the Client Script setup list to enable the script after Save and Close.

UI_ONLY_ACTIONS:
- Create via Setup: `Setup → Developer Hub → Client Script → +New Script → Name + Description → Category + Page + Module + Layout (+ Wizard, if Page = Wizard) → Event Details: Type + Event (+ Field, if Type = Field Event) → Next → IDE → Save and Close → toggle Enable`. Note: No API equivalent — UI-only.
- Create via record page: open the target Create / Clone / Edit record page → right-most `Client Script` panel → `Add Script` → fill Name / Description / Event Details → Next → IDE → Save and Close. Note: No API equivalent — UI-only.
- Edit or delete a script: `Setup → Developer Hub → Client Script → {script} → Edit | Delete`. Note: No API equivalent — UI-only.
- Open ZDK docs: in the IDE Information panel, click the help icon inside the Library section. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- Layout selected at creation time fixes the script binding — selecting the wrong layout silently no-fires on records using a different layout. (layout-binding) See [clientscript-overview.dou.md](./clientscript-overview.dou.md) for the per-layout-script rule.
- Save and Close persists the script in the setup list with an enable/disable status toggle; use the toggle to enable the script before it will execute (source: "You can enable a script by sliding the toggle button.").
- Category mismatch — choosing Module for a command-style script (or Commands for a module-bound script) routes the script away from its intended trigger surface. (category-binding)
- In-record creation pre-populates Page / Module / Layout from the current record context; editing those fields requires returning to the Setup-page edit flow.
- Field Event only supports `onChange` (per the pop-up); attempting `onLoad` / `onSave` as a field event is not offered — model the script as a Page Event instead.
