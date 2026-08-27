FILE_PURPOSE: Deluge matches() — test if a string matches a regex pattern exactly
MENTAL_MODEL: matches(string, regex) = Boolean; true only when string matches entire regex pattern; case-sensitive

WHEN_TO_USE:
- Validate that a string fully conforms to a regex pattern (e.g. ID format, email format, currency).
- Use case-sensitive full-string comparison against a regular expression.

WHEN_NOT_TO_USE:
- Partial pattern matching (substring search) — use `contains()` instead.
- Case-insensitive matching — `matches()` is always case-sensitive.

TRIGGER_KEYWORDS:
matches, string.matches, regex comparison, boolean return matches, regexString, case-sensitive matches

RULES:
- Two syntaxes: `<variable> = <string>.matches(<regexString>);` and `matches(<string>, <regexString>)`.
- Return type: BOOLEAN.
- Returns `true` if `<string>` matches the entire `<regexString>` regex; `false` otherwise.
- Comparison is case-sensitive.
- `<string>` and `<regexString>` are both TEXT.

CANONICAL_EXAMPLES:
```deluge
IDValue = "ID004500F";
retValue = matches(IDValue, "[A-Z]{2}[0-9]{6}[A-Z]"); // returns true

num = "$345.78";
ret = matches(num, "\\$[0-9]+\\.[0-9]{2}"); // returns true

useremail = "jane2023@zylker.com";
format_check = matches(useremail, "[a-z 0-9]+\\@[a-z]+\\.[a-z]+"); // returns true
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Text functions — https://www.zoho.com/deluge/help/functions/text.html
- Functions returning boolean — https://www.zoho.com/deluge/help/functions-returning-boolean.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/matches.html
