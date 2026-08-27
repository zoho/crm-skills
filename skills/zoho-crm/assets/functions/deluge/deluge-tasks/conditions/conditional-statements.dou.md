FILE_PURPOSE: Deluge conditional statements — if, else if, else, conditional if, and ifNull branching
MENTAL_MODEL: Five branching forms; if/else-if/else execute actions; conditional-if and ifNull return values

WHEN_TO_USE:
- Branch Deluge execution based on boolean criteria using if, else if, else.
- Return one of two values based on a criterion using conditional if.
- Return a fallback value when an expression evaluates to null using ifNull.

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
if, else if, else, conditional if, ifNull, ifNull expression, criteria-based branch

RULES:
- Criteria is mandatory for `if`, `else if`, and `conditional if`; `else` does NOT accept criteria.
- `else if` must be preceded by an `if` statement.
- `else` must be preceded by `if` or `else if`; must be the last statement in its set; cannot be followed by `if` or `else if` in the same set.
- Conditional if syntax: `<variable> = if(<criteria>, <success_value>, <failure_value>);` — returns `<success_value>` if criterion met, `<failure_value>` if not.
- `ifNull` syntax: `<variable> = ifNull(<expression1>, <expression2>);` — returns `expression1` if not null; returns `expression2` if `expression1` is null.
- `<success_value>` and `<failure_value>` accept direct values, expressions, or nested conditional statements.

CANONICAL_EXAMPLES:
```deluge
// if / else if / else
if(zoho.currentdate.weekday() == 7) {
  info "Today is a Holiday";
} else if(zoho.currentDate.weekday() == 6) {
  info "Today is a half working day";
} else {
  info "Today is a working day";
}

// ifNull — returns "Not found" if nameList.get(10) is null
name = ifNull(nameList.get(10), "Not found");
// Equivalent to:
// if(nameList.get(10) == null) { name = "Not Found"; }
// else { name = nameList.get(10); }
```

FAILURE_MODES:
- `else` given criteria → syntax error; `else` accepts no criteria.
- `else if` or `else` without a preceding `if` → syntax error.
- `else` followed by `if` or `else if` in the same set → syntax error; `else` must be the last statement.

RELATED_DOCS:
- Criteria in conditional statements — criteria-conditional-statements.dou.md

SOURCE:
https://www.zoho.com/deluge/help/conditional-statements/condition.html
