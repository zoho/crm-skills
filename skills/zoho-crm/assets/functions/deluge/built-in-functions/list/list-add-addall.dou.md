## FILE_PURPOSE
Deluge list add() and addAll() — append element(s) to a list in place.

## MENTAL_MODEL
add(el) appends one element (list arg = nested); addAll(list2) spreads list2 into list1.

## WHEN_TO_USE
- Append a single element (including another list as a nested element) to an existing list.
- Append all elements from a second list individually into a first list (flat merge).

## WHEN_NOT_TO_USE
- Getting elements that appear in both lists — use intersect() instead.
- Extracting a slice of a list — use subList() instead.

## TRIGGER_KEYWORDS
list.add, list.addAll, append element list, merge lists, nested list element

## RULES
- add() syntax: `<listVariable>.add(<addElement>);` — no return value; mutates listVariable in place.
- addAll() syntax: `<listVariableOne>.addAll(<listVariableTwo>);` — no return value; mutates listVariableOne in place.
- add(): if addElement is a list, it is added as a single nested element (not spread).
  - `list.add({"CRM", "Projects"})` → `{"Leads", {"Contacts", "Deals"}}`, not `{"Leads", "Contacts", "Deals"}`.
- addAll(): all elements of listVariableTwo are individually appended to listVariableOne.
- Mixed data types are allowed if the list is not restricted to a specific data type.
- Neither add() nor addAll() has a return value.

## CANONICAL_EXAMPLES
```deluge
// add() — list arg becomes a single nested element
Products = List();
Products.add("Leads");
Products.add({"CRM", "Projects"});
// Products is now {"Leads", {"Contacts", "Deals"}}

// addAll() — spreads all elements from the second list
listOne = {"Leads"};
listTwo = {"CRM", "Projects"};
listOne.addAll(listTwo);
// listOne is now {"Leads", "Contacts", "Deals"}
```

## FAILURE_MODES
*(none in source)*

## RELATED_DOCS
- addAll — https://www.zoho.com/deluge/help/functions/list/add.html
- intersect — list-intersect-sublist.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

## SOURCE
https://www.zoho.com/deluge/help/functions/list/add.html, https://www.zoho.com/deluge/help/functions/list/addall.html
