FILE_PURPOSE: Deluge criteria syntax — boolean conditions chained by logical operators for branching
MENTAL_MODEL: Criteria = one or more boolean conditions joined by logical operators; overall evaluates true/false

WHEN_TO_USE:
- Specify boolean conditions inside `if`, `else if`, or `conditional if` statements.
- Chain multiple conditions with `&&` (AND) and `||` (OR) logical operators.

WHEN_NOT_TO_USE:
- Inside an `else` statement — `else` does not accept criteria.

TRIGGER_KEYWORDS:
criteria, condition BOOLEAN, isNull, in not in, logical-operator chain, expression1 operator expression2

RULES:
- Criteria syntax: `(<condition_1> <logical_operator> <condition_2> ... <condition_n>)`
- Each condition is either `(<expression1> <operator> <expression2>)` or `(<function_returning_boolean>)`.
- Conditions evaluate to BOOLEAN; overall criteria evaluates to BOOLEAN.
- TEXT operators: `==`, `!=`, `is`, `is not`, `in`, `not in`; `in`/`not in` accept TEXT list.
- NUMBER/Decimal operators: `==`, `!=`, `is`, `is not`, `>`, `<`, `>=`, `<=`, `in`, `not in`.
- DATE-TIME operators: `==`, `!=`, `is`, `is not`, `in`, `not in`; accepts system variables `tomorrow`, `yesterday`, `now`, `today`.
- LIST operators: `==`, `in`, `!=`, `not in`; `in` matches if variable contains any specified list values even when additional elements are present.
- Null checks via `is not`: source advises using `isNull` function instead for null-checking.
- Field link names NOT supported in Custom Functions or Custom Schedule Workflows.

CANONICAL_EXAMPLES:
```deluge
// Multi-condition criteria with && and ||
if ((a > 5) && (b > 10) || (c > 20)) {
  // actions_to_be_executed
}
```

FAILURE_MODES:
- Passing criteria to `else` → syntax error; `else` accepts no criteria.
- Using field link name syntax in Custom Functions or Custom Schedule Workflows → unsupported.

RELATED_DOCS:
- Conditional statements — conditional-statements.dou.md
- Criteria while fetching records — https://www.zoho.com/deluge/help/criteria-conditional-statements.html
- Logical operators — ../../operators/logical-relational-operators.dou.md

SOURCE:
https://www.zoho.com/deluge/help/criteria-conditional-statements.html
