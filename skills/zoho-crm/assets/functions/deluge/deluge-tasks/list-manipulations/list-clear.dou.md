FILE_PURPOSE: Deluge list.clear() — permanently remove all elements from a list
MENTAL_MODEL: list.clear() = empties the list in place; all elements permanently removed; no return value

WHEN_TO_USE:
- Reset a list to empty within a script without creating a new list variable.
- Remove stale data from a list before repopulating it in the same script execution.

WHEN_NOT_TO_USE:
- When individual element removal is needed — use `remove()` or `removeElement()`.

TRIGGER_KEYWORDS:
list.clear, clear list, empty list, list reset, clear all elements

RULES:
- Syntax: `<list_variable>.clear();`
- Permanently removes all elements from the specified list.

CANONICAL_EXAMPLES:
```deluge
alldays = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"};
alldays.clear();
// alldays is now an empty list []
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
*(none in source)*

SOURCE:
https://www.zoho.com/deluge/help/list-manipulations/clear.html
