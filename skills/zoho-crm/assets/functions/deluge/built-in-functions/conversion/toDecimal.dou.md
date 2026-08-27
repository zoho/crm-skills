FILE_PURPOSE: Deluge `toDecimal()` — convert a NUMBER, DECIMAL, or numeric TEXT to a DECIMAL value.
MENTAL_MODEL: `expr.toDecimal()` = DECIMAL; TEXT must be purely numeric; preserves fractional precision unlike `toNumber()`.

WHEN_TO_USE:
- Convert a NUMBER to DECIMAL to retain fractional precision in calculations.
- Convert a numeric text string (e.g., `"99.9"`) to DECIMAL for arithmetic.

WHEN_NOT_TO_USE:
- When the TEXT contains non-numeric characters — throws a runtime error.
- When the TEXT is empty — throws a runtime error.
- When fraction truncation is desired — use `toNumber()` instead.

TRIGGER_KEYWORDS:
toDecimal, numeric-text toDecimal, decimal conversion, empty-text runtime, number-to-decimal

RULES:
- Return type: DECIMAL.
- Input types: DECIMAL, NUMBER, TEXT.
- TEXT input: must contain only numerical values; any non-numeric character throws a runtime error.
- Empty TEXT throws a runtime error.

CANONICAL_EXAMPLES:
```deluge
marks = 99.9;
marks_text = "100";

info toDecimal(marks);       // Returns 99.9
info toDecimal(marks_text);  // Returns 100
```

FAILURE_MODES:
- TEXT containing non-numeric characters throws a runtime error.
- Empty TEXT throws a runtime error.

RELATED_DOCS:
- toNumber / toLong — toNumber-toLong.dou.md
- Type conversion functions — https://www.zoho.com/deluge/help/functions/conversion.html

SOURCE:
https://www.zoho.com/deluge/help/functions/common/todecimal.html
