FILE_PURPOSE: Deluge replaceFirst() — replace only the first occurrence of a substring
MENTAL_MODEL: replaceFirst(string, search, replacement, regexEscape) = TEXT; replaces first match only; supports regex

WHEN_TO_USE:
- Replace only the first occurrence of a substring or regex pattern while leaving later occurrences intact.
- Use with `boolean=true` when the search string contains regex special characters that should be treated as literals.

WHEN_NOT_TO_USE:
- Replacing all occurrences — use `replaceAll()` instead.

TRIGGER_KEYWORDS:
replaceFirst, string.replaceFirst, regex escape boolean, first occurrence replace, replaceFirst case-sensitive, replacementString

RULES:
- Two syntaxes: `<variable> = <string>.replaceFirst(<searchString>, <replacementString>, <boolean>);` and `replaceFirst(<string>, <searchString>, <replacementString>, <boolean>)`.
- Return type: TEXT.
- Replaces only the FIRST occurrence of `<searchString>` with `<replacementString>`.
- If `<searchString>` is not found, returns the original string unchanged.
- Performs a case-sensitive search.
- `<searchString>` accepts TEXT and regex patterns.
- `<boolean>` parameter:
  - `false` (default): regex is supported — special regex chars are treated as metacharacters.
  - `true`: regex is escaped — all characters in `<searchString>` treated as literals.

CANONICAL_EXAMPLES:
```deluge
mainString = "Create online database applications";
newText = replaceFirst(mainString, "online", "custom");
// returns "Create custom database applications"

// Regex pattern replacement
useremail = "nancy@zylker.com";
newdomain_email = replaceFirst(useremail, "\\@[a-z]{6}\\.[a-z]{3}", "@zylkertech.com");
// returns "nancy@zylkertech.com"
```

FAILURE_MODES:
- `<boolean>` is `false` (default) and `<searchString>` contains unescaped regex special chars → special chars act as metacharacters; use `\\` escape or pass `true` for literal match.

RELATED_DOCS:
- replaceAll — replace-all.dou.md
- replaceFirstIgnoreCase — https://www.zoho.com/deluge/help/functions/string/replacefirstignorecase.html
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/replacefirst.html
