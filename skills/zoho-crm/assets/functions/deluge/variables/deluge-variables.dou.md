FILE_PURPOSE: Deluge variable declaration rules and predefined zoho.* system variables
MENTAL_MODEL: Variables = dynamically-typed script-scoped names; zoho.* = read-only system variables auto-set per execution

WHEN_TO_USE:
- Declare any user variable holding script-local state.
- Read predefined `zoho.*` system variables for current user, date, app context.

WHEN_NOT_TO_USE:
- Cross-script shared state — variables have no global scope; pass parameters explicitly.
- Writing to `zoho.*` variables — they are read-only.

TRIGGER_KEYWORDS:
dynamic typing, variable scope, variable naming rule, zoho.currentdate, zoho.loginuser, zoho.loginuserid, zoho.adminuser, zoho.ipaddress

RULES:
- Variables are dynamically typed; no type declaration required before assignment.
- Scope: limited to the script where declared; no global scope across scripts.
- Naming rules: begin with upper-case, lower-case, or underscore; contain only letters, numbers, underscores; case-sensitive.
- Reserved keywords that cannot be used as variable names: `true`, `false`, `null`, `void`, `return`.
- `zoho.*` variables are predefined, read-only, and auto-set by the system; user scripts cannot modify them.
- Availability of `zoho.*` variables depends on the Zoho service.
- `zoho.ipaddress` returns null when user is not in session (e.g. server-side scheduled or API-triggered executions).

CANONICAL_EXAMPLES:
```deluge
tax  = 0.1;
math = 1 + 1 + 1;

// Predefined zoho.* variables
input.Date = zoho.currentdate;
info zoho.loginuserid;   // email of currently logged-in user
```

FAILURE_MODES:
- Variable name with space (e.g. `total cost`) → parse error; use underscore: `total_cost`.
- Reserved keyword as variable name (`true`, `false`, `null`, `void`, `return`) → parse error.
- Assuming a variable in one script is accessible in another → undefined variable error.
- Case-sensitivity trap: `TotalCost` and `totalcost` are distinct variables; mixing cases silently creates a second unrelated variable.
- Assigning to a `zoho.*` variable (e.g. `zoho.loginuser = "x"`) → error; read-only.
- `zoho.ipaddress` returns null for server-side triggered executions.
- Calling `today()` instead of using `zoho.currentdate` → runtime error `Not able to find 'today' function`; `zoho.currentdate` is a system variable (no parentheses), not a function call.

RELATED_DOCS:
- Zoho variables — https://www.zoho.com/deluge/help/variables.html

SOURCE:
https://www.zoho.com/deluge/help/variables.html, https://www.zoho.com/deluge/help/zoho-variables.html
