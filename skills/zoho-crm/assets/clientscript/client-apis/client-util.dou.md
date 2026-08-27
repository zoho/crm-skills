FILE_PURPOSE: Read when reading client-side context (userAgent, online status, platform, current URL, geo-location, selected text, root-context page) or driving client-side actions (soft refresh, open URL, copy to clipboard) via the `$Client` utility.
SOURCE_DOC: https://www.zohocrm.dev/explore/client-script/clientapi/$Client
TRIGGER_KEYWORDS: $Client.userAgent, $Client.isOnline, $Client.platform, $Client.url, $Client.geoLocation, $Client.selectedValue, $Client.refresh, $Client.openURL, $Client.copyToClipboard, $Client.rootContext

TECHNICAL_CONSTRAINTS:
- `$Client` is a global utility namespace; **most properties are accessed as bare property reads** (source examples: `$Client.userAgent;`, `$Client.isOnline;`, `$Client.platform;`, `$Client.url;`, `$Client.geoLocation;`, `$Client.selectedValue;`, `$Client.rootContext`), while `refresh`, `openURL`, `copyToClipboard` are called as **methods** with parens.
- `$Client.userAgent` — browser User-Agent String (source example: a Chrome 100 on macOS UA String).
- `$Client.isOnline` — `Boolean` indicating client online status.
- `$Client.platform` — String. Source example output: `'web'`.
- `$Client.url` — current page URL String (source example shows a `crm.zoho.com` Leads create URL with `org<id>/tab/Leads/create?layoutId=<id>`).
- `$Client.geoLocation` — Object: `{ latitude, longitude, altitude, accuracy, altitudeAccuracy, heading, speed }` (numeric or `null`). **Triggers a browser permission prompt** — source verbatim: "the user is asked for permission to report location information".
- `$Client.selectedValue` — Object: `{ value: String }` — text currently selected by the user on the page. Source documents the signature as `selectedValue()` (method form) but the example uses bare property access.
- `$Client.refresh(config)` — soft-refreshes the client. `config.triggerOnLoad: Boolean <optional>` — if `true`, re-fires the page's `onLoad` event. Examples: `$Client.refresh()` and `$Client.refresh({ triggerOnLoad: true })`.
- `$Client.openURL(url)` — opens `url` in a new browser tab/window. `url: String`.
- `$Client.copyToClipboard(text)` — copies `text` to the clipboard. `text: string`.
- `$Client.rootContext` — Object: stores the **original page context that launched a form**. Used in multi-context cases (Quick Create) to reach the parent record's fields. Source example: `$Client.rootContext.getField('Name').getValue()` — `rootContext` exposes the same `getField` / etc. shape as `ZDK.Page` (i.e. it is a Page-like object).

REQUIRED_PARAMETERS:
- `$Client.userAgent` — no invocation; returns String.
- `$Client.isOnline` — no invocation; returns Boolean.
- `$Client.platform` — no invocation; returns String.
- `$Client.url` — no invocation; returns String.
- `$Client.geoLocation` — no invocation; returns Object (triggers browser permission prompt).
- `$Client.selectedValue` — no invocation; returns `{ value: String }`.
- `$Client.refresh(config?)` — `config: Object`; `config.triggerOnLoad: Boolean <optional>`.
- `$Client.openURL(url)` — `url: String`.
- `$Client.copyToClipboard(text)` — `text: string`.
- `$Client.rootContext` — no invocation; returns a Page-like Object (use its `getField` etc. methods — see [page.dou.md](./page.dou.md)).

UI_ONLY_ACTIONS:
- Granting / revoking geo-location permission is a browser-level Setup → Site Settings action (e.g. Chrome Settings → Privacy → Site Settings). The script cannot request permission programmatically without invoking `$Client.geoLocation`.
- Clipboard permission may require a user-gesture context in some browsers; opening preferences to grant clipboard access is browser-side.

CRITICAL_FAILURE_MODES:
- **`$Client.geoLocation` triggers a permission prompt** — first-time access shows a browser dialog; the user may deny, in which case the returned object may be empty / `null` / throw (source does not document the rejection path). Wrap in try-catch and handle absent permission.
- **`$Client.copyToClipboard` requires a user-gesture context in modern browsers** — calling it from a non-user-initiated handler (e.g. on page load) silently fails in Chrome / Firefox / Safari. Trigger only from click / keypress handlers.
- **`$Client.openURL` opens a new tab/window** — popup blockers may suppress non-user-gesture openURL calls; same gesture-context requirement as clipboard.
- **`$Client.refresh({triggerOnLoad:true})` re-fires `onLoad`** — calling it from inside an `onLoad` handler creates an unbounded refresh loop. (recursion)
- **`$Client.rootContext` is only meaningful in multi-context launchers (Quick Create)** — in a normal Detail / Create flow `rootContext` may be undefined or equal to the current page; do not assume parent-record access elsewhere.
- **`$Client.url` is a String snapshot** — subsequent SPA navigation does not update the previously-read value; re-read on each use.
- **`$Client.platform` enum is not fully documented** — branching on `platform === 'web'` may exclude legitimate mobile / embedded contexts.
- **`$Client.selectedValue.value`** is `''` (empty) when nothing is selected (per common DOM selection semantics) — source does not document the empty-selection shape.
