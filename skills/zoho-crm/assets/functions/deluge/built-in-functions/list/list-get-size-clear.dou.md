## FILE_PURPOSE
Deluge list get() size() clear() — index access, element count, and list emptying.

## MENTAL_MODEL
get(i) = element at index i (0-based); size() = element count; clear() empties the list.

## WHEN_TO_USE
- Retrieve a specific element from a list by its zero-based index position.
- Get the total number of elements in a list (including nested lists as single elements).
- Remove all elements from a list.

## WHEN_NOT_TO_USE
- Searching by value rather than position — use contains() or indexOf() instead.
- Extracting a range of elements — use subList() instead.

## TRIGGER_KEYWORDS
list.get, list.size, list.clear, list index access, count list elements, empty list

## RULES
- get() syntax: `<variable> = <listVariable>.get(<indexValue>);` — return type matches element's data type.
- size() syntax: `<variable> = <listVariable>.size();` — returns NUMBER.
- clear() syntax: `<listVariable>.clear();` — no return value; empties the list in place.
- Index starts from 0; valid range for get(): 0 to (size() - 1).
- get(): indexValue must not be negative → runtime error.
- get(): indexValue must not exceed list size → runtime error if it does.
- size(): a nested list counts as one element regardless of how many elements it contains.
- clear(): removes all elements; list variable remains but is empty.

## CANONICAL_EXAMPLES
```deluge
// get() — zero-based index; nested list at index 2 is one element
listVar      = {"Leads", "Contacts", {"Deals", "Tasks"}};
elementValue = listVar.get(2);   // returns {"Projects", "Reports"}

// size() — nested list {"Zoho Cliq", "Zoho CRM"} counts as 1
listVar       = {"Projects", "Mail", {"Zoho Cliq", "Zoho CRM"}};
countElements = listVar.size();  // returns 3

// clear()
listVar.clear();                 // listVar is now {}
```

## FAILURE_MODES
- get(): negative indexValue → runtime error.
- get(): indexValue ≥ list size → runtime error.

## RELATED_DOCS
- subList — list-intersect-sublist.dou.md
- contains — list-contains.dou.md
- indexOf — list-indexOf-lastIndexOf.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

## SOURCE
https://www.zoho.com/deluge/help/functions/list/get.html, https://www.zoho.com/deluge/help/functions/list/size.html, https://www.zoho.com/deluge/help/functions/list/clear.html
