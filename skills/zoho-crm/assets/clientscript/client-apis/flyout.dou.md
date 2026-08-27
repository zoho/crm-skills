FILE_PURPOSE: Read when driving a Flyout (created via `ZDK.Client.createFlyout`) — open a Widget inside it with PageLoad data, notify the Widget (with optional await), or close the Flyout.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/Flyout
TRIGGER_KEYWORDS: ZDK.Client.createFlyout, ZDK.Client.getFlyout, Flyout.open, Flyout.notify, Flyout.close, widget PageLoad, Notify, NotifyAndWait, widget sdk 1.2

TECHNICAL_CONSTRAINTS:
- Flyout instances are obtained via `ZDK.Client.getFlyout(name)` after creation via `ZDK.Client.createFlyout(name, config)` (see [client.dou.md](./client.dou.md)).
- **Active-loader mutex** — source verbatim: "The presence of an active loader restricts the availability of other pop-ups." A loader started via `ZDK.Client.showLoader` will block `Flyout.open`. (listener-after-init)
- `open(config, data)` opens a Widget inside the flyout. `config.type` must be the literal String `'widget'`. `config.api_name` is the Widget's API name (registered as a Custom Button-type Widget). `data` is forwarded to the Widget's `'PageLoad'` event (Widget SDK ≥ 1.2).
- `notify(data, options)` — pushes `data` to the Widget. If `options.wait` is `true`, the Widget receives the `'NotifyAndWait'` event and the call awaits the Widget's response (return type `{Any}`); otherwise the Widget receives `'Notify'` (fire-and-forget). Source verbatim: "The 'Notify' is not supported for components."
- `close()` — closes the flyout.
- Source-stated Widget SDK floor: **>= 1.2**. Widgets built against SDK < 1.2 do not receive `'PageLoad'` data forwarded via `open`'s second argument.

REQUIRED_PARAMETERS:
- `open(config, data)`:
  - `config: Object` — flyout type config.
  - `config.type: String` — must be `'widget'` (source enumerates only `widget`).
  - `config.api_name: String` — API name of the Widget (Custom Button type).
  - `data: Any <optional>` — forwarded to the Widget's `'PageLoad'` event.
- `notify(data, options)`:
  - `data: Any` — payload forwarded to Widget's `'Notify'` / `'NotifyAndWait'` event.
  - `options: Object <optional>`.
  - `options.wait: String <optional>` — `'true' | 'false'` (source types `wait` as `String`, not `Boolean`; example passes the boolean literal `true`).
- `close()` — no params.

UI_ONLY_ACTIONS:
- Registering / hosting the Widget that the Flyout loads is a Setup → Developer Space → Widgets action (see [../../widgets/widgets-usage.dou.md](../../widgets/widgets-usage.dou.md)). The Flyout API consumes the Widget API name but does not host the Widget.

CRITICAL_FAILURE_MODES:
- **Active loader blocks `Flyout.open`** — calling `open` while a loader from `ZDK.Client.showLoader` is active silently fails to surface the flyout. Hide the loader first. (listener-after-init)
- **`config.type` must be the literal String `'widget'`** — source enumerates no other value; an unknown type silently fails to open. (label-vs-api-name)
- **`config.api_name` must be the Widget's API name, not its display name** — using the display name fails to resolve the Widget. (label-vs-api-name)
- **Widget must be SDK ≥ 1.2 to receive `data` via `'PageLoad'`** — older Widgets open but their `PageLoad` handler does not receive the forwarded `data`. (listener-after-init)
- **`notify` is not supported for components** — source verbatim: "The 'Notify' is not supported for components." Only Widgets opened via `Flyout.open` receive `Notify` / `NotifyAndWait`. (listener-after-init)
- **`options.wait: true` blocks until the Widget responds** — a Widget that fails to call its `NotifyAndWait` responder leaves the script awaiting indefinitely. Consider a Widget-side timeout.
- **`close()` is silent** — no documented error if the flyout was never opened or was already closed.
- **Widget opened via `Flyout.open` must be registered as Custom Button type** — using any other Widget type (Dashboard, Web Tab, Custom Related List, etc.) silently fails to mount the Widget inside the flyout. When delivering a Flyout solution, always state the Custom Button type requirement in deployment instructions *before* the user registers the Widget in CRM Setup. (widget-type-required)

SUPPORTED_PAGES:
- `open` — no page restriction; available on all page types.
- `notify` — no page restriction; available on all page types.
- `close` — no page restriction; available on all page types.
