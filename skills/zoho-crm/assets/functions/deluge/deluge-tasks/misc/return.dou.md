FILE_PURPOSE: Deluge return statement — specify a typed custom function's return value
MENTAL_MODEL: return <expression>; exits a function and returns expression value; only valid in typed custom functions

WHEN_TO_USE:
- Return a computed value from a custom function that has a declared return type.

WHEN_NOT_TO_USE:
- Functions without a declared return type (void) — return statement is not applicable.

TRIGGER_KEYWORDS:
return, return expression, Custom-Fn only, void-excluded return, return-datatype mismatch

RULES:
- Syntax: `return <expression>;`
- Applicable only inside custom functions that have a declared return type.
- Return value data type must match the declared return type; mismatch → runtime error.

CANONICAL_EXAMPLES:
```deluge
// Function that returns number of days between two dates
int standalone.CalculateDays(date sdate, date edate) {
  days = (((edate - sdate) / 86400000)).toLong();
  return days;
}
```

FAILURE_MODES:
- Return value data type does not match the declared return type → runtime error.
- Used outside a custom function (e.g. in form workflow) → not applicable.

RELATED_DOCS:
*(none in source)*

SOURCE:
https://www.zoho.com/deluge/help/misc-statements/return-statement.html
