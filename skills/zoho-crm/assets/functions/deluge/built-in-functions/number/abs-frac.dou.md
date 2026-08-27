FILE_PURPOSE: Deluge `abs()` / `frac()` — extract the magnitude or fractional part of a number.
MENTAL_MODEL: `num.abs()` = DECIMAL without sign; `num.frac()` = NUMBER fractional part only; sign preserved in frac.

WHEN_TO_USE:
- Compute the unsigned magnitude of a positive or negative number (abs).
- Isolate the decimal portion of a number for separate processing (frac).

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
abs(), frac(), abs-magnitude, fractional-part, unsigned-result, frac-sign-preserved

RULES:
- `abs()` return type: DECIMAL; input: NUMBER or DECIMAL.
- `frac()` return type: NUMBER; input: NUMBER.
- `abs()` removes the sign; both positive and negative inputs return the positive magnitude.
- `frac()` preserves the sign of the fractional part: `frac(-25.1)` → `-0.1`.
- Both accept two syntaxes: `<num>.abs()` / `abs(<num>)` and `<num>.frac()` / `frac(<num>)`.

CANONICAL_EXAMPLES:
```deluge
number = -15.50;
absValue = number.abs();      // returns 15.50

inputNumber = 24.6;
info inputNumber.frac();      // returns 0.6

inputNumber = -25.1;
info frac(inputNumber);       // returns -0.1
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/abs.html, http://www.zoho.com/deluge/help/functions/number/frac.html
