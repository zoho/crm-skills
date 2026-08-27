FILE_PURPOSE: Deluge `toJSONList()` — convert a JSON-formatted TEXT array into a Deluge LIST.
MENTAL_MODEL: `jsonText.toJSONList()` = LIST; input must be a valid JSON array string; each element is accessible via `getJSON()`.

WHEN_TO_USE:
- Parse a JSON array response (e.g., from `getJSON()` on an API result) into a Deluge LIST for iteration.
- Extract nested objects from a JSON response array, then iterate with `for each` to access fields.

WHEN_NOT_TO_USE:
- When the TEXT is not in valid JSON array format — throws a runtime error.
- When the text is a comma-separated non-JSON string — use `toListString()` instead.

TRIGGER_KEYWORDS:
toJSONList, getJSON toJSONList, JSON-array parse, LIST from JSON, non-JSON runtime

RULES:
- Return type: LIST.
- Input type: TEXT (must be a valid JSON array string).
- Non-JSON text throws a runtime error.
- After conversion, call `getJSON("<key>")` on each list element to extract nested key-value pairs.

CANONICAL_EXAMPLES:
```deluge
// Extract a simple value array from a JSON string
json_text = "{Name:'Lia Shelton', OrderNo:[343,443,577]}";
orderNo = json_text.getJSON("OrderNo");
info orderNo.toJSONList();   // Returns 343,443,577

// Iterate a JSON array of objects to collect IDs
response = "{\"data\" : [{\"id\":1, \"firstname\":\"John\"}, {\"id\":2, \"firstname\":\"Patricia\"}]}";
data = response.getJSON("data");
json_list = data.toJSONList();
id_list = List();
for each item in json_list {
  id_list.add(item.getJSON("id"));
}
info id_list;  // Returns 1,2
```

FAILURE_MODES:
- Input TEXT not in valid JSON format throws a runtime error.

RELATED_DOCS:
- getJSON — ../../deluge-tasks/xml-manipulation/../../deluge-tasks/xml-manipulation/executeXpath.dou.md
- List functions — ../../datatypes/list.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/common/tojsonlist.html
