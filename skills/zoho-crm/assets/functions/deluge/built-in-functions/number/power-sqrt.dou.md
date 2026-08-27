FILE_PURPOSE: Deluge `power()` / `sqrt()` — exponentiate a number or compute its square root.
MENTAL_MODEL: `b.power(p)` = b^p as DECIMAL; `n.sqrt()` = √n as DECIMAL; √ of negative → null.

WHEN_TO_USE:
- Compute base raised to an arbitrary exponent using power().
- Compute the positive square root of a non-negative number using sqrt().

WHEN_NOT_TO_USE:
- When computing e^x — use exp() instead.
- When the sqrt() input is negative — returns null, not an error; guard before use.

TRIGGER_KEYWORDS:
power(), sqrt(), exponentiation, square-root, negative-sqrt-null, power-base-exponent

RULES:
- `power()` return type: DECIMAL; inputs: NUMBER or DECIMAL (baseNumber), NUMBER or DECIMAL (powerNumber).
- `sqrt()` return type: DECIMAL; input: NUMBER or DECIMAL.
- `sqrt()` on values below 0 returns null (not a runtime error).
- `power()` accepts two syntaxes: `<base>.power(<exp>)` / `power(<base>, <exp>)`.
- `sqrt()` accepts two syntaxes: `<num>.sqrt()` / `sqrt(<num>)`.

CANONICAL_EXAMPLES:
```deluge
numOne = 3;
numTwo = 2;
newValue = numOne.power(numTwo);  // returns 9 (3^2)

number = 9;
sqrtValue = number.sqrt();        // returns 3.0

negative = -4;
info negative.sqrt();             // returns null (no error)
```

FAILURE_MODES:
- `sqrt()` on a negative number returns null silently — no runtime error is raised.

RELATED_DOCS:
- exp — exp.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/power.html, https://www.zoho.com/deluge/help/functions/number/sqrt.html
