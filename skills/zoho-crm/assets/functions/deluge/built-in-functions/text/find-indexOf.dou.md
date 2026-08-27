FILE_PURPOSE: Deluge `find()` / `indexOf()` — return the 0-based index of a searchString's first occurrence.
MENTAL_MODEL: `str.find(sub)` = NUMBER; 0-based index of `sub`'s first character in `str`; -1 if not found; case-sensitive.

WHEN_TO_USE:
- Locate the position of a character or substring within a text string.
- Determine whether a substring exists by checking if the returned index is ≥ 0 (found) or -1 (absent).

WHEN_NOT_TO_USE:
- When only boolean presence (not position) is needed — use `contains()` instead.
- When the last occurrence index is needed — use `lastIndexOf()` instead.

TRIGGER_KEYWORDS:
find(), indexOf(), first-occurrence index, zero-based index, -1 not found, case-sensitive find

RULES:
- Return type: NUMBER.
- Input types: TEXT (string), TEXT (searchString).
- `find()` and `indexOf()` are aliases; all four syntaxes are equivalent:
  `str.find(sub)`, `find(str, sub)`, `str.indexOf(sub)`, `indexOf(str, sub)`.
- Index is 0-based (first character of string = index 0).
- Returns the index of the FIRST character of `searchString`'s first occurrence in the string.
- Returns `-1` if `searchString` is not found (no error is raised).
- Search is case-sensitive.

CANONICAL_EXAMPLES:
```deluge
text = "Hello world, welcome to the universe";
firstIndex = text.find("e");     // returns 1 (first 'e' at index 1 in "Hello")
firstIndex = text.indexOf("e");  // returns 1 — indexOf is an alias of find
notFound   = text.find("z");     // returns -1 (not present)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- lastIndexOf — lastIndexOf.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/find.html, https://www.zoho.com/deluge/help/functions/string/indexof.html
