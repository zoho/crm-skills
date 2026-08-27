FILE_PURPOSE: Deluge `isDate()` — return BOOLEAN true when expression is a valid DATE-TIME value.

MENTAL_MODEL: `isDate(expr)` = true (DATE-TIME), false (NUMBER), null (LIST/MAP), error (invalid-text).

WHEN_TO_USE:
- Guard-checking whether a variable holds a valid date-time before performing date operations
- Differentiating DATE-TIME values from numbers in mixed-type scenarios

WHEN_NOT_TO_USE:
- Validating arbitrary text strings for date format — TEXT with an invalid datetime throws an error, not false
- Expecting a universal safe boolean for all non-date inputs — behavior differs by input type

TRIGGER_KEYWORDS: isDate(), boolean-date-check, invalid-text-throws-runtime, null-for-list-map, isDate-boolean-guard

RULES:
1. Return type: BOOLEAN (true/false); or null for LIST/MAP inputs; or runtime error for invalid TEXT.
2. DATE-TIME typed value → true.
3. TEXT containing a valid date-time value → true.
4. TEXT NOT containing a valid date-time value → THROWS ERROR (does not return false).
5. NUMBER → false (no error thrown).
6. LIST or MAP (key-value) → null (not true or false).

CANONICAL_EXAMPLES:
```deluge
dateString = "01-Jan-2019"; // TEXT with valid date
dateValue  = '01-Jun-2020'; // DATE-TIME typed value
numValue   = 100;

boolValOne   = isDate(dateString);   // → true
boolValTwo   = isDate(numValue);     // → false
boolValThree = dateValue.isDate();   // → true

// TRAP: TEXT with invalid date → runtime error, NOT false
// isDate("not-a-date") → ERROR
```

FAILURE_MODES:
- Passing TEXT with an invalid date-time string → runtime error (does NOT return false)
- LIST or MAP input → null (not a boolean; cannot be used in boolean guard without null check)
- Assuming isDate() is a safe universal boolean for all inputs — it is not for invalid TEXT

RELATED_DOCS:
- isNumber() — https://www.zoho.com/deluge/help/functions/type-check/isnumber.html
- isText() — https://www.zoho.com/deluge/help/functions/type-check/istext.html
- Type check functions — https://www.zoho.com/deluge/help/functions/type-check.html

SOURCE:
https://www.zoho.com/deluge/help/functions/common/isdate.html
