FILE_PURPOSE: Deluge `openUrl()` — browser-navigate to a URL in a target window.
MENTAL_MODEL: `openUrl(url, window)` = client-side browser navigation; terminal statement — only the last call per action executes.

WHEN_TO_USE:
- Redirect the user to another page or external URL after an action.
- Navigate back in browser history using `#Script:page.back`.

WHEN_NOT_TO_USE:
- In a custom action placed in the View header — `openUrl` does not execute in that context.
- When multiple `openUrl` calls are configured in one action — only the LAST one executes; earlier calls are silently ignored.

TRIGGER_KEYWORDS:
openUrl, same window, new window, parent window, page.back, successive=true

RULES:
- Syntax: `openUrl(<URL>, <window>, [optional_param]);`
- Supported `window` values: `same window`, `new window`, `parent window`.
- All URLs must include a protocol prefix (e.g. `https://`).
- `optional_param` when window is `new window`: omitting it causes all subsequent clicks to reuse the same new window; set `successive=true` to force each call to open a distinct window.
- `openUrl` is a terminal statement — when multiple `openUrl` tasks appear in one action, only the last one executes.

CANONICAL_EXAMPLES:
```deluge
// Open an external URL in a new tab from a CRM Button action
openUrl("https://maps.google.com/?q=" + billingAddress, "new window", "successive=true");

// Navigate back in browser history
openUrl("#Script:page.back", "same window");
```

FAILURE_MODES:
- Multiple `openUrl` tasks in one action: only the last one executes; all earlier `openUrl` calls are silently discarded.
- `openUrl` inside a custom action placed in the View header does not execute — task is not supported in that context.
- Omitting the protocol prefix (e.g. `www.zoho.com` instead of `https://www.zoho.com`) causes the URL to not open correctly.
- When `new window` and no `successive=true`, subsequent `openUrl` calls reuse the same tab instead of opening new ones.

RELATED_DOCS:
*(none)*

SOURCE:
https://www.zoho.com/deluge/help/openurl.html
