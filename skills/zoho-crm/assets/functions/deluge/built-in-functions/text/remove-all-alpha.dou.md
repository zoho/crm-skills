FILE_PURPOSE: Deluge removeAllAlpha() — strip all alphabetic letters from a string
MENTAL_MODEL: removeAllAlpha(string) = TEXT; removes all [a-zA-Z] letters; spaces and non-letter chars retained

WHEN_TO_USE:
- Extract only digits, spaces, and special characters from a mixed string.
- Strip letter characters to isolate numeric or symbolic content.

WHEN_NOT_TO_USE:
- Removing digits as well — use `removeAllAlphaNumeric()` instead.

TRIGGER_KEYWORDS:
removeAllAlpha, string.removeAllAlpha, strip letters, alpha removal, empty on all-alpha

RULES:
- Two syntaxes: `<variable> = <string>.removeAllAlpha();` and `removeAllAlpha(<string>)`.
- Return type: TEXT.
- Removes all alphabetic letters (a–z, A–Z) from the string.
- Returns all other characters, including spaces and digits.
- If the string contains only letters, returns an empty string.
- `<string>` must be TEXT.

CANONICAL_EXAMPLES:
```deluge
Product = "Zoho CRM 8";
newText = Product.removeAllAlpha(); // returns " 5"
```

FAILURE_MODES:
- String contains only letters → returns empty string (not null; no error).

RELATED_DOCS:
- removeAllAlphaNumeric — remove-all-alphanumeric.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/removeAllAlpha.html
