FILE_PURPOSE: Read when advancing a Blueprint transition or posting Wizard form data from a Widget via `ZOHO.CRM.BLUEPRINT.proceed` and `ZOHO.CRM.WIZARD.post`.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_BLUEPRINT, https://www.zohocrm.dev/explore/widgets/v1.5/ZOHO_CRM_WIZARD
TRIGGER_KEYWORDS: ZOHO.CRM.BLUEPRINT, BLUEPRINT.proceed, ZOHO.CRM.WIZARD, WIZARD.post, blueprint transition, transition_id, wizard widget

TECHNICAL_CONSTRAINTS:
- Two state-flow surfaces — `BLUEPRINT.proceed(data)` advances a Blueprint transition; `WIZARD.post(record_data)` writes field values into the active Wizard form.
- `BLUEPRINT.proceed` returns a Promise resolved with the transition success / failure envelope; the call body mirrors the v2 Blueprint API contract.
- `BLUEPRINT.proceed` `data` requires `Entity` (module API name), `RecordID`, and a `blueprint_transition` object with `transition_id` plus any `data` field values keyed by API name.
- `WIZARD.post` returns a Promise that resolves when the field values are committed to the parent Wizard's record buffer; the resolved value carries no payload — await it for write-acknowledgement, not for data.
- `WIZARD.post` `record_data` keys must be field **API names** (e.g. `Last_Name`, not `Last Name`); values are scalar / array per field type.
- Blueprint surface respects the host record's currently active Blueprint state — `transition_id` must be valid for the record's current state, otherwise the call rejects.
- Wizard surface is only meaningful when the Widget is hosted as a Wizard Widget step (parent-skill Routing Table → [widgets-usage.dou.md](../widgets-usage.dou.md)); calling it from other locations is a no-op.
- See sibling [widgets-jssdk-events.dou.md](./widgets-jssdk-events.dou.md) `ContextUpdate` event — that event signals the Wizard form changed; `WIZARD.post` is the inverse write path.

REQUIRED_PARAMETERS:
- `BLUEPRINT.proceed({ Entity, RecordID, blueprint_transition: { transition_id, data?: Record<string, any> } })`.
- `WIZARD.post(record_data: Record<string, any>)` — keys are field API names.

UI_ONLY_ACTIONS:
- Author / edit a Blueprint and harvest `transition_id` values: `Setup → Process Management → Blueprint → {blueprint} → Transitions`. Note: `transition_id` is exposed in the UI per transition — capture from there or via the Blueprint metadata API.
- Author / edit a Wizard and assign a Widget as a step: `Setup → Customization → Wizards → {wizard} → Steps`. Note: a Wizard step hosts exactly one Widget — `WIZARD.post` writes into that wizard's record buffer.

CRITICAL_FAILURE_MODES:
- `BLUEPRINT.proceed` `Entity` is module display label (`"Lead"`) instead of API name (`Leads`): API rejects with `INVALID_MODULE` — `label-vs-api-name`.
- `transition_id` value hardcoded against a Blueprint that admins re-versioned: IDs change per Blueprint version — fetch via [widgets-jssdk-api.dou.md](./widgets-jssdk-api.dou.md) `getBluePrint` at runtime instead.
- `blueprint_transition.data` keys use field display labels: transition succeeds but the data fields remain unset — `label-vs-api-name`.
- `WIZARD.post` called from a Widget not hosted on a Wizard step: no-op, no error — feature-detect by checking the Widget's host context via `PageLoad`.
- `WIZARD.post` payload keys mix camelCase / snake_case inconsistently against the module's field API names: mismatched keys silently dropped — match each field's exact API name from [widgets-jssdk-meta.dou.md](./widgets-jssdk-meta.dou.md) `getFields`.
- Multiple `WIZARD.post` calls fired rapidly from a `ContextUpdate` handler: race condition on the wizard buffer can drop intermediate writes — debounce.
- `BLUEPRINT.proceed` invoked while the record's current state has unresolved mandatory transition fields: rejects with `MANDATORY_NOT_FOUND` — pre-validate against Blueprint metadata.
- `BLUEPRINT.proceed` invoked in a tight retry loop after rejection: each call consumes Blueprint audit history — backoff exponentially on failure.
- `WIZARD.post` called after the Wizard has navigated past the step that owns the field: writes silently discarded — gate by current step from the `PageLoad` payload.
- `BLUEPRINT.proceed` success treated as record-updated event for downstream code: transition update fires its own workflows / approvals — coordinate trigger semantics (see parent-skill Top-5 Gotcha #3).
- `WIZARD.post` value type mismatch (e.g. picklist value not in the field's allowed set): silently dropped on the server — validate against `getFields` `pick_list_values` first.
- `transition_id` reused across record types: each Blueprint is module-scoped — using a Leads transition on a Deals record rejects with `INVALID_DATA`.
- `BLUEPRINT.proceed` consumed without inspecting the resolved envelope's status: failure transitions report success at the Promise layer but contain error details inside the body — inspect both.
- `WIZARD.post` value supplied as `null` to clear a field: server interprets `null` and `undefined` differently — use the documented sentinel for the field's data type.
- `WIZARD.post` invoked from inside a `Notify` handler: Notify-spawned context is not the Wizard's record buffer — the call no-ops.
- `BLUEPRINT.proceed` chained with another `proceed` immediately on resolution: second transition can race against the server-side Blueprint state machine — reload record state between transitions.
- Multiple Wizard widgets posting overlapping field sets: last-write-wins on the wizard buffer — partition writes by step.
- `blueprint_transition.data` containing a subform / multiselect field as a comma-string instead of an array: server rejects — use array shape.
- `WIZARD.post` caller proceeds with a follow-up read before the returned Promise resolves: the wizard buffer write is not yet visible — always `await WIZARD.post(...)` before consuming the buffer state.
- `BLUEPRINT.proceed` invoked against a record whose Blueprint was paused by admins: returns blueprint-inactive error — check Blueprint status before retry.
- Caching the result of [widgets-jssdk-api.dou.md](./widgets-jssdk-api.dou.md) `getBluePrint` across versions: admin re-publish invalidates `transition_id` values — re-fetch on every Widget mount.
- `WIZARD.post` to a field that is not present in the Wizard's step layout: silently dropped — verify field presence against the active step.
- Triggering `BLUEPRINT.proceed` from a `ContextUpdate` event: every keystroke advances Blueprint state — only call it on explicit user submit.
- Transition `data` payload includes audit-only fields the Blueprint marks read-only: server rejects — supply only transition-input fields.
- Same `transition_id` invoked twice as a fast double-click: first advances state, second rejects — disable the trigger button between submissions.
- Wizard widget reads `record_data` back from `getRecord` immediately after `WIZARD.post`: data is in the wizard buffer, not yet on the record — do not round-trip via CRM API mid-wizard.
- `BLUEPRINT.proceed` resolved branch interpreted as the transition's downstream workflow has completed: workflows run asynchronously after transition success — do not assume side effects landed.
