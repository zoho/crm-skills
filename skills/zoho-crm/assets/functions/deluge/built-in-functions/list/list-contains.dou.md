## FILE_PURPOSE
Deluge list contains() — exact membership test for a list element.

## MENTAL_MODEL
list.contains(el) = BOOLEAN true only on exact case-sensitive type-sensitive whole-element match.

## WHEN_TO_USE
- Check whether a specific value exists as an element in a list (exact match, case-sensitive).

## WHEN_NOT_TO_USE
- Case-insensitive membership check — contains() is strictly case-sensitive.
- Searching for a map key within a nested map element — contains() matches the entire element, not a key inside it.
- Partial list match — contains() does not match a subset of a nested list element.

## TRIGGER_KEYWORDS
list.contains, list membership check, element in list boolean, exact match list, case sensitive contains

## RULES
- Syntax: `<variable> = <listVariable>.contains(<searchElement>);`
- Returns BOOLEAN: true if searchElement is found as an element, false otherwise.
- searchElement accepts ALL DATA TYPES.
- Match is exact: case-sensitive AND type-sensitive.
  - String `"1"` does NOT match number `1` in the list.
  - String `"zoho"` does NOT match `"Zoho"` (case mismatch).
- Map key is NOT the same as the whole map element.
  - `"version"` does NOT match element `{"version":5}`.
  - `{"Version":5}` does NOT match `{"version":5}` (case mismatch on key).
- Partial list is NOT matched against a full nested list element.
  - `{"India"}` does NOT match element `{"India", "USA", "Australia"}`.

## CANONICAL_EXAMPLES
```deluge
listVar = {1, "2", "Zoho", "CRM", {"version":8}, {"India", "USA", "Australia"}};

a = listVar.contains("1");             // false — type mismatch (string vs number 1)
b = listVar.contains(2);              // false — type mismatch (number vs string "2")
c = listVar.contains("zoho");         // false — case mismatch ("zoho" vs "Zoho")
d = listVar.contains("CRM");      // true  — exact match
e = listVar.contains("version");      // false — map key ≠ whole element
f = listVar.contains({"Version": 5}); // false — case mismatch on map key
g = listVar.contains({"India"});      // false — partial list ≠ full list element
```

## FAILURE_MODES
- Type mismatch (string vs number for same value) → returns false.
- Case mismatch on string values or map keys → returns false.
- Searching for a map key instead of the full map element → returns false.
- Searching for a partial list instead of the full nested list element → returns false.

## RELATED_DOCS
- indexOf — list-indexOf-lastIndexOf.dou.md
- notContains (text) — list-notContains-isEmpty.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

## SOURCE
https://www.zoho.com/deluge/help/functions/list/contains.html
