FILE_PURPOSE: Deluge logical and relational operators for boolean conditional expressions
MENTAL_MODEL: Logical = &&, ||, !; relational = <, >, ==, !=; all return Boolean; precedence: NOT > AND > OR

WHEN_TO_USE:
- Compose multi-condition if/while expressions with AND, OR, NOT.
- Compare two values with relational operators inside conditionals.

WHEN_NOT_TO_USE:
- Non-Boolean operands for logical operators — inputs must be Boolean expressions.
- `<`, `>`, `<=`, `>=` on Text values — unsupported per source.

TRIGGER_KEYWORDS:
AND &&, OR ||, NOT !, equals ==, not-equals !=, NOT-AND-OR precedence, relational boolean result, parentheses precedence

RULES:
- `&&` (AND): both conditions true → combined result true.
- `||` (OR): at least one condition true → combined result true.
- `!` (NOT): negates a single condition; does not connect two conditions.
- Precedence (highest first): NOT → AND → OR; use parentheses to override.
- Innermost parentheses evaluated first; same-level operators evaluated left-to-right.
- Relational operators `<`, `>`, `<=`, `>=`, `==`, `!=`: supported for Number, Decimal, Date-Time.
- `==` and `!=` only: supported for Text (String) comparison.

CANONICAL_EXAMPLES:
```deluge
result       = (Experience > 1) && (Experience < 5);
status_check = (status == "Active") || (status == "Pending");
if(!(a > b)) { info "not greater"; }

// Relational
(x < y)   // true if x < y
(x == y)  // true if x equals y
(x != y)  // true if x is not equal to y
```

FAILURE_MODES:
- `<`, `>`, `<=`, `>=` on Text values → not supported per source.
- `!` applied to compound expression without parentheses: `!a && b` ≠ `!(a && b)`.

RELATED_DOCS:
- Logical operators — https://www.zoho.com/deluge/help/operators/logical-operators.html
- Relational operators — https://www.zoho.com/deluge/help/operators/logical-operators.html

SOURCE:
https://www.zoho.com/deluge/help/operators/logical-operators.html, https://www.zoho.com/deluge/help/operators/relational-operators.html
