FILE_PURPOSE: Deluge tanh() and atanh() — hyperbolic tangent and inverse hyperbolic tangent
MENTAL_MODEL: tanh(x) = NUMBER hyperbolic tangent of radian angle; atanh(x) = NUMBER inverse hyperbolic tangent in radians

WHEN_TO_USE:
- Compute the hyperbolic tangent of a radian-valued angle with tanh().
- Compute the inverse hyperbolic tangent (artanh) of a number with atanh().

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
tanh, atanh, number.tanh, number.atanh, hyperbolic tangent, inverse hyperbolic tangent radians

RULES:
- tanh() syntax: `<variable> = <number>.tanh();` or `tanh(<number>)`.
- atanh() syntax: `<variable> = <number>.atanh();` or `atanh(<number>)`.
- Both accept NUMBER as input.
- Both return NUMBER.
- Angle is measured in radians.

CANONICAL_EXAMPLES:
```deluge
number = 0.785398;
tanhValue = number.tanh();   // returns 0.6557941095069071

number = 0.7;
atanhValue = number.atanh(); // returns 0.8673005276940532
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/tanh.html, https://www.zoho.com/deluge/help/functions/number/atanh.html
