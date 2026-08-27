FILE_PURPOSE: Read when picking `ZDK.Client.*` UX primitives — toasts, alerts, confirmations, input pop-ups, mailer, navigation, popup / callout widgets, flyouts, and loaders.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Client
TRIGGER_KEYWORDS: ZDK.Client, showMessage, showAlert, showConfirmation, getInput, openMailer, navigateTo, openPopup, openCallout, showLoader

TECHNICAL_CONSTRAINTS:
- **Active-loader mutual exclusion**: *"The presence of an active loader restricts the availability of other pop-ups."* Applies to `showMessage`, `showAlert`, `showConfirmation`, `getInput`, `openMailer`, `openPopup`, `openCallout`, `showLoader`. Always pair `showLoader` with `hideLoader` before launching another pop-up.
- **`showMessage` Markdown is restricted**: source explicitly states *"Image Markdown not supported for showMessage"*. Supported tokens: Italics `_text_`, Bold `*text*`, Underline `__text__`, Strikeout `~text~`, Code `` `text` ``, Heading1 `# text`, Heading3 `### text`, Blockquote `!text`, Hyperlink `[label](url)`.
- **`showAlert` Markdown** supports the full set above **including** image (`![alt](url)`) and `\n` line breaks. Demonstrated in source example.
- **`showConfirmation` returns Boolean** — `true` on accept, `false` on reject. Awaitable.
- **`getInput` per-type max-value limits**: `text` 120 chars · `number` 50 digits · `textarea` 2000 chars · `picklist options` 2000 options × 120 chars each · `multiselectpicklist options` 2000 options × 120 chars each. Max inputs per call: **7**.
- **`getInput` output shape**: array. Single-input call returns `['value']`; multi-input returns `['val1', 'val2', ...]`; multiselect returns `[[<selected_actual_values>]]` (nested array).
- **`openPopup` / `openCallout` require Widget SDK ≥ 1.2** — source explicit.
- **`navigateTo` page enum**: `tab` (Web Tab / default list view), `record_create`, `record_edit`, `record_detail`, `record_clone`, `record_list` (List view or Canvas List view).
- **`navigateTo` target enum**: `_self` (default) or `_blank` (new tab).
- **`showLoader` template enum**: `spinner`, `vertical-bar`, `standard` (default). Source note: *"spinner and vertical bar can be used when invoking time consuming APIs"*. `message` limit 240 characters.
- **`navigateTo` for canvas record_detail / record_list requires `view: { type:'canvas', id:<canvas_id> }`** — source comments `// id is mandatory for canvas`.
- **`navigateTo` `params.custom_data`** — source example passes `custom_data: [{key:'value'}]` inside `params` for record_list navigation, separate from the 3rd `data` arg.
- **`openPopup` / `openCallout` / `createFlyout` accept position-config keys** — source `openPopup` example uses `left: '10px'` alongside `height` / `width`; full position keyset (likely `top`, `right`, `bottom`, `left`) not enumerated in the captured headings.
- **`openPopup` / `openCallout` / `createFlyout` `animation_type` enum**: `1` top, `2` right, `3` left, `4` bottom, `5` fade, `6` zoom.

REQUIRED_PARAMETERS:
- `showMessage(message, options?)` — `message` String; `options.type` ∈ `'info' | 'error' | 'warning' | 'success'` (default `'info'`).
- `showAlert(message, heading?, accept_message?)` — `accept_message` default `'Okay'`.
- `showConfirmation(message, accept_message?, reject_message?) → Boolean` — defaults `'Yes, Proceed'` / `'Cancel'`.
- `getInput(options[], heading?, accept_message?, reject_message?) → Object` — `options[].type` ∈ `'text' | 'number' | 'textarea' | 'picklist' | 'multiselectpicklist'`; `options[].label` String; `options[].default_value` String or Array (multiselect); `options[].list_options` `{ actual_value, display_value }[]`. Defaults: `heading='Heading'`, `accept_message='Okay'`, `reject_message='Cancel'`.
- `openMailer(mail_config)` — `mail_config.from` String; `to` / `cc` arrays of `{email, label}`; `subject`, `body`, `templateId` Strings.
- `navigateTo(page, params, data?, target?)` — `params.module` (API name, String) required; `params.record_id`, `params.layout_id`, `params.custom_view_id` optional Strings. `data` is custom navigation data — readable on target page via `$Page.navigation_data` (per source).
- `openPopup(config, data?) → object|string|number|boolean` — `config.api_name` (widget API name, Custom Button type); `config.type='widget'`; `config.header` (default `${widget name}`; `undefined` hides header); `close_icon` (default `true`); `close_on_escape` Boolean; `animation_type` 1–6 (default 1); plus height / width / position config. Awaits widget's `$Client.close()` payload.
- `openCallout(config, target, data?) → object|string|number|boolean` — like `openPopup` but anchors to a target component. `target` example: `{ type:'field', api_name:'State' }`. Closes on out-of-focus by default. `close_on_body_click` default `true`.
- `createFlyout(name, config?) → Flyout` — `name` String; `config` mirrors popup config keys (header, close_icon, close_on_exit default `true`, animation_type 1–6, height, width).
- `getFlyout(name) → Flyout` — fetch existing flyout by name.
- `showLoader(config)` — `config.type='page'` (default `'page'`); `config.template` ∈ enum above (default `'standard'`); `config.message` String (≤ 240 chars).
- `hideLoader()` — no args.

UI_ONLY_ACTIONS:
- Widget binding for `openPopup` / `openCallout` — widget must be created as **Custom Button** type via the Widgets setup screen (referenced by source: "Custom Button type"). Note: No API equivalent — UI-only.
- Mail template ID lookup for `openMailer({templateId})` — created from `Setup → Customization → Templates → Email Templates`. Note: No API equivalent for creating the template — UI-only.

CRITICAL_FAILURE_MODES:
- **Active-loader blocks every other pop-up** — calling `showAlert` while a loader is active silently fails (or queues — source ambiguous). Always `hideLoader()` first. (loader-mutex)
- **`showMessage` Markdown subset is smaller than other pop-ups** — embedding `![alt](url)` in `showMessage` renders raw text, not an image. (showmessage-markdown-restricted)
- **`getInput` cap of 7 inputs per call** — passing > 7 input objects silently truncates or errors.
- **`getInput` multiselect returns nested array** — `output[0]` is the array of selected actual_values; treating as flat strings yields `undefined`. (multiselect-output-shape)
- **`navigateTo` canvas variant silently falls back to standard** if `view.id` omitted — comment `// id is mandatory for canvas` is enforced. (canvas-view-id-required)
- **`navigateTo('record_detail', {module, record_id})` requires `record_id`** — calling without it does not resolve to a record. (param-required)
- **`openPopup` / `openCallout` widget API name must match a **Custom Button type** widget** — other widget types silently fail to mount. (widget-type-required)
- **`createFlyout` returns a Flyout handle; subsequent `getFlyout(name)` fetches the same handle** — calling `createFlyout` twice with same name silently re-uses or replaces (source does not state).
- **`openMailer.templateId` is a record-style ID String** — passing a template name silently no-ops. (id-vs-name)
- **`navigateTo` `data` is opaque to CRM** — on `tab` page it surfaces as widget `PageLoad` data; on other pages it surfaces as `$Page.navigation_data`. Reading the wrong global on the wrong target gives `undefined`. (cross-surface-data-channel)
- **`showLoader` `message` > 240 chars** — silently truncated. (message-cap)

SUPPORTED_PAGES:
| Method | Standard | Canvas | Wizard |
|---|---|---|---|
| `showMessage` | all page types | all page types | all page types |
| `showAlert` | all page types | all page types | all page types |
| `showConfirmation` | all page types | all page types | all page types |
| `getInput` | all page types | all page types | all page types |
| `openMailer` | Detail | Detail | — |
| `navigateTo` | all page types | all page types | all page types |
| `openPopup` | all page types | all page types | all page types |
| `openCallout` | all page types | all page types | all page types |
| `createFlyout` | all page types | all page types | all page types |
| `getFlyout` | all page types | all page types | all page types |
| `showLoader` | all page types | all page types | all page types |
| `hideLoader` | all page types | all page types | all page types |
