FILE_PURPOSE: Deluge `rightpad()` — add trailing whitespace to a text string for alignment.
MENTAL_MODEL: `str.rightpad(n)` = TEXT with `n` trailing spaces appended; max 100; negative `n` returns original.

WHEN_TO_USE:
- Add trailing whitespace to a text string for fixed-width formatting or column alignment.

WHEN_NOT_TO_USE:
- When left-side padding is needed — use `leftpad()` instead.
- When non-space padding characters are required — this function pads with whitespace only.

TRIGGER_KEYWORDS:
rightpad(), right-pad whitespace, trailing-space append, negative-pad no-change, rightpad max-100

RULES:
- Return type: TEXT.
- Input types: TEXT (text), NUMBER (whitespaces).
- Both `.rightpad(<whitespaces>)` and `rightpad(<text>, <whitespaces>)` syntaxes are valid.
- Pads with whitespace characters only (padding character is not configurable).
- Negative `whitespaces` value returns the original string unchanged.
- Maximum `whitespaces` value: 100 (source notation "100,00" is a typo; same resolution as leftpad).
- `whitespaces` is the number of spaces to append (per source description; same pattern as leftpad — description treated as authoritative despite example inconsistency).

CANONICAL_EXAMPLES:
```deluge
text = "Right";
newText = text.rightpad(6);  // returns "Right " (per source example)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- leftpad — leftpad.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/rightpad.html
