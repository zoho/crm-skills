FILE_PURPOSE: Deluge `indexOf()` / `lastIndexOf()` — find first or last index of element in a LIST.

MENTAL_MODEL: `list.indexOf(el)` = first 0-based index of el; -1 if absent. `lastIndexOf` = last occurrence.

WHEN_TO_USE:
- Finding the position of an element within a LIST
- Checking existence by testing for index != -1

WHEN_NOT_TO_USE:
- Need boolean membership test → use contains() / notContains()
- Need to retrieve element by position → use get()

TRIGGER_KEYWORDS: indexOf(), lastIndexOf(), 0-based-list-index, not-found-returns-minus-1, first-vs-last-occurrence

RULES:
1. Return type: NUMBER. Index is 0-based (first element = 0).
2. Returns -1 if searchElement is not found.
3. indexOf() returns the FIRST occurrence index; lastIndexOf() returns the LAST occurrence index.
4. Input: LIST (listVariable), any data type (searchElement).

CANONICAL_EXAMPLES:
```deluge
listVar = {"Leads", "Contacts", "Deals"};
firstIndex = listVar.indexOf("Leads");     // → 0
lastIndex  = listVar.lastIndexOf("Leads"); // → 0 (appears only once)
missing    = listVar.indexOf("Books");       // → -1 (not found)
```

FAILURE_MODES:
- searchElement not found → returns -1 (no error raised)
- Existence guard: test for != -1, NOT for > 0 — index 0 is a valid position

RELATED_DOCS:
- contains() — list-contains.dou.md
- get() — list-get-size-clear.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

SOURCE:
https://www.zoho.com/deluge/help/functions/list/indexof.html, https://www.zoho.com/deluge/help/functions/list/lastindexof.html
