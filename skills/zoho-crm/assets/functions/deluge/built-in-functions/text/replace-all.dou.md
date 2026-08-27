FILE_PURPOSE: Deluge replaceAll() — replace all occurrences of a substring in a string
MENTAL_MODEL: replaceAll(string, search, replacement, regexEscape) = TEXT; replaces all matches; supports regex by default

WHEN_TO_USE:
- Replace every occurrence of a substring or regex pattern in a string.
- Use with `boolean=true` when the search string contains regex special characters that should be treated as literals.

WHEN_NOT_TO_USE:
- Replacing only the first occurrence — use `replaceFirst()` instead.

TRIGGER_KEYWORDS:
replaceAll, string.replaceAll, regex escape boolean, replaceAll case-sensitive, all occurrences replace, replacementString

RULES:
- Two syntaxes: `<variable> = <string>.replaceAll(<searchString>, <replacementString>, <boolean>);` and `replaceAll(<string>, <searchString>, <replacementString>, <boolean>)`.
- Return type: TEXT.
- Replaces ALL occurrences of `<searchString>` with `<replacementString>`.
- If `<searchString>` is not found, returns the original string unchanged.
- Performs a case-sensitive search.
- `<boolean>` parameter (optional):
  - `false` (default): regex is supported — special regex chars like `$` are treated as metacharacters.
  - `true`: regex is escaped — all characters in `<searchString>` treated as literals.
- `<searchString>` accepts TEXT; accepts regex patterns when `<boolean>` is `false`.

CANONICAL_EXAMPLES:
```deluge
mainString = "Create online database applications";
newText = replaceAll(mainString, "online", "custom");
// returns "Create custom database applications"

// Literal replacement of regex-special char ($): pass true to escape
price = "$100 and $200";
newText = price.replaceAll("$100", "USD100", true); // treats "$" as literal
```

FAILURE_MODES:
- `<boolean>` is `false` (default) and `<searchString>` contains unescaped regex special chars (e.g. `$`) → special chars act as regex metacharacters, not literals; use `\\$` or pass `true` for literal match.

RELATED_DOCS:
- replaceFirst — replace-first.dou.md
- replaceAllIgnoreCase — https://www.zoho.com/deluge/help/functions/string/replaceallignorecase.html
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/replaceall.html
