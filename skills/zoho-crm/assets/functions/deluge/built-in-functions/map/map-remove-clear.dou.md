## FILE_PURPOSE
Deluge map remove() and clear() — delete a key-value pair or empty the entire map.

## MENTAL_MODEL
remove(key) deletes one pair silently if key absent; clear() removes all pairs in place.

## WHEN_TO_USE
- Remove a specific key-value pair from a map by its key.
- Remove all key-value pairs from a map at once.

## WHEN_NOT_TO_USE
- Adding or updating pairs — use put() or putAll() instead.
- Checking key existence before removal — use containKey() first if presence confirmation is needed.

## TRIGGER_KEYWORDS
map.remove, map.clear, delete key-value pair, empty map, remove map entry

## RULES
- remove() syntax: `<mapVariable>.remove(<key>);` — no return value; mutates mapVariable in place.
- clear() syntax: `<mapVariable>.clear();` — no return value; empties the map in place.
- remove(): if the specified key is not found, mapVariable is returned as-is — no error thrown.
- clear(): removes all key-value pairs; the map variable remains but is empty.

## CANONICAL_EXAMPLES
```deluge
// remove() — removes the specified key-value pair
details = {"Company": "Zoho", "Product": "CRM", "Version": 8};
details.remove("Version");
// details is now {"Company": "Zoho", "Product": "CRM"}

// remove() — key not found → map unchanged, no error
details.remove("NonExistentKey");
// details unchanged

// clear() — empties the entire map
mapVar = {"Product": "CRM", "Version": 8};
mapVar.clear();
// mapVar is now {}
```

## FAILURE_MODES
- remove(): key not found → map returned unchanged, no error thrown (silent no-op).

## RELATED_DOCS
- put — map-put-putall.dou.md
- containKey — map-containkey-containvalue-notcontains.dou.md
- Map functions — https://www.zoho.com/deluge/help/functions/key-value.html

## SOURCE
https://www.zoho.com/deluge/help/functions/map/remove.html, https://www.zoho.com/deluge/help/functions/map/clear.html
