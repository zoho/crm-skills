FILE_PURPOSE: Deluge call function — invoke a named custom function from within another Deluge script
MENTAL_MODEL: function_name(params) or variable = function_name(params); invokes a custom function by name

WHEN_TO_USE:
- Invoke a custom function that returns a value and capture its return.
- Invoke a custom function that does not return a value (void call).
- Reuse shared logic (e.g. send mail, record creation) across multiple workflows.

WHEN_NOT_TO_USE:
- In Zoho Sheets, Zoho Connect, or Zoho Cliq — call function is not supported.

TRIGGER_KEYWORDS:
<function_name>(), namespace.function_name, category.function_name, not-Sheets-Connect-Cliq, parameter-count mismatch

RULES:
- Two syntaxes:
  - `<variable> = <function_name>(<parameters>);` — for functions that return a value.
  - `<function_name>(<parameters>);` — for functions that do not return a value.
- `<function_name>` must be the complete name including namespace or category if applicable:
  - Zoho CRM: `<category>.<function_name>`.
- Number of parameters and their data types must match the arguments defined in the function exactly; mismatch prevents the script from being saved.
- NOT supported in Zoho Sheets, Zoho Connect, and Zoho Cliq.

CANONICAL_EXAMPLES:
```deluge
// Call a function that returns a value
lead_response = create_lead("John", "Doe", "john.doe@zylker.com", "Event Registration");
info lead_response;

// Call a void function
send_mail("emily@zylker.com", "Welcome Aboard", "We welcome you aboard.");
```

FAILURE_MODES:
- Parameter count or data type mismatch with defined function arguments → script will not be saved.
- Used in Zoho Sheets, Zoho Connect, or Zoho Cliq → not supported.

RELATED_DOCS:
*(none in source)*

SOURCE:
https://www.zoho.com/deluge/help/misc-statements/call-function.html
