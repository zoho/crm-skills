FILE_PURPOSE: Deluge proper() — convert a string to title/start case
MENTAL_MODEL: proper(string) = TEXT; first char of each word uppercase, all remaining lowercase

WHEN_TO_USE:
- Normalize user-entered names or titles to consistent start case.
- Convert an all-lowercase or all-uppercase string to title case.

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
proper, string.proper, title case, start case, first char uppercase proper

RULES:
- Syntax: `<variable> = <string>.proper();`
- Return type: TEXT.
- First character of each word is returned in upper case.
- All other characters in each word are returned in lower case.
- `<string>` must be TEXT.

CANONICAL_EXAMPLES:
```deluge
product_name = "zoho creator";
newText = product_name.proper(); // returns "Zoho Crm"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/proper.html
