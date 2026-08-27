FILE_PURPOSE: Deluge cosh() and acosh() — hyperbolic cosine and inverse hyperbolic cosine
MENTAL_MODEL: cosh(x) = NUMBER hyperbolic cosine of radian angle; acosh(x) = NUMBER inverse hyperbolic cosine in radians

WHEN_TO_USE:
- Compute the hyperbolic cosine of a radian-valued angle with cosh().
- Compute the inverse hyperbolic cosine (arcosh) of a number with acosh().

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
cosh, acosh, number.cosh, number.acosh, hyperbolic cosine, inverse hyperbolic cosine radians

RULES:
- cosh() syntax: `<variable> = <number>.cosh();` or `cosh(<number>)`.
- acosh() syntax: `<variable> = <number>.acosh();` or `acosh(<number>)`.
- Both accept NUMBER as input.
- Both return NUMBER.
- Angle is measured in radians.

CANONICAL_EXAMPLES:
```deluge
number = 0;
coshValue = number.cosh();   // returns 1.0

number = 3;
acoshValue = number.acosh(); // returns 1.762747174039086
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/cosh.html, https://www.zoho.com/deluge/help/functions/number/acosh.html
