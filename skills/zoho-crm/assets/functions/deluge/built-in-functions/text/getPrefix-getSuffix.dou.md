FILE_PURPOSE: Deluge `getPrefix()` / `getSuffix()` — split a string on the first delimiter occurrence.
MENTAL_MODEL: `str.getPrefix(delim)` = TEXT before first `delim`; `str.getSuffix(delim)` = TEXT after first `delim`; null if not found.

WHEN_TO_USE:
- Extract the portion of a string before a known delimiter (e.g., comma, keyword, separator).
- Extract the portion of a string after a known delimiter.

WHEN_NOT_TO_USE:
- When splitting on more than the first occurrence — both functions use only the FIRST occurrence as the split point.
- When the delimiter is not found — both return `null`, not an empty string; guard before using the result.

TRIGGER_KEYWORDS:
getPrefix(), getSuffix(), before-delimiter extraction, after-delimiter extraction, null-not-found, case-sensitive split

RULES:
- Return type: TEXT.
- Input types: TEXT (string), TEXT (searchString).
- Both functions perform a case-sensitive search.
- `getPrefix()`: returns all characters BEFORE the first occurrence of searchString.
- `getSuffix()`: returns all characters AFTER the first occurrence of searchString.
- If searchString is not found, both functions return `null` (not an empty string and not an error).
- Only the FIRST occurrence determines the split point; all content after it is included in getSuffix.

CANONICAL_EXAMPLES:
```deluge
text = "Zoho CRM is a customer relationship platform, which helps you manage sales pipelines";
newText = text.getPrefix(",");   // returns "Zoho CRM is a customer relationship platform"

text2 = "Manage customer data with Zoho CRM";
newText2 = text2.getSuffix("with");  // returns " Zoho CRM" (includes trailing space)
```

FAILURE_MODES:
- When searchString is not found, both functions return `null` — check for null before further string operations on the result.
- Only the FIRST occurrence is used as split point; content between multiple occurrences of the delimiter is included in the result.

RELATED_DOCS:
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/getPrefix.html, https://www.zoho.com/deluge/help/functions/string/getSuffix.html
