FILE_PURPOSE: Deluge `subString()` / `subText()` — extract a substring between two 0-based character indices.
MENTAL_MODEL: `str.subString(start, end)` = TEXT[start..end); 0-based; end is exclusive; `subText()` is a direct alias.

WHEN_TO_USE:
- Extract a substring at an arbitrary position within a text string using start and end indices.
- Extract from a start index to the end of the string by omitting end_index.

WHEN_NOT_TO_USE:
- When extracting from the left or right by character count — use `left()` or `right()` instead.
- When extracting based on a delimiter — use `getPrefix()` or `getSuffix()` instead.

TRIGGER_KEYWORDS:
subString(), subText(), start-index substring, end-index exclusive, zero-based substring, negative-end-index-ignored

RULES:
- Return type: TEXT.
- Input types: TEXT (source_text), NUMBER (start_index), NUMBER (end_index, optional).
- `subString()` and `subText()` are aliases; all four syntaxes are equivalent.
- Index is 0-based (first character = index 0).
- `end_index` is EXCLUSIVE — the character at end_index is NOT included in the result.
- If `end_index` is omitted or negative → returns from start_index to end of string.
- If `start_index` equals `end_index` → returns empty text (no error).
- If `start_index` or `end_index` exceeds the string length → runtime error.
- If `end_index` < `start_index` → runtime error.

CANONICAL_EXAMPLES:
```deluge
sourceText = "Welcome to Zoho Deluge";
newText = sourceText.subString(11, 22);  // returns "Zoho Deluge" (chars 11–21)

Email_Data = "Email: jack@zylker.com";
Email = Email_Data.subString(7);         // returns "jack@zylker.com" (index 7 to end)

product_name = "Zoho Deluge";
result = product_name.subText(0, 4);     // returns "Zoho" (end_index 4 excluded)
result = product_name.subText(5, -12);   // returns "Deluge" (negative end ignored)
result = product_name.subText(6, 4);     // throws error (end < start)
```

FAILURE_MODES:
- `start_index` or `end_index` exceeding the string length throws a runtime error.
- `end_index` < `start_index` throws a runtime error.
- `start_index` == `end_index` returns empty text (not an error).

RELATED_DOCS:
- mid — mid.dou.md
- left — left.dou.md
- right — right.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/string/substring.html, https://www.zoho.com/deluge/help/functions/string/subtext.html
