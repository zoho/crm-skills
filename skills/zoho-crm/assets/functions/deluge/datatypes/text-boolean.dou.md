FILE_PURPOSE: Deluge Text and Boolean datatypes — string literals and true/false state
MENTAL_MODEL: Text = double-quoted character sequence; Boolean = unquoted true/false; no implicit coercion between them

WHEN_TO_USE:
- Text: store any character sequence — words, sentences, numeric-looking strings, special characters.
- Boolean: represent binary state in conditionals; returned by relational and contains-type functions.

WHEN_NOT_TO_USE:
- Text for arithmetic — store numeric values as Number or Decimal.
- Text string "true"/"false" as substitute for Boolean true/false.

TRIGGER_KEYWORDS:
text datatype, boolean true, boolean false, double-quote delimiter, backslash escape, case-insensitive boolean, no-quote boolean

RULES:
- Text values must be enclosed in double quotes (`"value"`); single quotes produce Date-Time, not Text.
- Backslash `\` is the escape character; use `\"` for a literal double quote inside Text.
- Numeric characters stored in Text are Text datatype — no implicit coercion to Number.
- Boolean values must NOT be enclosed in quotes (single or double).
- Boolean is case-insensitive: `true`, `TRUE`, `True`, `tRuE` are all equivalent.

CANONICAL_EXAMPLES:
```deluge
Name    = "John";
Address = "Zoho Corp, Pleasanton, CA";
escaped = "He said \"hello\"";
Num     = "1234567890";   // Text, NOT Number

job_experience    = false;
Salary_negotiable = true;
flag              = TRUE;    // same as true

wrong = "true";   // Text "true", NOT Boolean true
```

FAILURE_MODES:
- Text not in double quotes — interpreted as variable name or identifier, not string literal.
- Text in single quotes (e.g. `'John'`) — interpreted as Date-Time; applying Text built-ins fails.
- Unescaped `"` inside a Text literal — parse error; use `\"`.
- Numeric-looking Text not auto-coerced to Number; explicit conversion needed for arithmetic.
- `"true"` (Text) does not equal Boolean `true`; `if (flag == true)` where `flag = "true"` evaluates false.
- `'true'` (single-quoted) — Text or Date-Time, never Boolean.

RELATED_DOCS:
- Text built-in functions — ../built-in-functions/text/text.dou.md
- Functions returning Boolean — https://www.zoho.com/deluge/help/functions-returning-boolean.html

SOURCE:
https://www.zoho.com/deluge/help/datatypes/text.html, https://www.zoho.com/deluge/help/datatypes/boolean.html
