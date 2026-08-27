FILE_PURPOSE: Deluge `left()` — return a specified number of characters from a string's left side.
MENTAL_MODEL: `str.left(n)` = TEXT; first `n` chars of `str`; negative `n` returns full string; exceeding length throws.

WHEN_TO_USE:
- Extract a known-length prefix from a text string.

WHEN_NOT_TO_USE:
- When characters from the right side are needed — use `right()` instead.
- When a substring at an arbitrary position is needed — use `mid()` or `substring()` instead.

TRIGGER_KEYWORDS:
left(), substring from-left, left-side characters, negative-n full-string, left-overflow runtime

RULES:
- Return type: TEXT.
- Input types: TEXT (string), NUMBER (number of characters to return).
- Syntax: `<string>.left(<number>)` (only one syntax form documented in source).
- If `number` exceeds the character count of the string → runtime error.
- If `number` is negative → returns the full original string unchanged.

CANONICAL_EXAMPLES:
```deluge
product_name = "Zoho CRM";
newText = product_name.left(4);   // returns "Zoho"
```

FAILURE_MODES:
- `left(n)` where `n` exceeds the string's character count throws a runtime error.

RELATED_DOCS:
- right — right.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/left.html
