FILE_PURPOSE: Deluge `notContains()` / `isEmpty()` — boolean membership absence and empty checks on TEXT/LIST/MAP.

MENTAL_MODEL: `notContains(val)` = !contains(); case-sensitive. `isEmpty()` = true if zero-length; whitespace TEXT is NOT empty.

WHEN_TO_USE:
- Verifying a value is absent from a TEXT, LIST, MAP, or COLLECTION → use notContains()
- Checking whether a list, collection, map, or text has zero elements/length → use isEmpty()

WHEN_NOT_TO_USE:
- Need to check presence → use contains()
- Need to guard for whitespace-only strings → use isBlank() (isEmpty returns false for " ")
- Need to guard for null → use isNull()

TRIGGER_KEYWORDS: notContains(), isEmpty(), case-sensitive-membership, boolean-collection-check, whitespace-not-empty

RULES:
1. notContains() return type: BOOLEAN. Input types: TEXT, LIST, MAP, or COLLECTION. searchValue: any data type.
2. notContains() is case-sensitive — "crm" does not match "CRM".
3. notContains() on MAP: checks KEY existence only — does NOT search values.
4. notContains() on key-value COLLECTION: checks KEY existence only.
5. notContains() on index-value COLLECTION and LIST: checks element values.
6. isEmpty() return type: BOOLEAN. Input: TEXT, LIST, MAP, or COLLECTION.
7. isEmpty() on TEXT: a whitespace-only string (e.g. " ") → false (whitespace is NOT empty).
8. isEmpty() on empty Collection() or empty map {} → true.

CANONICAL_EXAMPLES:
```deluge
// notContains on TEXT (substring search, case-sensitive)
"Zoho CRM".notContains("CRM"); // → false ("CRM" is a substring)
"Zoho CRM".notContains("crm"); // → true (case-sensitive mismatch)

// notContains on LIST (element membership)
products = {"Leads", "Contacts", "Deals"};
products.notContains("Books"); // → true

// notContains on MAP (checks KEYS, not values)
m = Map(); m.put("product", "CRM"); m.put("subscription", "yearly");
m.notContains("price"); // → true (key "price" is absent)

// isEmpty
{"Projects", "Mail"}.isEmpty(); // → false
Collection().isEmpty();          // → true (empty collection)
" ".isEmpty();                   // → false (whitespace is NOT empty)
```

FAILURE_MODES:
- notContains() on MAP or key-value COLLECTION checks keys only — does NOT scan values
- isEmpty(" ") → false; use isBlank() to detect whitespace-only strings
- Confusing isEmpty with isNull or isBlank — three distinct functions with different semantics

RELATED_DOCS:
- contains() — list-contains.dou.md
- isBlank() / isNull() / isEmpty() differences — https://www.zoho.com/deluge/help/functions/common/isnull-isblank-isempty-difference.html
- Functions returning boolean — https://www.zoho.com/deluge/help/functions-returning-boolean.html
- Text functions — https://www.zoho.com/deluge/help/functions/text.html
- List functions — https://www.zoho.com/deluge/help/functions/list.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/notcontains.html, https://www.zoho.com/deluge/help/functions/text/is-empty.html
