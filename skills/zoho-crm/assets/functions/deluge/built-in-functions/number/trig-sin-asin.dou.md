FILE_PURPOSE: Deluge sin() and asin() — trigonometric sine and arcsine in radians
MENTAL_MODEL: sin(x) = DECIMAL trig sine of radian angle; asin(x) = DECIMAL inverse sine returning radian angle

WHEN_TO_USE:
- Compute the trigonometric sine of a radian-valued angle with sin().
- Compute the angle in radians whose sine equals a given value with asin().

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
sin, asin, number.sin, number.asin, trigonometric sine, arcsine radians

RULES:
- sin() syntax: `<variable> = <number>.sin();` or `sin(<number>)`.
- asin() syntax: `<variable> = <number>.asin();` or `asin(<number>)`.
- Both accept NUMBER or DECIMAL as input.
- Both return DECIMAL.
- Angle is measured in radians.

CANONICAL_EXAMPLES:
```deluge
number = 90;
sinValue = number.sin();    // returns 0.8939966636005579

number = 1;
asinValue = number.asin();  // returns 1.5707963267948966
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html
- Degrees — https://www.zoho.com/deluge/help/functions/number/degrees.html
- Radians — https://www.zoho.com/deluge/help/functions/number/radians.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/sin.html, https://www.zoho.com/deluge/help/functions/number/asin.html
