FILE_PURPOSE: Deluge sinh() and asinh() — hyperbolic sine and inverse hyperbolic sine
MENTAL_MODEL: sinh(x) = NUMBER hyperbolic sine of radian angle; asinh(x) = NUMBER inverse hyperbolic sine in radians

WHEN_TO_USE:
- Compute the hyperbolic sine of a radian-valued angle with sinh().
- Compute the inverse hyperbolic sine (arsinh) of a number with asinh().

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
sinh, asinh, number.sinh, number.asinh, hyperbolic sine, inverse hyperbolic sine radians

RULES:
- sinh() syntax: `<variable> = <number>.sinh();` or `sinh(<number>)`.
- asinh() syntax: `<variable> = <number>.asinh();` or `asinh(<number>)`.
- Both accept NUMBER as input.
- Both return NUMBER.
- Angle is measured in radians.

CANONICAL_EXAMPLES:
```deluge
number = 1;
sinhValue = number.sinh();   // returns 1.1752011936438014

number = 1;
asinhValue = number.asinh(); // returns 0.8813735870195429
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/sinh.html, https://www.zoho.com/deluge/help/functions/number/asinh.html
