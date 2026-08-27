FILE_PURPOSE: Deluge `ltrim` — remove all leading whitespace characters from the left side of a string.
MENTAL_MODEL: `str.ltrim()` = TEXT with all leading spaces stripped; trailing spaces and internal spaces are unaffected.

WHEN_TO_USE:
- Remove leading (left-side) whitespace from a text string before processing or comparison.

WHEN_NOT_TO_USE:
- When trailing (right-side) whitespace needs removal — use `rtrim()` instead.
- When ALL leading and trailing whitespace should be removed — use `trim()` instead.

TRIGGER_KEYWORDS:
ltrim(), leading-whitespace removal, left-trim, ltrim vs trim, ltrim vs rtrim

RULES:
- Return type: TEXT.
- Input type: TEXT.
- Removes ALL whitespace inserted BEFORE the text (all leading spaces).
- Trailing and internal spaces are not affected.
- Both `.ltrim()` and `ltrim(<input_text>)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
text = "   Zoho";
result = text.ltrim();          // returns "Zoho"

text_size   = text.length();    // returns 7  (3 leading spaces + 4 chars)
result_size = result.length();  // returns 4
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- rtrim — rtrim.dou.md
- trim — trim.dou.md
- length — len-length.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/ltrim.html
