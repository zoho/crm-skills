FILE_PURPOSE: Deluge `startsWith()` / `startsWithIgnoreCase()` — check if a TEXT string starts with a prefix.
MENTAL_MODEL: `str.startsWith(prefix)` = BOOLEAN; `startsWith()` is case-sensitive; `startsWithIgnoreCase()` ignores case.

WHEN_TO_USE:
- Validate that a string begins with a specific prefix (e.g., protocol, keyword, category).
- Check prefix match without caring about letter case using `startsWithIgnoreCase()`.

WHEN_NOT_TO_USE:
- When checking the end of a string — use `endsWith()` instead.
- When checking anywhere in the string (not just the start) — use `contains()` instead.

TRIGGER_KEYWORDS:
startsWith(), startsWithIgnoreCase(), prefix check, case-sensitive startsWith, case-insensitive startsWith

RULES:
- Return type: BOOLEAN.
- Input types: TEXT (string), TEXT (searchString).
- `startsWith()`: performs a case-sensitive search.
- `startsWithIgnoreCase()`: performs a case-insensitive search.
- Returns `false` (not an error) when `searchString` is not found at the start.

CANONICAL_EXAMPLES:
```deluge
Product = "Zoho CRM";
var = startsWith(Product, "Zoho");             // true  (exact case match)
var = startsWith(Product, "zoho");             // false (case mismatch)
var = startsWithIgnoreCase(Product, "zoho");   // true  (case-insensitive)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- endsWith — endsWith-endsWithIgnoreCase.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/startswith.html, https://www.zoho.com/deluge/help/functions/string/startswithignorecase.html
