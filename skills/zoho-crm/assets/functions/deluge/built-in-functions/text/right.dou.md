FILE_PURPOSE: Deluge `right()` — return a specified number of characters from a string's right side.
MENTAL_MODEL: `str.right(n)` = TEXT; last `n` chars; negative or exceeding-length `n` throws a runtime error.

WHEN_TO_USE:
- Extract a known-length suffix from a text string.

WHEN_NOT_TO_USE:
- When characters from the left side are needed — use `left()` instead.
- When a substring at an arbitrary position is needed — use `subString()` or `subText()` instead.

TRIGGER_KEYWORDS:
right(), right-side characters, right-suffix extraction, right-overflow runtime, right negative-n

RULES:
- Return type: TEXT.
- Input types: TEXT (string), NUMBER (number of characters to return).
- Syntax: `<string>.right(<number>)` (only one syntax form documented in source).
- If `number` exceeds the character count of the string → runtime error.
- If `number` is negative → runtime error.

CANONICAL_EXAMPLES:
```deluge
product_name = "Zoho CRM";
text = product_name.right(3);  // returns "CRM"
```

FAILURE_MODES:
- `right(n)` where `n` exceeds the string's character count throws a runtime error.
- `right(n)` where `n` is negative throws a runtime error.

RELATED_DOCS:
- left — left.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/right.html
