FILE_PURPOSE: Deluge `getOccurenceCount()` — count occurrences of a substring within a text string.
MENTAL_MODEL: `str.getOccurenceCount(sub)` = NUMBER; counts all occurrences of `sub` in `str`; case-sensitive.

WHEN_TO_USE:
- Count how many times a specific substring appears in a text string.

WHEN_NOT_TO_USE:
- When only checking presence (not count) — use `contains()` instead.

TRIGGER_KEYWORDS:
getOccurenceCount(), occurrence count, case-sensitive count, searchString frequency, substring tally

RULES:
- Return type: NUMBER.
- Input types: TEXT (string), TEXT (searchString).
- Performs a case-sensitive search.
- Both `.getOccurenceCount(searchString)` and `getOccurenceCount(string, searchString)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
text = "Zoho CRM, a customer relationship platform, helps you manage customer data effectively";
count = text.getOccurenceCount("database");  // returns 2
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/getOccurenceCount.html
