FILE_PURPOSE: Deluge Collection datatype — ordered index-value or unordered key-value storage
MENTAL_MODEL: Collection = ordered list OR named map; two mutually exclusive modes addressed by integer index or string key

WHEN_TO_USE:
- Store a sequence addressable by position (index-value mode).
- Store named pairs addressable by unique key (key-value mode).
- Nest Collections inside Collections for hierarchical data structures.

WHEN_NOT_TO_USE:
- Only ordered integer-indexed access needed — use List (broader built-in method support).
- Only named-pair access with map-specific methods — use Key-Value.

TRIGGER_KEYWORDS:
Collection(), collection.insert(), collection.get(), index-value collection, key-value collection, for each, 50000 elements

RULES:
- Two mutually exclusive modes: index-value (ordered, 0-based integer index) OR key-value (unordered, unique string key).
- A single Collection variable cannot mix modes.
- Collection size limit: 50,000 elements.
- Keys in key-value mode must be unique; duplicate key silently overwrites existing value.
- First element of index-value Collection has index 0; last is n-1.
- `for each` iterates every element; no documented break-out mechanism in source.

CANONICAL_EXAMPLES:
```deluge
// Index-value Collection
gadgets = Collection("Mobile phone", "Laptop");
value   = gadgets.get(0);    // "Mobile phone"
gadgets.insert("Camera");    // appends

// Key-value Collection
details = Collection("Name":"Shawn", "Gender":"Male");
details.insert("Company":"Zoho");
name = details.get("Name"); // "Shawn"

// Iterate
sum  = 0;
nums = Collection(1, 2, 3);
for each v in nums { sum = sum + v; }
info sum; // 6
```

FAILURE_MODES:
- Accessing index >= Collection size or < 0 → error; validate bounds before indexed access.
- `insert()` is Collection-specific; using `put()` (Key-Value) or `add()` (List) on a Collection → type error.
- Duplicate key in key-value Collection silently overwrites; no error raised.
- Exceeding 50,000 elements → error.
- Mixing index-value and key-value `insert()` syntax on the same Collection → undefined behavior.

RELATED_DOCS:
- Collection built-in functions — https://www.zoho.com/deluge/help/datatypes/collection.html

SOURCE:
https://www.zoho.com/deluge/help/datatypes/collection.html
