FILE_PURPOSE: Deluge remove() — remove all occurrences of a substring from a string
MENTAL_MODEL: remove(string, search) = TEXT; removes ALL occurrences of search; unchanged if absent; case-sensitive

WHEN_TO_USE:
- Remove every occurrence of a known substring from a text value.
- Sanitize strings by stripping unwanted tokens.

WHEN_NOT_TO_USE:
- Removing only the first occurrence — use `removeFirstOccurence()` instead.
- Removing only the last occurrence — use `removeLastOccurence()` instead.

TRIGGER_KEYWORDS:
remove, string.remove, remove all occurrences, case-sensitive remove, searchString remove

RULES:
- Two syntaxes: `<variable> = <string>.remove(<searchString>);` and `remove(<string>, <searchString>)`.
- Return type: TEXT.
- Removes ALL occurrences of `<searchString>` from `<string>`.
- If `<searchString>` is not found, returns the original string unchanged.
- Performs a case-sensitive search.
- Both `<string>` and `<searchString>` must be TEXT.

CANONICAL_EXAMPLES:
```deluge
Product = "Zoho CRM";
newText = Product.remove("CRM"); // returns "Zoho "
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- removeFirstOccurence — remove-first-occurence.dou.md
- removeLastOccurence — remove-last-occurence.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/remove.html
