FILE_PURPOSE: Deluge `ceil()` / `floor()` — round a DECIMAL to the nearest integer above or below.
MENTAL_MODEL: `d.ceil()` = nearest-larger INTEGER; `d.floor()` = nearest-smaller INTEGER; both return NUMBER.

WHEN_TO_USE:
- Round a decimal up to the next whole number (ceil).
- Round a decimal down to the previous whole number (floor).

WHEN_NOT_TO_USE:
- When rounding to a specific number of decimal places — use `round()` instead.

TRIGGER_KEYWORDS:
ceil(), floor(), ceiling-integer, floor-integer, nearest-above, nearest-below

RULES:
- Both functions input type: DECIMAL.
- `ceil()` return type: NUMBER — always rounds toward positive infinity (away from zero for positives).
- `floor()` return type: NUMBER — always rounds toward negative infinity (toward zero for positives).
- Both accept two syntaxes: `<decimalValue>.ceil()` / `ceil(<decimalValue>)` and `<decimalValue>.floor()` / `floor(<decimalValue>)`.

CANONICAL_EXAMPLES:
```deluge
number = 10.1;
ceilValue  = number.ceil();   // returns 11
floorValue = number.floor();  // returns 10
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- round — round.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/ceil.html, https://www.zoho.com/deluge/help/functions/number/floor.html
