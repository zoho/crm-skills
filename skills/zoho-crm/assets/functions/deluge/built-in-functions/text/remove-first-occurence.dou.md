FILE_PURPOSE: Deluge removeFirstOccurence() — remove only the first matching substring occurrence
MENTAL_MODEL: removeFirstOccurence(string, search) = TEXT; removes first match only; unchanged if absent; case-sensitive

WHEN_TO_USE:
- Remove only the first occurrence of a substring when duplicates should be preserved.

WHEN_NOT_TO_USE:
- Removing all occurrences — use `remove()` instead.
- Removing only the last occurrence — use `removeLastOccurence()` instead.

TRIGGER_KEYWORDS:
removeFirstOccurence, string.removeFirstOccurence, first occurrence removal, case-sensitive first, remove first match

RULES:
- Two syntaxes: `<variable> = <string>.removeFirstOccurence(<searchString>);` and `removeFirstOccurence(<string>, <searchString>)`.
- Return type: TEXT.
- Removes only the FIRST occurrence of `<searchString>` from `<string>`.
- If `<searchString>` is not found, returns the original string unchanged.
- Performs a case-sensitive search.
- Both `<string>` and `<searchString>` must be TEXT.

CANONICAL_EXAMPLES:
```deluge
Product = "Zoho CRM v8";
newText = Product.removeFirstOccurence("v8"); // returns "Zoho CRM "
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- removeLastOccurence — remove-last-occurence.dou.md
- remove — remove.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/removefirstoccurence.html
