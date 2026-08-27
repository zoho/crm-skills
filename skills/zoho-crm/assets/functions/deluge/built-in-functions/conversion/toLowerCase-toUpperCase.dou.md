FILE_PURPOSE: Deluge `toLowerCase()` / `toUpperCase()` — convert all string letters to lower or upper case.
MENTAL_MODEL: `str.toLowerCase()` = all-lowercase TEXT; `str.toUpperCase()` = all-uppercase TEXT; `lower()`/`upper()` are aliases.

WHEN_TO_USE:
- Normalise string case before storage or display formatting.
- Perform case-insensitive comparison by converting both strings to the same case first.

WHEN_NOT_TO_USE:
- When comparing strings case-insensitively — prefer `equalsIgnoreCase()` or `containsIgnoreCase()` directly to avoid creating an intermediate string.

TRIGGER_KEYWORDS:
toLowerCase(), toUpperCase(), lower(), upper(), lowercase conversion, uppercase conversion, case-normalise

RULES:
- Return type: TEXT.
- Input type: TEXT.
- `toLowerCase()` and `lower()` are aliases; all four syntaxes are equivalent.
- `toUpperCase()` and `upper()` are aliases; all four syntaxes are equivalent.
- Only letter characters are converted; digits, spaces, and special characters are unchanged.

CANONICAL_EXAMPLES:
```deluge
mainString = "Create online database applications";

newText = lower(mainString);
// returns "create online database applications"

newText = upper(mainString);
// returns "CREATE ONLINE DATABASE APPLICATIONS"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- equalsIgnoreCase — ../text/../text/equalsIgnoreCase.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/tolowerCase.html, https://www.zoho.com/deluge/help/functions/string/touppercase.html
