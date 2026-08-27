## FILE_PURPOSE
Deluge map put() and putAll() — insert or merge key-value pairs in place.

## MENTAL_MODEL
put(k,v) inserts/overwrites one pair; putAll(map2) merges all pairs; duplicate keys overwrite value.

## WHEN_TO_USE
- Add a single key-value pair to an existing map.
- Merge all key-value pairs from a second map into a first map.

## WHEN_NOT_TO_USE
- Removing key-value pairs — use remove() or clear() instead.

## TRIGGER_KEYWORDS
map.put, map.putAll, insert key value pair, merge maps, duplicate key overwrite

## RULES
- put() syntax: `<mapVariable>.put(<key>, <value>);` — no return value; mutates mapVariable in place.
- putAll() syntax: `<mapVariableOne>.putAll(<mapVariableTwo>);` — no return value; mutates mapVariableOne in place.
- put(): duplicate key → new value OVERWRITES the existing value; no second entry is created.
- putAll(): duplicate key in mapVariableTwo → new value from mapVariableTwo OVERWRITES existing value in mapVariableOne.

## CANONICAL_EXAMPLES
```deluge
// put() — duplicate key "CRM" overwrites value (4 → 5)
Products = map();
Products.put("CRM", 7);
Products.put("CRM", 3);
Products.put("CRM", 8);   // map is now {"CRM": 8, "Deals": 3}

// putAll() — merges all pairs from mapTwo into mapOne
mapOne = {"Product": "CRM", "Version": 8};
mapTwo = {"Company": "Zoho", "Country": "India"};
mapOne.putAll(mapTwo);
// mapOne is now {"Product": "CRM", "Version": 8, "Company": "Zoho", "Country": "India"}
```

## FAILURE_MODES
- put(): duplicate key does not create a second entry — value is silently overwritten.
- putAll(): duplicate key from mapVariableTwo silently overwrites the existing value in mapVariableOne.

## RELATED_DOCS
- remove — map-remove-clear.dou.md
- Map functions — https://www.zoho.com/deluge/help/functions/key-value.html

## SOURCE
https://www.zoho.com/deluge/help/functions/map/put.html, https://www.zoho.com/deluge/help/functions/map/putAll.html
