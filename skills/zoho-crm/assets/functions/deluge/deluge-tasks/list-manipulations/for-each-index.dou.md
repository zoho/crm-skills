FILE_PURPOSE: Deluge for-each-index loop — iterate over list element indices (0-based positions)
MENTAL_MODEL: for each index <var> in <list> = loop body executes once per index; var holds current 0-based index

WHEN_TO_USE:
- Iterate over list elements by their integer index positions.
- When both the index position and the element value are needed within the loop body.

WHEN_NOT_TO_USE:
- Iterating by element value without needing the index — use `for each element` instead.
- Iterating CSV files — only `for each element` supports CSV; `for each index` is List-only.

TRIGGER_KEYWORDS:
for each index, for each index in list, index-based iteration, loop variable index, list.get by index

RULES:
- Syntax: `for each index <loop_variable> in <list_variable>;`
- `<loop_variable>` holds the current 0-based integer index on each iteration.
- Only List data type is supported (not CSV file).
- `<loop_variable>` needs no prior declaration.
- After iteration completes, `<loop_variable>` holds the index of the last element.
- Retrieve element at each index using `<list_variable>.get(<loop_variable>)`.

CANONICAL_EXAMPLES:
```deluge
colorList = {"red", "green", "blue"};
for each index colorIndex in colorList {
  info "(" + colorIndex + ")" + colorList.get(colorIndex);
}
// Output: (0)red  (1)green  (2)blue
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- For each element — for-each-element.dou.md

SOURCE:
https://www.zoho.com/deluge/help/list-manipulations/for-each-index.html
