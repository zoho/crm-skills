FILE_PURPOSE: Deluge cos() and acos() — trigonometric cosine and arccosine in radians
MENTAL_MODEL: cos(x) = DECIMAL trig cosine of radian angle; acos(x) = DECIMAL inverse cosine returning radian angle

WHEN_TO_USE:
- Compute the trigonometric cosine of a radian-valued angle with cos().
- Compute the angle in radians whose cosine equals a given value with acos().

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
cos, acos, number.cos, number.acos, trigonometric cosine, arccosine radians

RULES:
- cos() syntax: `<variable> = <number>.cos();` or `cos(<number>)`.
- acos() syntax: `<variable> = <number>.acos();` or `acos(<number>)`.
- Both accept NUMBER or DECIMAL as input.
- Both return DECIMAL.
- Angle is measured in radians.

CANONICAL_EXAMPLES:
```deluge
number = 90;
cosValue = number.cos();    // returns -0.4480736161291702

number = 0.5;
acosValue = number.acos();  // returns 1.0471975511965979
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html
- Degrees — https://www.zoho.com/deluge/help/functions/number/degrees.html
- Radians — https://www.zoho.com/deluge/help/functions/number/radians.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/cos.html, https://www.zoho.com/deluge/help/functions/number/acos.html
