FILE_PURPOSE: Read when reading the current page's CRM context inside a Client Script — current record, record id, layout id, module, parent-record id (clone), custom navigation data, or page name — via the `$Page` utility.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/$Page
TRIGGER_KEYWORDS: $Page.record, $Page.record_id, $Page.layout_id, $Page.module, $Page.parent_record_id, $Page.navigation_data, $Page.name, record_detail, record_create, record_clone, record_edit, record_list

TECHNICAL_CONSTRAINTS:
- `$Page` is a global utility namespace; **every example accesses properties bare** (no parens) — e.g. `$Page.record;`, `$Page.record_id;`, `$Page.module;`. Source signatures notate them as `(){Object}` / `(){String}` (method form).
- `$Page.record` returns the **current record as stored on the server** (source verbatim: "get current record information stored in the server"). Source example output: `{ First_Name: "John", Full_Name: "John zylker", Last_Name: "zylker", ... }`. Object keys are field API names.
- `$Page.record_id` returns the current record id as String (source example: `527627200000037XXXX`). Treat as opaque.
- `$Page.layout_id` returns the current layout id as String (source example: `527627200000009XXXX`). Treat as opaque.
- `$Page.module` returns the current module's API name as String (source example: `Leads`).
- `$Page.parent_record_id` returns the parent record id **while cloning** (source verbatim: "Get the parent record ID while cloning"). Source example: `1776121000000694009`.
- `$Page.navigation_data` returns the custom `params.custom_data` payload forwarded by `ZDK.Client.navigateTo` (see [client.dou.md](./client.dou.md)). Source example: caller passes `custom_data: [{ key: "value" }]` and receiver reads `$Page.navigation_data` → `{ key: "value", ... }`. **Source returns the payload as an Object** (`{ key: "value", ... }`) even though the caller passed an Array (`[{ key: "value" }]`).
- `$Page.name` returns the **current page name** as one of the literal tokens: `'record_detail'` | `'record_create'` | `'record_clone'` | `'record_edit'` | `'record_list'` | `undefined`. Source declares the signature as `name()` with no return-type annotation.

REQUIRED_PARAMETERS:
- `$Page.record` — no invocation; returns Object keyed by field API names.
- `$Page.record_id` — no invocation; returns String.
- `$Page.layout_id` — no invocation; returns String.
- `$Page.module` — no invocation; returns String (module API name).
- `$Page.parent_record_id` — no invocation; returns String (clone scenario).
- `$Page.navigation_data` — no invocation; returns Object (mirrors `custom_data` payload from `ZDK.Client.navigateTo`).
- `$Page.name` — no invocation; returns String in `{'record_detail','record_create','record_clone','record_edit','record_list'}` or `undefined`.

UI_ONLY_ACTIONS:
- Defining the layout that `$Page.layout_id` resolves to is a Setup → Customization → Modules and Fields → <Module> → Layouts action. `$Page.layout_id` reads the active layout's id but does not switch it.

CRITICAL_FAILURE_MODES:
- **`$Page.record` is the server-side snapshot, not the live form values** — on an Edit page, user edits in the form are not reflected in `$Page.record` until save; use `ZDK.Page.getForm().getValues()` for in-flight values. (layout-binding)
- **`$Page.record_id` is empty / undefined on Create pages** — guarding on truthiness before using it as a key avoids passing `undefined` to downstream API calls.
- **`$Page.layout_id` reflects the active layout** — a script that compares `layout_id` against a hard-coded value silently misroutes when an admin clones / renames layouts; pin against the documented id and confirm in Setup.
- **`$Page.module` returns the module API name, not the display label** — string-compare against `"Leads"` works only because `Leads` happens to be both API name and label; for renamed / custom modules use the API name. (label-vs-api-name)
- **`$Page.parent_record_id` is meaningful only during Clone** — reading it on a non-clone page returns an undocumented value (likely `undefined` / empty). Always branch on `$Page.name === 'record_clone'` first.
- **`$Page.navigation_data` is `undefined` when the page was not reached via `ZDK.Client.navigateTo`** — direct navigation (URL paste, bookmark, in-app link) leaves it empty. Branch defensively.
- **`$Page.name === undefined`** is a documented value (source enumerates `undefined` in the page-name set) — code that switches on the 5 known names without an `undefined` / default branch silently no-ops on unsupported page types (Wizard, Canvas list, etc.).
- **Property-vs-method ambiguity** — if `$Page.record` is a getter that re-fetches from the server on every read, repeated access in a loop incurs cost; cache the value.
