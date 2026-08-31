FILE_PURPOSE: Read when prompting users from a Widget via `ZDK.Client` dialogs / loaders / popups or returning a popup result via `$Client.close()`.
SOURCE_DOC: https://www.zohocrm.dev/explore/widgets/v1.5/ZDK_Client, https://www.zohocrm.dev/explore/widgets/v1.5/$Client
TRIGGER_KEYWORDS: ZDK.Client, getInput, showAlert, showConfirmation, showLoader, showMessage, openPopup, sendResponse, $Client.close

TECHNICAL_CONSTRAINTS:
- All `ZDK.Client.show*` and `getInput` calls are blocked while a loader is active — call `hideLoader()` before opening another dialog.
- `getInput` field-type caps: `text` 120 chars, `number` 50 digits, `textarea` 2000 chars, `picklist` / `multiselectpicklist` 2000 options × 120 chars each, max 7 fields per call.
- `openPopup` requires the target Widget's `api_name` (Custom Button type) and `type: 'widget'`; minimum target Widget-SDK version `>= 1.2`.
- `openPopup` `animation_type` accepts integer enum `1`–`6`; default `1`. `header: undefined` hides the header bar; default header is the Widget name.
- `showLoader` `template` enum: `'spinner' | 'vertical-bar' | 'standard'` (default `'standard'`); `message` ≤ 240 chars.
- `showMessage` `options.type` enum: `'info' | 'error' | 'warning' | 'success'`; image markdown is **not** supported in `showMessage`.
- Supported markdown across alert / message / confirmation: italics `_x_`, bold `*x*`, underline `__x__`, strikeout `~x~`, code, headings `# / ###`, blockquote `!x`, hyperlink, image (alerts only).
- `openPopup` resolves with whatever `$Client.close(response)` passes back — type is any of: object, string, number, boolean.
- `$Client.close(response)` is only valid inside a Widget that was launched via `openPopup` or as a Flyout — calling it elsewhere is a no-op.
- `sendResponse(uuid, data)` is paired one-to-one with a `NotifyAndWait` event; the `uuid` is `data.id` from that event payload (see [widgets-jssdk-events.dou.md](./widgets-jssdk-events.dou.md)).

REQUIRED_PARAMETERS:
- `getInput(options[], heading?, accept_message?='Okay', reject_message?='Cancel')`; each `options[i]` needs `{ type, label?, default_value?, list_options? }`.
- `openPopup(config, data?)`; `config` requires `api_name` + `type`; optional `header`, `close_icon` (default `true`), `close_on_escape`, `animation_type`, `height`, `width`, `left`.
- `sendResponse(request_uuid: string, data?: any)`; `request_uuid` is `data.id` from the `NotifyAndWait` event.
- `showAlert(message, heading?, accept_message?='Okay')`.
- `showConfirmation(message, accept_message?='Yes, Proceed', reject_message?='Cancel')` resolves to `true | false`.
- `showLoader({ type?='page', template?='standard', message? })`.
- `showMessage(message, { type?='info' })`.
- `$Client.close(response?: any)`.

UI_ONLY_ACTIONS:
*(none in source)*

CRITICAL_FAILURE_MODES:
- Second dialog / loader invoked while a loader is still active: SDK silently suppresses the second call — always `hideLoader()` first.
- `openPopup` target `api_name` is the Widget display label instead of the API name: popup never opens, no error — use the Custom Button Widget's API name verbatim (`label-vs-api-name`).
- `sendResponse` called with a stale or wrong UUID: the original `NotifyAndWait` caller hangs until the ClientScript flyout timeout fires.
- `$Client.close` called from a Widget that was opened via a regular CRM placement (not `openPopup`): no-op, parent never receives a response.
- `showMessage` payload contains image markdown: image renders as raw text — switch to `showAlert` for image content.
- `getInput` `picklist` / `multiselectpicklist` `default_value` not present in `list_options.actual_value`: option silently dropped from the selection.
- `multiselectpicklist` default supplied as a comma-joined string instead of an array of strings: input renders empty selection.
- Forgetting `await` on `openPopup` / `getInput` / `showConfirmation`: subsequent code runs against a Promise rather than the user's response.
- `showLoader` opened in a background tab, then user backgrounds the widget for >40 s: loader persists into next interaction — pair every `showLoader` with a `try / finally hideLoader()`.
- Markdown injection from untrusted CRM record content into `showAlert(message, ...)`: links can be spoofed — sanitize record-sourced strings before passing.
- `getInput` consumer indexes the result array by label-derived index instead of input order: re-ordering inputs at refactor time silently swaps values — destructure by position with explicit names.
- `showLoader` `template: 'spinner'` chosen for an instant operation: visual flash without value — reserve spinner / vertical-bar for long-running async work.
- `openPopup` `header: undefined` hides the header but caller still relies on the header to communicate context: users lose context cue — supply explicit header text instead.
- `getInput` `multiselectpicklist` result returned as a nested array (per source: `[ ['A', 'C'] ]`): caller indexes `result[0]` expecting a string — destructure the inner array.
- `showConfirmation` resolved value `true` interpreted as the accept-button label string: source returns Boolean only — branch on `=== true` / `=== false`.
- `openPopup` `width` / `height` / `left` passed as integers instead of CSS-unit strings (`'450px'`, `'10px'`): popup renders unsized — always include unit suffix.
- `sendResponse` invoked twice for the same UUID: SDK behaviour undocumented; second call can no-op or error — emit exactly once per `NotifyAndWait` event.
- `showAlert` / `showConfirmation` hyperlink markdown opens in a new tab inside the iframe sandbox — set `target` expectations accordingly; in-iframe navigation breaks the widget.
- `$Client.close(undefined)`: parent `openPopup` resolves with `undefined`, not a closed-marker object — caller must distinguish cancellation from explicit-empty.
- `getInput` dialog while another widget on the same page holds an active loader: dialog is suppressed cross-widget — coordinate loader lifecycle across widgets on shared pages.
