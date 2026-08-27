FILE_PURPOSE: Deluge mid() — extract a substring between two 0-based character indices
MENTAL_MODEL: mid(text, start, end) = TEXT slice [start, end); 0-based; end optional; start must not exceed length

WHEN_TO_USE:
- Extract a substring from a known start index to a known end index.
- Extract from a start index to the end of the string (omit end_index).

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
mid, string.mid, start_index, end_index optional, 0-based index mid, substring mid

RULES:
- Two syntaxes: `<variable> = <source_text>.mid(<start_index>, [<end_index>]);` and `mid(<source_text>, <start_index>, [<end_index>])`.
- Return type: TEXT.
- Index is 0-based.
- `<end_index>` is optional; if omitted, rest of text from `<start_index>` is returned.
- Negative `<end_index>` is treated as omitted; rest of text from `<start_index>` is returned.
- If `<start_index>` equals `<end_index>`, returns empty string.
- Returned text includes `<start_index>` character and excludes `<end_index>` character.
- `<start_index>` and `<end_index>` must not exceed the length of `<source_text>`.
- `<end_index>` must be greater than or equal to `<start_index>`.

CANONICAL_EXAMPLES:
```deluge
sourceText = "Welcome to Zoho Deluge";
newText = sourceText.mid(11, 22);
info newText; // returns "Zoho Deluge"
```

FAILURE_MODES:
- `<start_index>` or `<end_index>` exceeds length of `<source_text>` → runtime error.
- `<end_index>` is less than `<start_index>` → runtime error.

RELATED_DOCS:
- subString — subString-subText.dou.md
- subText — subString-subText.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/mid.html
