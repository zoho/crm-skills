FILE_PURPOSE: Deluge `toListString()` — split a comma-separated TEXT or LIST into a LIST of TEXT elements.
MENTAL_MODEL: `"a,b,c".toListString()` = LIST of TEXT; all elements are TEXT regardless of original content type.

WHEN_TO_USE:
- Split a comma-delimited string (e.g., `"1,2,3,4,5"`) into a Deluge LIST where each element is TEXT.
- Convert a LIST into a LIST of TEXT elements for downstream string operations.

WHEN_NOT_TO_USE:
- When element type preservation is required (e.g., numeric elements should remain NUMBER) — use `toList()` instead.
- When the input is a JSON array string — use `toJSONList()` instead.

TRIGGER_KEYWORDS:
toListString, comma-separated to LIST, TEXT-element list, toList vs toListString, LIST-STRING split

RULES:
- Return type: LIST; all elements are of type TEXT.
- Input types: LIST, TEXT.
- All elements of the output list are TEXT regardless of the original input content.

CANONICAL_EXAMPLES:
```deluge
number_text = "1,2,3,4,5";
items = number_text.toListString();
// items is a LIST with TEXT elements: "1","2","3","4","5"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- toList — https://www.zoho.com/deluge/help/functions/list/to-list-string.html

SOURCE:
https://www.zoho.com/deluge/help/functions/list/to-list-string.html
