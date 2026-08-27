FILE_PURPOSE: Deluge list.removeElement() — remove the first matching element by value
MENTAL_MODEL: list.removeElement(value) = removes first matching element by value; silent if not found; typed-list mismatch errors

WHEN_TO_USE:
- Remove a specific element from a list by its value (not position).

WHEN_NOT_TO_USE:
- Removing by index position — use `list.remove(index)` instead.

TRIGGER_KEYWORDS:
list.removeElement, removeElement, remove by value, silent not-found, typed list mismatch

RULES:
- Syntax: `<list_variable>.removeElement(<expression>);`
- Element not found in list → no error; list is unchanged (silent no-op).
- For type-specific lists: the data type of `<expression>` must match the list's declared type; mismatch causes a runtime error.
- All data types are applicable for `<expression>`.

CANONICAL_EXAMPLES:
```deluge
days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"};
days.removeElement("Tuesday");
// list becomes ["Monday", "Wednesday", "Thursday", "Friday"]

days.removeElement("Saturday");
// "Saturday" not found — no error, list unchanged
```

FAILURE_MODES:
- Removing from a typed list with a mismatched data type → runtime error.
- Element not found → silent no-op; no error raised.

RELATED_DOCS:
- Remove by index — list-remove-index.dou.md

SOURCE:
https://www.zoho.com/deluge/help/list-manipulations/remove-element.html
