FILE_PURPOSE: Deluge removeLastOccurence() — remove only the last matching substring occurrence
MENTAL_MODEL: removeLastOccurence(string, search) = TEXT; removes last match only; unchanged if absent; case-sensitive

WHEN_TO_USE:
- Remove only the last occurrence of a substring when earlier occurrences should be preserved.

WHEN_NOT_TO_USE:
- Removing all occurrences — use `remove()` instead.
- Removing only the first occurrence — use `removeFirstOccurence()` instead.

TRIGGER_KEYWORDS:
removeLastOccurence, string.removeLastOccurence, last occurrence removal, case-sensitive last, remove last match

RULES:
- Two syntaxes: `<variable> = <string>.removeLastOccurence(<searchString>);` and `removeLastOccurence(<string>, <searchString>)`.
- Return type: TEXT.
- Removes only the LAST occurrence of `<searchString>` from `<string>`.
- If `<searchString>` is not found, returns the original string unchanged.
- Performs a case-sensitive search.
- Both `<string>` and `<searchString>` must be TEXT.

CANONICAL_EXAMPLES:
```deluge
Product = "Manage leads using Zoho CRM lead module";
newText = Product.removeLastOccurence("app");
// returns "Manage leads using Zoho CRM  module"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- removeFirstOccurence — remove-first-occurence.dou.md
- remove — remove.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/removelastoccurence.html
