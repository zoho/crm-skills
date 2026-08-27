FILE_PURPOSE: Deluge removeAllAlphaNumeric() — strip all letters and digits from a string
MENTAL_MODEL: removeAllAlphaNumeric(string) = TEXT; removes [a-zA-Z0-9]; spaces and special chars retained

WHEN_TO_USE:
- Extract only spaces and special characters from a mixed string.
- Isolate punctuation or symbols from a string containing letters and digits.

WHEN_NOT_TO_USE:
- Removing only letters (keeping digits) — use `removeAllAlpha()` instead.

TRIGGER_KEYWORDS:
removeAllAlphaNumeric, string.removeAllAlphaNumeric, strip alphanumeric, special chars only, empty on all-alphanumeric

RULES:
- Two syntaxes: `<variable> = <string>.removeAllAlphaNumeric();` and `removeAllAlphaNumeric(<string>)`.
- Return type: TEXT.
- Removes all alphanumeric characters (letters a–z, A–Z and digits 0–9) from the string.
- Returns all other characters, including spaces.
- If the string contains only alphanumeric characters, returns an empty string.
- `<string>` must be TEXT.

CANONICAL_EXAMPLES:
```deluge
Product = "Zoho CRM v8 is live!";
newText = Product.removeAllAlphaNumeric(); // returns " !"
```

FAILURE_MODES:
- String contains only alphanumeric characters → returns empty string (not null; no error).

RELATED_DOCS:
- removeAllAlpha — remove-all-alpha.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/removeallalphanumeric.html
