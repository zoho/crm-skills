FILE_PURPOSE: Deluge `contains()` / `containsIgnoreCase()` — check if a TEXT string contains a substring.
MENTAL_MODEL: `str.contains(sub)` = BOOLEAN; `contains()` is case-sensitive; `containsIgnoreCase()` ignores case.

WHEN_TO_USE:
- Check if a substring exists anywhere within a text string (case-sensitive).
- Check if a substring exists regardless of letter case using `containsIgnoreCase()`.

WHEN_NOT_TO_USE:
- When checking only at the start or end of a string — use `startsWith()` or `endsWith()` instead.
- When the position (index) of the substring is needed — use `find()` / `indexOf()` instead.

TRIGGER_KEYWORDS:
contains(), containsIgnoreCase(), substring existence check, case-sensitive contains, case-insensitive contains

RULES:
- Return type: BOOLEAN.
- Input types: TEXT (string), TEXT (searchString).
- `contains()`: performs a case-sensitive search.
- `containsIgnoreCase()`: performs a case-insensitive search.
- Returns `false` (not an error) when the `searchString` is not found.
- Space character is a valid `searchString` and is treated like any other character.

CANONICAL_EXAMPLES:
```deluge
Product = "Zoho CRM";
check = Product.contains("CRM");           // true  (exact case match)
check = Product.contains("creator ");          // false (case mismatch and trailing space)
check = Product.contains(" ");                 // true  (space is a valid search string)
boolVal = Product.containsIgnoreCase("creator"); // true  (case-insensitive)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- notContains — ../../built-in-functions/list/../list/list-notContains-isEmpty.dou.md
- Text functions — text.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/contains.html, https://www.zoho.com/deluge/help/functions/string/containsignorecase.html
