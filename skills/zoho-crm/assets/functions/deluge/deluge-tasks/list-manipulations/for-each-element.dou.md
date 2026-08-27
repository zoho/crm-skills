FILE_PURPOSE: Deluge for-each-element loop — iterate over list elements or CSV file rows
MENTAL_MODEL: for each <var> in <list|csv> {} = loop body executes once per element; var holds current element

WHEN_TO_USE:
- Iterate over all elements in a list.
- Process each row in a CSV file (up to 2 MB).

WHEN_NOT_TO_USE:
- Iterating by index position rather than element value — use `for each index` instead.

TRIGGER_KEYWORDS:
for each element, for each in list, CSV iteration, 2MB CSV limit, elementVariable last value

RULES:
- Syntax: `for each <elementVariable> in <variable> { }`
- `<variable>` supports List and CSV file types.
- CSV file size limit: 2 MB maximum.
- `<elementVariable>` needs no prior declaration.
- After iteration completes, `<elementVariable>` holds the last element value.

CANONICAL_EXAMPLES:
```deluge
numbers = {"One", "Two", "Three"};
for each item in numbers {
  info item;
}
// Output: One  Two  Three

// CSV iteration
csv_file_zip = invokeurl[url:"https://example.com/file.zip" type:GET];
csv_file = csv_file_zip.extract().get("file.csv");
for each val in csv_file {
  info val;
}
```

FAILURE_MODES:
- CSV file exceeds 2 MB → error.

RELATED_DOCS:
- For each index — for-each-index.dou.md
- Extract — ../../file-functions/extract.dou.md
- Send Mail — ../misc/../misc/send-mail.dou.md

SOURCE:
https://www.zoho.com/deluge/help/list-manipulations/for-each-element.html
