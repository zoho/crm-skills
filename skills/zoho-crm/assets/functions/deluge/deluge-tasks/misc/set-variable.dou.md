FILE_PURPOSE: Deluge set variable — declare and assign a local script variable using assignment syntax
MENTAL_MODEL: <variable> = <expression>; creates or overwrites a local variable; returns stored value; no prior declaration needed

WHEN_TO_USE:
- Assign any value or expression to a script-local variable.
- Overwrite a variable's value later in the same script.

WHEN_NOT_TO_USE:
- Cross-script shared state — variables are script-local only; pass values explicitly between functions.

TRIGGER_KEYWORDS:
set variable, variable assignment, declare variable Deluge, local variable overwrite, expression assignment

RULES:
- Syntax: `<variable> = <expression>;`
- Returns the stored value.
- Variables need not be declared before assigning; declaration and assignment happen simultaneously.
- Assigning a new value to an existing variable overwrites the previous value.

CANONICAL_EXAMPLES:
```deluge
temp = 0;
// temp now holds 0

temp = temp + 1;
// temp is now 1; prior value overwritten
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
*(none)*

SOURCE:
https://www.zoho.com/deluge/help/misc-statements/set-variable/declare-variable.html
