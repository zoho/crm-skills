## FILE_PURPOSE
Deluge list intersect() and subList() — get common elements or a slice of a list.

## MENTAL_MODEL
intersect(list2) = LIST of shared elements; subList(start, end) = LIST slice [start, end).

## WHEN_TO_USE
- Get the elements that appear in both of two lists (intersect()).
- Extract a contiguous range of elements from a list by index positions (subList()).

## WHEN_NOT_TO_USE
- Combining all elements from two lists — use addAll() instead.
- Retrieving a single element by index — use get() instead.

## TRIGGER_KEYWORDS
list.intersect, list.subList, common elements two lists, list slice, index range list

## RULES
- intersect() syntax: `<variable> = <listVariableOne>.intersect(<listVariableTwo>);`
- subList() syntax: `<variable> = <listVariable>.subList(<start_index>, <end_index>);`
- Both return LIST.
- subList(): index starts from 0.
- subList(): range is inclusive of start_index and exclusive of end_index — [start_index, end_index).
- subList(): if end_index is omitted → returns all elements from start_index to end of list.
- subList(): negative start_index → runtime error.
- subList(): end_index exceeds list size → runtime error.

## CANONICAL_EXAMPLES
```deluge
// intersect() — elements present in both lists
listOne    = {"Zoho Cliq", "Zoho CRM", "Zoho Projects"};
listTwo    = {"Zoho Mail", "Zoho Analytics", "Zoho Cliq"};
commonList = listOne.intersect(listTwo);  // returns {"Zoho Cliq"}

// subList() — [start_index inclusive, end_index exclusive)
listVar    = {1, 2, 3, 4};
newListVar = listVar.subList(0, 3);       // returns {1, 2, 3}  (index 0,1,2; index 3 excluded)
```

## FAILURE_MODES
- subList(): negative start_index → runtime error.
- subList(): end_index > list size → runtime error.

## RELATED_DOCS
- addAll — list-add-addall.dou.md
- get — list-get-size-clear.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

## SOURCE
https://www.zoho.com/deluge/help/functions/list/intersect.html, https://www.zoho.com/deluge/help/functions/list/sublist.html
