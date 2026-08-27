FILE_PURPOSE: Deluge map-manipulation tasks — create, insert, merge, delete, and clear map entries.
MENTAL_MODEL: Map() = Deluge Key-Value container; insert pairs with put()/putAll(); delete with remove()/clear().

WHEN_TO_USE:
- Build structured key-value containers for API payloads, condition checks, or dynamic data assembly.
- Merge two maps, delete specific entries by key, or reset a map to empty state.

WHEN_NOT_TO_USE:
*(none in source)* — all five tasks are supported in every Deluge workflow event and context.

TRIGGER_KEYWORDS:
Map(), .put(), .putAll(), .remove(), .clear(), key overwrite behavior, map merge putAll

RULES:
- Create empty map: `<var> = Map();`
- Create map with initial pairs: `<var> = {<key1>: <val1>, <key2>: <val2>};`
- Insert or update a single pair: `<map>.put(<key>, <value>);`
- Merge all pairs from map2 into map1: `<map1>.putAll(<map2>);`
- Remove one key and its value: `<map>.remove(<key>);` — if key is not found, no error is raised.
- Empty the entire map permanently: `<map>.clear();`
- Keys must be unique; specifying an existing key in `Map()`, `put()`, or `putAll()` silently OVERWRITES the existing value — no duplicate entry is appended.
- Keys and values can be of any Deluge data type.
- Date keys or values specified without a time component default to `00:00:00` as the time value.

CANONICAL_EXAMPLES:
```deluge
// Create map inline
mapVal = {"Product": "Zoho CRM", "Version": 8};

// Create map with list as value
mapVal = {"Products": {"Zoho CRM", "Zoho Cliq", "Zoho Books"}};

// Create empty map then insert entries
companyDetails = map();
companyDetails.put("Name", "Zoho");
companyDetails.put("Team", {"Zoho CRM", "Zoho Cliq", "Zoho Books"});

// Merge map2 into map1
city_list1 = {"Anchorage": "99501", "Phoenix": "85001"};
city_list2 = {"Little Rock": "72201", "Beverly Hills": "90213"};
city_list1.putAll(city_list2);
// city_list1 now contains all four entries

// Remove a specific key
details = {"Company": "Zoho", "Product": "CRM", "Version": 8};
details.remove("Version");
// details is now {"Company": "Zoho", "Product": "CRM"}

// Clear all entries
Company_details.clear();
```

FAILURE_MODES:
- Inserting a key that already exists silently overwrites the existing value — no error, no second entry with the same key.
- `putAll()` on overlapping keys in map2 silently overwrites those keys in map1 — no merge warning.
- `remove()` on a key that does not exist silently does nothing — no error is raised.
- `clear()` permanently removes all key-value pairs from the variable; there is no undo within the same script.

RELATED_DOCS:
- Key-Value data type — ../../datatypes/key-value.dou.md
- Map Manipulations overview — https://www.zoho.com/deluge/help/map-manipulations/create-map.html

SOURCE:
https://www.zoho.com/deluge/help/map-manipulations/create-map.html, https://www.zoho.com/deluge/help/map-manipulations/put.html, https://www.zoho.com/deluge/help/map-manipulations/put-all-keys.html, https://www.zoho.com/deluge/help/map-manipulations/remove-key.html, https://www.zoho.com/deluge/help/map-manipulations/clear-map.html
