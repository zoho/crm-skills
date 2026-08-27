## FILE_PURPOSE
Deluge map containKey() containValue() notContains() — membership test for keys and values.

## MENTAL_MODEL
containKey/containValue = BOOLEAN key/value exists (case-sensitive); notContains = inverse membership.

## WHEN_TO_USE
- Check if a specific key exists in a map (containKey()).
- Check if a specific value exists in a map (containValue()).
- Check if a key (or substring/element) is ABSENT from a map, list, text, or collection (notContains()).

## WHEN_NOT_TO_USE
- Retrieving the value for a key — use get() instead.
- Case-insensitive membership check — all three functions are strictly case-sensitive.

## TRIGGER_KEYWORDS
map.containKey, map.containValue, map.notContains, key exists in map, value exists in map, case sensitive key check

## RULES
- containKey() syntax: `<variable> = <mapVariable>.containKey(<searchkey>);` — returns BOOLEAN.
  - searchkey type: TEXT.
- containValue() syntax: `<variable> = <mapVariable>.containValue(<searchValue>);` — returns BOOLEAN.
  - searchValue type: TEXT.
- notContains() syntax: `<variable> = <inputValue>.notContains(<searchValue>);` — returns BOOLEAN.
  - inputValue type: TEXT/LIST/MAP/COLLECTION; searchValue: any datatype.
- All three functions perform case-sensitive searches.
- notContains() returns true if searchValue is NOT present, false if it is.
- notContains() on MAP: checks for KEY presence (not value) — behaves as inverse of containKey().
- notContains() on TEXT: checks for substring absence.
- notContains() on LIST: checks for element absence.

## CANONICAL_EXAMPLES
```deluge
// containKey() — case-sensitive key check
mapVar     = {"Product": "CRM", "Company": "Zoho"};
boolVal    = mapVar.containKey("product");   // false — lowercase mismatch
newBoolVal = mapVar.containKey("Product");  // true

// containValue() — case-sensitive value check
boolVal    = mapVar.containValue("creator"); // false — lowercase mismatch
newBoolVal = mapVar.containValue("CRM"); // true

// notContains() on MAP — checks KEY absence
product_details = Map();
product_details.put("product", "CRM");
product_details.put("subscription", "yearly");
boolVal = product_details.notContains("price");        // true  — key absent
boolVal = product_details.notContains("subscription"); // false — key exists

// notContains() on TEXT — substring absence
products = "Zoho CRM";
boolVal  = products.notContains("CRM");  // false — substring found
boolVal  = products.notContains("CREATOR");  // true  — case mismatch
```

## FAILURE_MODES
- containKey()/containValue(): case mismatch → returns false (no error).
- notContains() on MAP: checks KEYS only — cannot detect value absence.

## RELATED_DOCS
- get — ../../datatypes/key-value.dou.md
- Map functions — https://www.zoho.com/deluge/help/functions/key-value.html

## SOURCE
https://www.zoho.com/deluge/help/functions/map/containkey.html, https://www.zoho.com/deluge/help/functions/map/containvalue.html, https://www.zoho.com/deluge/help/functions/string/notcontains.html
