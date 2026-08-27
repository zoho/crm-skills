FILE_PURPOSE: Deluge `concat()` — join two TEXT strings into a single concatenated string.
MENTAL_MODEL: `text1.concat(text2)` = TEXT; equivalent to `text1 + text2`; both arguments must be TEXT.

WHEN_TO_USE:
- Append one text string to another to form a combined string.
- Chain multiple `concat()` calls to join more than two strings.

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
concat, text1.concat(text2), chained concat, string join, text concatenation

RULES:
- Return type: TEXT.
- Input types: TEXT, TEXT.
- Both `.concat(text2)` and `concat(text1, text2)` syntaxes are valid.
- `concat()` calls can be chained: `text1.concat(" ").concat(text2)`.

CANONICAL_EXAMPLES:
```deluge
text1 = "Zoho";
text2 = "Deluge";
result = text1.concat(text2);
info concat(text1, text2);             // yields "ZohoDeluge"
info result;                           // yields "ZohoDeluge"
info text1.concat(" ").concat(text2);  // yields "Zoho Deluge"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Text functions — text.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/concat.html
