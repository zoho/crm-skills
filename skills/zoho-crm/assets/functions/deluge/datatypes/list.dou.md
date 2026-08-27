FILE_PURPOSE: Deluge List datatype — ordered zero-indexed heterogeneous element sequence
MENTAL_MODEL: List = zero-indexed ordered array; mixed types allowed; grows via add/addAll; addAll capped at 25,000

WHEN_TO_USE:
- Store ordered sequences addressable by integer index.
- Perform set operations: intersect two lists, sort, remove by index.
- Iterate ordered results from CRM API responses.

WHEN_NOT_TO_USE:
- Named (keyed) access — use Key-Value or Collection (key-value mode).
- Batches > 25,000 elements added in one addAll call — split into multiple adds.

TRIGGER_KEYWORDS:
list.add, list.addAll, list.contains, list.indexOf, list.sublist, list.intersect, list.sort, addAll 25000

RULES:
- First element index is 0; last is n-1.
- Elements of different Deluge data types are permitted in the same List.
- `addAll` hard cap: 25,000 elements per call.
- `add` built-in: no per-call limit (adds one element at a time).
- Direct declaration (curly-brace literal): no element limit.

CANONICAL_EXAMPLES:
```deluge
ZohoProducts = {"Leads", "Contacts", "Deals"};
found   = ZohoProducts.contains("Contacts");     // true
element = ZohoProducts.get(0);                   // "Leads"
pos     = ZohoProducts.indexOf("Deals");         // 2
sub     = ZohoProducts.sublist(1, 3);            // ["Contacts","Deals"]
common  = listA.intersect(listB);               // shared elements
sorted  = ZohoProducts.sort();
ZohoProducts.remove(1);                          // removes at index 1
```

FAILURE_MODES:
- `addAll` exceeds 25,000 elements per call — error; batch large datasets.
- Accessing index outside bounds (negative or >= List size) throws an error.
- Applying Key-Value `put()` or Collection `insert()` on a List variable — type error.

RELATED_DOCS:
- List built-in functions — https://www.zoho.com/deluge/help/datatypes/list.html
- add / addAll — ../built-in-functions/list/list-add-addall.dou.md

SOURCE:
https://www.zoho.com/deluge/help/datatypes/list.html
