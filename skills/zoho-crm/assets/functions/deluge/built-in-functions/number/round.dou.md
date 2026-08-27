FILE_PURPOSE: Deluge `round()` — round a number to a specified decimal or integer precision.
MENTAL_MODEL: `num.round(p)` = DECIMAL; positive `p` = decimal places; negative `p` = places left of decimal.

WHEN_TO_USE:
- Round a numeric value to a fixed number of decimal places for display or calculation.
- Round large integers to the nearest 10, 100, or 1000 using negative precision.

WHEN_NOT_TO_USE:
- When truncating decimals to integers without rounding — use `floor()` or `ceil()` instead.

TRIGGER_KEYWORDS:
round(), roundingPrecision, negative-precision rounding, round-to-left, half-up rounding, round-precedence

RULES:
- Return type: DECIMAL; input: DECIMAL/NUMBER (numericalExpression), NUMBER (roundingPrecision).
- Positive `roundingPrecision`: rounds to that many decimal places.
  - Digit to the right of the rounding position ≥ 5 → round up (add 1 to rounding digit, drop remaining).
  - Digit to the right of the rounding position ≤ 4 → truncate (drop without carry).
- Negative `roundingPrecision`: rounds to left of decimal point.
  - `round(-1)` → nearest 10; `round(-2)` → nearest 100.
  - Negative precision ≥ total digits before decimal → returns 0.
- Operator precedence: `.round()` binds to its immediately preceding number literal, not the whole expression.
  - `1.4+3.6.round(0)` evaluates as `1.4 + round(3.6, 0)` = `1.4 + 4` = `5.4`.
  - Use parentheses for whole-expression rounding: `(1.4+3.6).round(0)` = `5`.

CANONICAL_EXAMPLES:
```deluge
218.5.round(0);     // returns 219  (≥5 → round up)
218.4.round(0);     // returns 218  (≤4 → truncate)
218.49.round(1);    // returns 218.5

214.2.round(-1);    // returns 210  (nearest 10)
218.2.round(-2);    // returns 200  (nearest 100)
218.222.round(-3);  // returns 0    (precision ≥ digit count)

1.4 + 3.6.round(0);   // returns 5.4  (rounds 3.6 only — precedence trap)
(1.4 + 3.6).round(0); // returns 5    (rounds the sum)
```

FAILURE_MODES:
- `round(-p)` where `p` ≥ the number of digits before the decimal returns `0` silently — not an error.
- `1.4+3.6.round(0)` ≠ `(1.4+3.6).round(0)`; `.round()` applies to its directly preceding operand without explicit parentheses.

RELATED_DOCS:
- ceil — ceil-floor.dou.md
- floor — ceil-floor.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/round.html
