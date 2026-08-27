FILE_PURPOSE: Deluge `leftpad()` — add leading whitespace to a text string for alignment.
MENTAL_MODEL: `str.leftpad(n)` = TEXT with `n` leading spaces prepended; max `n` is 100; negative `n` returns original string.

WHEN_TO_USE:
- Add leading whitespace to a text string for fixed-width formatting or column alignment.

WHEN_NOT_TO_USE:
- When right-side padding is needed — use `rightpad()` instead.
- When non-space padding characters are required — this function pads with whitespace only.

TRIGGER_KEYWORDS:
leftpad(), left-pad whitespace, leading-space prepend, negative-pad no-change, leftpad max-limit

RULES:
- Return type: TEXT.
- Input types: TEXT (text), NUMBER (whitespaces).
- Both `.leftpad(<whitespaces>)` and `leftpad(<text>, <whitespaces>)` syntaxes are valid.
- Pads with whitespace characters only (padding character is not configurable).
- Negative `whitespaces` value returns the original string unchanged.
- Maximum `whitespaces` value: 100 (source notation "100,00" is a typo; authoritative value is 100).
- `whitespaces` is the number of spaces to prepend (per source description); source example output appears inconsistent with this but the description is treated as authoritative.

CANONICAL_EXAMPLES:
```deluge
text = "Left";
newText = text.leftpad(6);  // returns "  Left" (per source example)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- rightpad — rightpad.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/leftpad.html
