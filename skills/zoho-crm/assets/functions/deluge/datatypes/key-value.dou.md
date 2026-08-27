FILE_PURPOSE: Deluge Key-Value datatype — dictionary map of unique-keyed values
MENTAL_MODEL: Key-Value = typed dictionary; keyed by any Deluge type; duplicate key silently overwrites existing value

WHEN_TO_USE:
- Store and retrieve values by unique named key.
- Merge two maps with putAll.
- Check key/value existence before conditional operations.

WHEN_NOT_TO_USE:
- Ordered integer-indexed access — use List.
- Ordered iteration with positional access — use Collection (index-value mode).

TRIGGER_KEYWORDS:
map.put, map.get, map.putAll, containKey, containValue, map.keys, map.size, key-value map

RULES:
- Keys must be unique; inserting a duplicate key silently overwrites the existing value with no error.
- Both keys and values can be of any Deluge data type.
- `get()` returns null when the key does not exist; use `containKey()` before relying on `get()`.
- `keys()` returns a List of all keys; `size()` returns count of key-value pairs.

CANONICAL_EXAMPLES:
```deluge
ZohoProduct = {"Product":"CRM", "Version":8};
ZohoProduct.put("Status", "Active");           // insert/overwrite
ver        = ZohoProduct.get("Version");         // 5
ZohoProduct.putAll(other_map);                   // merge all pairs
has_key    = ZohoProduct.containKey("Product");  // true
has_active = ZohoProduct.containValue("Active"); // true
all_keys   = ZohoProduct.keys();                  // List of keys
size       = ZohoProduct.size();                  // count of pairs
```

FAILURE_MODES:
- Duplicate key insert silently overwrites; validate with `containKey()` before conditional puts.
- `put()` (Key-Value) and `add()` (List) are not interchangeable; type error when misapplied.
- `put()` and Collection `insert()` are not interchangeable.
- `putAll()` silently overwrites existing keys on collision — no error.
- `get()` returns null for missing key — no error; always check `containKey()` first.

RELATED_DOCS:
- Key-Value built-in functions — https://www.zoho.com/deluge/help/datatypes/key-value.html
- get() — https://www.zoho.com/deluge/help/datatypes/key-value.html

SOURCE:
https://www.zoho.com/deluge/help/datatypes/key-value.html, https://www.zoho.com/deluge/help/functions/map/get.html
