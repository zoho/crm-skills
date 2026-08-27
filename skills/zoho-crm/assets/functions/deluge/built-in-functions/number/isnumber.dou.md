FILE_PURPOSE: Deluge isNumber() — check whether an expression evaluates to a valid numeric value
MENTAL_MODEL: isNumber(x) = Boolean; true if x is a valid number literal, variable, or arithmetic result; null for List/Map

WHEN_TO_USE:
- Validate that an expression or variable holds a numeric value before performing arithmetic.
- Check if a string in quotes contains a valid numeric literal (e.g. "12.3" returns true).

WHEN_NOT_TO_USE:
- Checking a List or Key-value — isNumber() returns null (not false) for those input types.

TRIGGER_KEYWORDS:
isNumber, expression.isNumber, boolean type-check numeric, quoted number isNumber, null for List Map

RULES:
- Two syntaxes: `isNumber(<expression>)` or `<expression>.isNumber()`.
- Returns BOOLEAN (true or false).
- Valid numerical values in single or double quotes return true.
- String expressions containing arithmetic operators (e.g. `"24/2*10"`) return false.
- List and Key-value data types always return null (not true or false).

CANONICAL_EXAMPLES:
```deluge
numValue = isNumber("12.3");         // returns true
numValue = "1".isNumber();           // returns true
numValue = 24.isNumber();            // returns true
numValue = (24/2*10).isNumber();     // returns true
numValue = "24/2*10".isNumber();     // returns false
```

FAILURE_MODES:
- List or Key-value as input → returns null, not false; null-check required to avoid silent logic errors.

RELATED_DOCS:
- Type check functions — https://www.zoho.com/deluge/help/functions/type-check.html
- Functions returning boolean — https://www.zoho.com/deluge/help/functions-returning-boolean.html
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/common/isnumber.html
