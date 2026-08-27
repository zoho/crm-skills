FILE_PURPOSE: Deluge `toNumber()` / `toLong()` — convert any expression to an integer NUMBER, truncating decimals.
MENTAL_MODEL: `expr.toNumber()` = cast to integer; decimal fraction is truncated; DATE-TIME → milliseconds since epoch.

WHEN_TO_USE:
- Convert a numeric text string (e.g., `"1234"`) to a NUMBER for arithmetic operations.
- Strip the fractional part of a DECIMAL to get an integer.
- Convert a DATE-TIME value to its millisecond representation (epoch offset from `'31-Dec-1969 16:00:00'`).

WHEN_NOT_TO_USE:
- When the TEXT contains non-numeric characters (e.g., `"1000abc"`) — throws a runtime error.
- When fraction preservation is required — use `toDecimal()` instead.
- When the TEXT is empty — throws a runtime error.

TRIGGER_KEYWORDS:
toNumber, toLong, decimal truncation, datetime milliseconds, numeric-text cast, alphanumeric cast fails

RULES:
- Return type: NUMBER.
- Input types accepted: NUMBER, DECIMAL, DATE-TIME, TEXT.
- `toNumber()` and `toLong()` are aliases; all four syntaxes are equivalent:
  `expr.toNumber()`, `toNumber(expr)`, `expr.toLong()`, `toLong(expr)`.
- DECIMAL input: fraction part is silently truncated (e.g., `123.25` → `123`; `99.9` → `99`).
- DATE-TIME input: converted to milliseconds offset from `'31-Dec-1969 16:00:00'` (= 0);
  `'31-Dec-1969 16:00:01'` → `1000`; `'31-Dec-1969 15:59:59'` → `-1000`.
- TEXT input: must contain only numeric characters; alphanumeric text throws a runtime error.
- Empty TEXT input throws a runtime error.

CANONICAL_EXAMPLES:
```deluge
decimal = 123.25;
info decimal.toNumber();      // Returns 123 (fraction truncated, not rounded)

num_text = "1234";
info num_text.toNumber();     // Returns 1234

alpha_text = "134A123B";
info alpha_text.toNumber();   // Throws runtime error — alphanumeric not allowed

marks = 99.9;
info toLong(marks);           // Returns 99 (toLong is alias of toNumber)
```

FAILURE_MODES:
- TEXT containing alphanumeric characters (e.g., `"134A123B"`) throws a runtime error.
- Empty TEXT input throws a runtime error.
- DECIMAL fraction is silently truncated without rounding: `99.9` → `99`, not `100`.

RELATED_DOCS:
- toDecimal — toDecimal.dou.md
- Type conversion functions — https://www.zoho.com/deluge/help/functions/conversion.html

SOURCE:
https://www.zoho.com/deluge/help/functions/common/to-number.html, https://www.zoho.com/deluge/help/functions/common/tolong.html
