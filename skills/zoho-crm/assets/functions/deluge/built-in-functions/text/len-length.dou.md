FILE_PURPOSE: Deluge `len()` / `length()` — return the character count (including spaces) of a text string.
MENTAL_MODEL: `str.len()` = NUMBER of chars including spaces; `str.length()` is a direct alias.

WHEN_TO_USE:
- Determine the total number of characters in a text string (spaces count).
- Validate string length before passing to length-limited functions.

WHEN_NOT_TO_USE:
- When checking if a string is empty — use `isEmpty()` instead.

TRIGGER_KEYWORDS:
len(), length(), character count, spaces-included count, len-length aliases, string length check

RULES:
- Return type: NUMBER.
- Input type: TEXT.
- `len()` and `length()` are aliases; all four syntaxes are equivalent:
  `.len()`, `len(str)`, `.length()`, `length(str)`.
- Spaces are included in the returned character count.

CANONICAL_EXAMPLES:
```deluge
text = "Manage customer relationships with Zoho CRM";
count      = text.len();     // returns 46
textLength = text.length();  // returns 46 — length() is alias of len()
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- ltrim — ltrim.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/len.html, https://www.zoho.com/deluge/help/functions/string/length.html
