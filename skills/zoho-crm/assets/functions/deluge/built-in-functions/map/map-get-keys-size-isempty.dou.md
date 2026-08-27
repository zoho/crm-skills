## FILE_PURPOSE
Deluge map get() keys() size() isEmpty() — read access and state inspection.

## MENTAL_MODEL
get(key)=value|null; keys()=LIST of all keys; size()=pair count; isEmpty()=BOOLEAN empty check.

## WHEN_TO_USE
- Retrieve the value mapped to a known key (get()).
- Get all keys from a map as a list for iteration (keys()).
- Count the number of key-value pairs in a map (size()).
- Check whether a map, list, text, or collection has no elements (isEmpty()).

## WHEN_NOT_TO_USE
- Checking whether a specific key exists — use containKey() instead.
- Mutating the map — use put(), remove(), or clear() instead.

## TRIGGER_KEYWORDS
map.get, map.keys, map.size, map.isEmpty, retrieve map value, list map keys, null if key absent

## RULES
- get() syntax: `<variable> = <mapVariable>.get(<searchkey>);` — return type matches value's data type.
- keys() syntax: `<variable> = <mapVariable>.keys();` — returns LIST.
- size() syntax: `<variable> = <mapVariable>.size();` — returns NUMBER (count of key-value pairs).
- isEmpty() syntax: `<variable> = <expression>.isEmpty();` — returns BOOLEAN; accepts TEXT/LIST/MAP/COLLECTION.
- get(): if the key is not found → returns null (no error).
- keys(): map keys can be TEXT, NUMBER, or LIST; all are returned as elements in the resulting list.
- isEmpty(): a text value containing only spaces (e.g. `" "`) → returns false (spaces ≠ empty).
- isEmpty() is distinct from isBlank() and isNull() — refer to differences doc for each behavior.

## CANONICAL_EXAMPLES
```deluge
// get() — key not found returns null
mapVar     = {"Product": "CRM", "Company": "Zoho"};
boolVal    = mapVar.get("Module");     // returns null (not a key)
newBoolVal = mapVar.get("Product");   // returns "CRM"

// keys() — all keys returned as a list
mapVar  = {"Product": "Zoho CRM", "Version": 8};
listVar = mapVar.keys();              // returns {Product, Version}

// size()
size = mapVar.size();                 // returns 2

// isEmpty() — empty map, empty collection, but NOT space-string
mapVar  = {};
info mapVar.isEmpty();                // returns true

textVar = " ";
info textVar.isEmpty();               // returns false (space is not empty)
```

## FAILURE_MODES
- get(): key not found → returns null; using null in arithmetic or string operations causes downstream errors.
- isEmpty(): whitespace-only string → returns false (use isBlank() to catch whitespace-only strings).

## RELATED_DOCS
- containKey — map-containkey-containvalue-notcontains.dou.md
- isBlank/isNull/isEmpty differences — https://www.zoho.com/deluge/help/functions/common/isnull-isblank-isempty-difference.html
- Map functions — https://www.zoho.com/deluge/help/functions/key-value.html

## SOURCE
https://www.zoho.com/deluge/help/functions/map/get.html, https://www.zoho.com/deluge/help/functions/map/keys.html, https://www.zoho.com/deluge/help/functions/map/size.html, https://www.zoho.com/deluge/help/functions/text/is-empty.html
