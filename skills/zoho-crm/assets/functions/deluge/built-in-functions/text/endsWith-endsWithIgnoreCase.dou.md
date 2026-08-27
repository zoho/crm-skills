FILE_PURPOSE: Deluge `endsWith()` / `endsWithIgnoreCase()` — check if a TEXT string ends with a specific suffix.
MENTAL_MODEL: `str.endsWith(suffix)` = BOOLEAN; `endsWith()` is case-sensitive; `endsWithIgnoreCase()` ignores case.

WHEN_TO_USE:
- Validate that a string ends with a specific suffix (e.g., file extension, domain ending).
- Check suffix match without caring about letter case using `endsWithIgnoreCase()`.

WHEN_NOT_TO_USE:
- When checking the start of a string — use `startsWith()` instead.
- When checking anywhere in the string (not just the end) — use `contains()` instead.

TRIGGER_KEYWORDS:
endsWith(), endsWithIgnoreCase(), suffix check, case-sensitive endsWith, case-insensitive endsWith

RULES:
- Return type: BOOLEAN.
- Input types: TEXT (string), TEXT (searchString).
- `endsWith()`: performs a case-sensitive search.
- `endsWithIgnoreCase()`: performs a case-insensitive search.
- Returns `false` (not an error) when `searchString` is not found at the end.

CANONICAL_EXAMPLES:
```deluge
Product = "Zoho CRM";
var    = endsWith(Product, "CRM");             // true  (exact case match)
var    = endsWith(Product, "creator");             // false (case mismatch)
boolVal = endsWithIgnoreCase(Product, "creator"); // true  (case-insensitive)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- startsWith — https://www.zoho.com/deluge/help/functions/string/endswith.html
- Text functions — text.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/endswith.html, https://www.zoho.com/deluge/help/functions/string/endswithignorecase.html
