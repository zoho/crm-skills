FILE_PURPOSE: Deluge `equalsIgnoreCase()` — compare two TEXT strings for equality, ignoring case differences.
MENTAL_MODEL: `str1.equalsIgnoreCase(str2)` = BOOLEAN; full-string equality ignoring case; spaces and all other chars remain significant.

WHEN_TO_USE:
- Compare two text strings for equality while treating uppercase and lowercase as equivalent.
- Validate user input against a known string without requiring exact case match.

WHEN_NOT_TO_USE:
- When exact case-sensitive equality is required — use the `==` operator instead.
- When checking for substring presence (not full-string equality) — use `contains()` instead.

TRIGGER_KEYWORDS:
equalsIgnoreCase(), case-insensitive equality, full-string equality check, spaces-significant, ignore-case comparison

RULES:
- Return type: BOOLEAN.
- Input types: TEXT (string1), TEXT (string2).
- Performs a case-insensitive comparison of the full strings.
- Spaces and all non-letter characters are significant: `"ZohoCRM"` vs `"Zoho CRM"` (space differs) → false.
- Both `.equalsIgnoreCase(str2)` and `equalsIgnoreCase(str1, str2)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
Product = "ZohoCRM";
var = equalsIgnoreCase(Product, "ZohoCRM");   // true  (same string, any casing)
var = equalsIgnoreCase(Product, "ZOHOCREATOR");   // true  (case-insensitive)
var = equalsIgnoreCase(Product, "Zoho CRM");  // false (space differs)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Text functions — text.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/equalsIgnoreCase.html
