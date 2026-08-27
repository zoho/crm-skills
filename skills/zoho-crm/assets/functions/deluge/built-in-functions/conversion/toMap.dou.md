FILE_PURPOSE: Deluge `toMap()` — convert a JSON-formatted TEXT string into a KEY-VALUE map.
MENTAL_MODEL: `jsonText.toMap()` = KEY-VALUE; input must be valid JSON; max 5 MB; non-JSON → runtime error.

WHEN_TO_USE:
- Parse a JSON object TEXT string (e.g., from an API response payload) into a Deluge KEY-VALUE map for `get()` / `put()` operations.

WHEN_NOT_TO_USE:
- When the TEXT is a JSON array — use `toJSONList()` instead.

TRIGGER_KEYWORDS:
toMap(), JSON-text parse, toMap 5MB limit, non-JSON runtime, JSON-to-map conversion

RULES:
- Return type: KEY-VALUE.
- Input type: TEXT (must be in JSON format).
- Syntax: `<json_text>.toMap()` (only one syntax form documented in source).
- Input TEXT must be valid JSON format; non-JSON throws a runtime error.
- Input TEXT size must be less than 5 MB.

CANONICAL_EXAMPLES:
```deluge
products = "{company:Zoho, product:CRM}";
info products.toMap();
// Returns {"product":"CRM","company":"Zoho"}
```

FAILURE_MODES:
- Non-JSON formatted TEXT input throws a runtime error.
- Input TEXT size ≥ 5 MB throws a runtime error.

RELATED_DOCS:
- toJSONList — toJSONList.dou.md
- Map functions — https://www.zoho.com/deluge/help/functions/key-value.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/tomap.html
