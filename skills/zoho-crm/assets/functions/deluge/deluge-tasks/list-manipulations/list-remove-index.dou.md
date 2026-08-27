FILE_PURPOSE: Deluge list.remove(index) — remove and return the element at a specified index
MENTAL_MODEL: list.remove(index) = removes element at 0-based index; returns removed element; errors on invalid index

WHEN_TO_USE:
- Remove a specific element by its position (index) in a list.
- Retrieve and remove an element simultaneously.

WHEN_NOT_TO_USE:
- Removing by element value rather than position — use `list.removeElement()` instead.

TRIGGER_KEYWORDS:
list.remove, remove by index, 0-based index removal, list index remove, remove returns element

RULES:
- Syntax: `<variable> = <list_variable>.remove(<index>);` (return variable is optional).
- Index is 0-based: first element is index 0, last is size−1.
- `<index>` must be a Number; negative values are not allowed.
- Returns the removed element.

CANONICAL_EXAMPLES:
```deluge
days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"};
days.remove(1);
// removes "Tuesday" (index 1)
// list becomes ["Monday", "Wednesday", "Thursday", "Friday"]
```

FAILURE_MODES:
- Negative index → runtime error.
- Index >= list size → runtime error.

RELATED_DOCS:
- Remove element — list-remove-element.dou.md

SOURCE:
https://www.zoho.com/deluge/help/list-manipulations/remove-index.html
