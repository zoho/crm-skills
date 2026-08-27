## FILE_PURPOSE
Deluge error message reference — save errors, runtime errors, and built-in function type errors.

## MENTAL_MODEL
Save errors block script saving (syntax/declaration); runtime errors fire during execution (type/bounds/logic).

## WHEN_TO_USE
- Diagnosing a Deluge script that fails to save or throws a runtime error
- Mapping an error message pattern to its root cause and fix

## WHEN_NOT_TO_USE
- *(none in source)*

## TRIGGER_KEYWORDS deluge-save-errors, deluge-runtime-errors, null-operation-runtime, index-out-of-bounds, cast-mismatch, divide-by-zero, undefined-variable

## RULES
Save Errors — block script save:
1. `Variable '<var>' is not defined` — variable used before it is declared/assigned.
2. `Expecting '}' but found '<EOF>'` — unmatched opening brace or block.
3. `Comment Task is not closed properly` — `/*` not paired with `*/`.
4. `Improper Statement Error might be due to missing ';'` — missing semicolon; unclosed string literal; trailing backslash misinterpreted as escape (e.g. `"test\"` treats `\"` as escaped quote, leaving string unclosed). Also raised by: (a) statement split across multiple lines — every statement including `info`, assignments, and chained method calls must fit on a single line ending with `;`; (b) map literal `{"key": value}` used directly in an `invokeurl parameters` field — build the map as a variable first.
5. `Number of Arguments mismatches` — wrong arg count in a Deluge task.
6. `In Criteria left expression is of type <DT1> and right expression is of type <DT2> and the operator <Op> is not valid` — incompatible operand types for the operator used.
7. `<fn> function needs to be assigned to a variable` — value-returning built-in result is not captured.
8. `<fn> function cant be assigned to variable or used in expression` — void built-in result assigned to a variable.
9. `No. of arguments mismatches for the function <fn>` / `Argument type mismatches for the function <fn> at index <i>` — wrong arg count or data type supplied to a built-in.
10. `<integration_task> is not supported for this function` — service-specific integration task invoked outside its service, OR `connections` param omitted in Zoho Cliq.

sendmail save constraints:
11. FROM and TO are mandatory fields; SUBJECT and MESSAGE are mandatory fields.
12. BCC and CC blocked unless From = `zoho.adminuserid` or `zoho.loginuserid`.
13. `Invalid email address found` — From or To field is not of TEXT data type.

Runtime Errors — fire during execution:
14. `Error in performing the Operation / : Divide by zero error` — division by zero terminates execution.
15. `Null value occurred while performing <Op> operation` — any arithmetic/logical operation on a null variable.
16. `Given string is lesser than the applied boundary, so index out of bounds exception arisen` — text index exceeds string length (subText, mid, indexOf, etc.).
17. `Given index <N> is greater than the list size` — collection or list index out of range.
18. `Invalid JSON Format String` — text supplied to JSON parse or toCollection is not valid JSON.
19. `An error occurred while performing this action` — relational operator applied to two non-numeric operands.
20. `'<Number>' can not be cast to 'MAP'` — number used where key-value collection is expected.

Runtime Errors: Built-In Functions:
21. `'TEXT' can not be cast to '[BIGINT]'` — text supplied where NUMBER expected (text, number, datetime functions).
22. `'TEXT' can not be cast to '[DATE-TIME, DATE]'` — text not in a valid date format for a datetime function.
23. `Incompatible types...Required: [DATE-TIME, DATE] Found: NUMBER` — number supplied where DATE or DATE-TIME expected.
24. `'TEXT' can not be cast to '[BOOLEAN]'` — text supplied where boolean expected (e.g. `sort` direction param).
25. `UnParsable date` — value not in a recognized date format (common functions).
26. `Invalid XML or Invalid XPath` — malformed XML string or XPath expression.
27. Non-ASCII characters (em dash `—`, ellipsis `…`, box-drawing `═`, middot `·`, etc.) inside **string literals** — trigger Improper Statement Error on the **following line**, not the line containing the character; the root cause is non-obvious. ASCII characters only in string literals; non-ASCII is safe in comments.

## CANONICAL_EXAMPLES
```deluge
// Save error: undefined variable
info b;        // → save error: "Variable 'b' is not defined"
b = 10; info b; // fix: declare b before use

// Runtime error: divide by zero
a = 20; b = 0;
info a / b; // → runtime: "Divide by zero error"

// Runtime error: text index out of bounds
t = "Hi";
sub = t.subText(0, 10); // → runtime: "string is lesser than applied boundary"
```

## FAILURE_MODES
- String ending with backslash (`"path\"`) causes save error — backslash escapes the closing quote; fix by escaping the backslash (`"path\\"`)
- Divide-by-zero terminates execution at that line — guard with `!= 0` before dividing
- Out-of-bounds error wording differs: text = "string lesser than boundary"; list = "index greater than list size"
- In Zoho Cliq, `connections` param is mandatory for all integration tasks; omitting it raises a save error
- Returning from a function without a value causes `Missing return statement: Provide MAP expression to return`

Runtime Errors: Method calls:
28. `Number of Arguments mismatches for ifnull expecting 2` — `.ifNull(default)` called as a method chain on a value; `ifnull` is a 2-argument standalone function, not a method. Correct form: `ifnull(expression, fallback)` not `expression.ifNull(fallback)`.

## RELATED_DOCS
- Deluge built-in functions — https://www.zoho.com/deluge/help/built-in-functions.html
- Deluge data types — https://www.zoho.com/deluge/help/datatypes.html
- Deluge tasks — https://www.zoho.com/deluge/help/deluge-tasks.html

## SOURCE
https://www.zoho.com/deluge/help/error-messages.html
