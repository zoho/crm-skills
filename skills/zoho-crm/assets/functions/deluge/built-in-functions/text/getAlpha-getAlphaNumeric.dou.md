FILE_PURPOSE: Deluge `getAlpha()` / `getAlphaNumeric()` — extract letters or alphanumeric characters from a string.
MENTAL_MODEL: `str.getAlpha()` = letters only; `str.getAlphaNumeric()` = letters + digits; all other chars stripped and compacted.

WHEN_TO_USE:
- Strip all non-letter characters (digits, spaces, punctuation, special chars) from a string using `getAlpha()`.
- Strip all non-alphanumeric characters (spaces, punctuation, special chars) using `getAlphaNumeric()`.

WHEN_NOT_TO_USE:
- When specific characters (not all non-alpha) need removal — use `remove()` or `replaceAll()` instead.
- When the original character positions or spacing must be preserved — these functions compact the result with no separators.

TRIGGER_KEYWORDS:
getAlpha(), getAlphaNumeric(), extract letters only, extract alphanumeric, strip special chars, spaces stripped

RULES:
- Return type: TEXT.
- Input type: TEXT.
- `getAlpha()`: returns only letter characters (A-Z, a-z); digits, spaces, and all other characters are removed.
- `getAlphaNumeric()`: returns only letters and digits (A-Z, a-z, 0-9); spaces, hyphens, and special characters are removed.
- Characters are returned in their original order; the result is a compacted string with no separators.
- Both `.getAlpha()` and `getAlpha(str)` syntaxes are valid; same for `getAlphaNumeric()`.

CANONICAL_EXAMPLES:
```deluge
Subject = "Your joining date is January 25th, 2019";
letters = getAlpha(Subject);
// returns "YourjoiningdateisJanuaryth"  (digits, comma, space stripped)

Subject = "Your joining date is 25-01-2019";
chars = getAlphaNumeric(Subject);
// returns "Yourjoiningdateis25012019"  (hyphens, spaces stripped)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- removeAllAlpha — https://www.zoho.com/deluge/help/functions/string/getAlpha.html
- Text functions — text.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/getAlpha.html, https://www.zoho.com/deluge/help/functions/string/getAlphaNumeric.html
