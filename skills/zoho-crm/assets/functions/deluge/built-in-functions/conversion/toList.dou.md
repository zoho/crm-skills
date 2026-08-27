FILE_PURPOSE: Deluge `toList()` — split a TEXT string by a separator into a LIST.
MENTAL_MODEL: `text.toList(sep)` = LIST; tokenises text by separator; no-separator case returns single-element list.

WHEN_TO_USE:
- Split a delimited text string (e.g., slash-separated, comma-separated) into a LIST for iteration or indexing.

WHEN_NOT_TO_USE:
- When the input is a JSON array — use `toJSONList()` instead.
- When list elements must be TEXT type explicitly — use `toListString()` for comma-separated input.

TRIGGER_KEYWORDS:
toList, separator tokenise, toList separator, single-element list, consecutive-separator empty-element

RULES:
- Return type: LIST.
- Input types: TEXT (source_text), TEXT (separator).
- Syntax: `<source_text>.toList(<separator>)`.
- Text values punctuated by the separator become the list's elements.
- If separator is not provided or not found in source_text → entire source_text returned as a single-element list.
- If separators appear consecutively in source_text → empty string elements are created in the list at each consecutive position.

CANONICAL_EXAMPLES:
```deluge
products = "ZohoCRM/ZohoProjects";
productList = products.toList("/");
info productList;  // Returns ZohoCRM,ZohoProjects
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- toListString — toListString.dou.md
- toJSONList — toJSONList.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/tolist.html
