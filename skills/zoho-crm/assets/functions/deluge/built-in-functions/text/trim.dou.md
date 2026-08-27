## FILE_PURPOSE
Deluge `trim()` — remove all leading and trailing whitespace from a text string.

## MENTAL_MODEL
`str.trim()` = TEXT with all leading and trailing spaces removed; internal spaces are unaffected.

## WHEN_TO_USE
- Remove both leading and trailing whitespace from a text string in a single operation.

## WHEN_NOT_TO_USE
- When only leading whitespace needs removal — use `ltrim()` instead.
- When only trailing whitespace needs removal — use `rtrim()` instead.

## TRIGGER_KEYWORDS
trim(), leading-trailing whitespace removal, full-trim, trim vs ltrim, trim vs rtrim

## RULES
- Return type: TEXT.
- Input type: TEXT.
- Removes ALL leading AND trailing spaces.
- Internal (mid-string) spaces are not affected.
- Both `.trim()` and `trim(<string>)` syntaxes are valid.

## CANONICAL_EXAMPLES
```deluge
mainString = " Welcome to Zoho CRM ";
newText = trim(mainString);   // returns "Welcome to Zoho CRM"
```

## FAILURE_MODES
- CRM merge variables (e.g. `${Accounts.Id}`) can deliver whitespace-only strings; `length() == 0` or `isEmpty()` checks pass these through as non-empty. Always `trim()` merge variable inputs before an empty check: `if (value == null || value.trim().length() == 0)`.

## RELATED_DOCS
- ltrim — ltrim.dou.md
- rtrim — rtrim.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

## SOURCE
https://www.zoho.com/deluge/help/functions/string/trim.html
