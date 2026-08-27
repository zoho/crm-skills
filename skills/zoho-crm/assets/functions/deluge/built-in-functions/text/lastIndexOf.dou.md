FILE_PURPOSE: Deluge `lastIndexOf()` — return the 0-based index of the LAST occurrence of a searchString.
MENTAL_MODEL: `str.lastIndexOf(sub)` = NUMBER; 0-based index of last occurrence of `sub`'s first char; -1 if not found; case-sensitive.

WHEN_TO_USE:
- Locate the position of the LAST occurrence of a character or substring within a text string.
- Complement `indexOf()` when the rearmost match is needed instead of the first.

WHEN_NOT_TO_USE:
- When the FIRST occurrence index is needed — use `indexOf()` / `find()` instead.
- When only boolean presence is needed — use `contains()` instead.

TRIGGER_KEYWORDS:
lastIndexOf(), last-occurrence index, zero-based lastIndexOf, -1 not found, case-sensitive lastindex

RULES:
- Return type: NUMBER.
- Input types: TEXT (string), TEXT (searchString).
- Index is 0-based (first character of string = index 0).
- Returns the index of the first character of searchString's LAST occurrence in the string.
- Returns `-1` if searchString is not found (no error is raised).
- Performs a case-sensitive search.
- Both `.lastIndexOf(searchString)` and `lastIndexOf(string, searchString)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
text = "Hello world, welcome to the universe";
lastIndex = text.lastIndexOf("e");  // returns 35
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- indexOf / find — find-indexOf.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/lastindexof.html
