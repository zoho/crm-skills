FILE_PURPOSE: Deluge `rtrim` — remove all trailing whitespace characters from the right side of a string.
MENTAL_MODEL: `str.rtrim()` = TEXT with all trailing spaces stripped; leading and internal spaces are unaffected.

WHEN_TO_USE:
- Remove trailing (right-side) whitespace from a text string before processing.

WHEN_NOT_TO_USE:
- When leading (left-side) whitespace needs removal — use `ltrim()` instead.
- When ALL leading and trailing whitespace should be removed — use `trim()` instead.

TRIGGER_KEYWORDS:
rtrim(), trailing-whitespace removal, right-trim, rtrim vs trim, rtrim vs ltrim

RULES:
- Return type: TEXT.
- Input type: TEXT.
- Removes ALL whitespace inserted AFTER the text (trailing spaces).
- Leading and internal spaces are not affected.
- Both `.rtrim()` and `rtrim(<input_text>)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
text = "   Zoho Deluge   ";
result = text.rtrim();          // returns "   Zoho Deluge"

text_size   = text.length();    // returns 17
result_size = result.length();  // returns 14
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- ltrim — ltrim.dou.md
- trim — trim.dou.md
- length — len-length.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/rtrim.html
