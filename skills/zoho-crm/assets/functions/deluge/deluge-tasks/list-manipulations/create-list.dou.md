FILE_PURPOSE: Deluge List() — declare an empty or pre-populated heterogeneous list variable
MENTAL_MODEL: List() = ordered, zero-indexed, mutable collection; mixed data types allowed unless type-restricted

WHEN_TO_USE:
- Create a list to hold multiple values of potentially different data types.
- Initialize a list variable before adding elements with `.add()`.

WHEN_NOT_TO_USE:
- When elements must be constrained to a single data type — use `List:String()`, `List:Int()`, etc.

TRIGGER_KEYWORDS:
List(), list literal, list curly brackets, list initialization, mixed-type list

RULES:
- Three declaration forms:
  - `<variable> = List();` — empty list.
  - `<variable> = List(<value>);` — accepts only Text or List as `<value>`.
  - `<variable> = {<e1>, <e2>, ...};` — literal form; brackets `{}` or `[]` both accepted.
- Text value with commas in `List(<value>)`: words on either side of each comma become individual list elements.
- Mixed data types coexist in the same list unless it is a typed list.

CANONICAL_EXAMPLES:
```deluge
colors = {"red", "blue", "green"};   // literal list

listVar = List();
listVar.add(1);
listVar.add("Harry");                // mixed types: integer + string
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- List datatype — ../../datatypes/list.dou.md
- Create list of specific data type — create-list-typed.dou.md

SOURCE:
https://www.zoho.com/deluge/help/list-manipulations/create-list.html
