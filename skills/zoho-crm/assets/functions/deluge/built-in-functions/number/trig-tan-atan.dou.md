FILE_PURPOSE: Deluge tan() and atan() — trigonometric tangent and arctangent in radians
MENTAL_MODEL: tan(x) = DECIMAL trig tangent of radian angle; atan(x) = DECIMAL inverse tangent returning radian angle

WHEN_TO_USE:
- Compute the trigonometric tangent of a radian-valued angle with tan().
- Compute the angle in radians whose tangent equals a given value with atan().

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
tan, atan, number.tan, number.atan, trigonometric tangent, arctangent radians

RULES:
- tan() syntax: `<variable> = <number>.tan();` or `tan(<number>)`.
- atan() syntax: `<variable> = <number>.atan();` or `atan(<number>)`.
- Both accept NUMBER or DECIMAL as input.
- tan() returns DECIMAL.
- atan() return type is listed as Decimal in the Return Type section of the source.
- Angle is measured in radians.

CANONICAL_EXAMPLES:
```deluge
number = 90;
tanValue = number.tan();    // returns -1.995200412208242

number = 1;
atanValue = number.atan();  // returns 0.7853981633974483
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html
- atan2 — atan2.dou.md
- Degrees — https://www.zoho.com/deluge/help/functions/number/degrees.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/tan.html, https://www.zoho.com/deluge/help/functions/number/atan.html
