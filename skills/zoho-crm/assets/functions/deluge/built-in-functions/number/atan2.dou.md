FILE_PURPOSE: Deluge atan2() — angle from positive x-axis to point (x,y) in radians
MENTAL_MODEL: atan2(y, x) = NUMBER angle in radians from x-axis to ray through point; y-axis argument is first

WHEN_TO_USE:
- Compute the angle (in radians) between the positive x-axis and the ray from the origin to a specified point (x, y).
- Use when both x and y coordinates are available and quadrant-aware angle is needed.

WHEN_NOT_TO_USE:
- When only one coordinate is available — use atan() instead.

TRIGGER_KEYWORDS:
atan2, number.atan2, atan2 y-axis x-axis, two-argument arctangent, origin-to-point angle

RULES:
- Syntax: `<variable> = atan2(<y-axis>, <x-axis>);` or `<variable> = <y-axis>.atan2(<x-axis>);`.
- First argument is the y-axis value; second argument is the x-axis value.
- Both arguments accept NUMBER.
- Returns NUMBER (angle in radians).
- Result represents the angle between the positive x-axis and the ray from (0,0) to the point (x, y).

CANONICAL_EXAMPLES:
```deluge
number = 1;
atan2Value = number.atan2(2); // returns 0.4636476090008061
// equivalent: atan2(1, 2) — y=1, x=2
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- atan — trig-tan-atan.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/atan2.html
