FILE_PURPOSE: Deluge `exp()` — compute e raised to the power of a given number.
MENTAL_MODEL: `num.exp()` = e^num; e ≈ 2.71828182845904; input NUMBER or DECIMAL, return NUMBER.

WHEN_TO_USE:
- Compute the natural exponential function e^x for scientific or statistical calculations.
- Use as the inverse of the natural logarithm log().

WHEN_NOT_TO_USE:
- When raising an arbitrary base to a power — use power() instead.

TRIGGER_KEYWORDS:
exp(), natural-exponential, e-raised-power, euler-number, exp-inverse-log, e-power-formula

RULES:
- Input types: NUMBER or DECIMAL.
- Return type: NUMBER (per parameter table; the Return Type section states "Decimal" — source inconsistency, parameter table treated as authoritative per user resolution).
- e constant = 2.71828182845904 (as documented in source).
- Both `<num>.exp()` and `exp(<num>)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
number = 1;
expValue = number.exp();  // returns 2.718281828459045
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- log — log-log10.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/exp.html
