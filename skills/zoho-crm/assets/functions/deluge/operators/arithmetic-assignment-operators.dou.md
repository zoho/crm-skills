FILE_PURPOSE: Deluge arithmetic and compound-assignment operators for numeric, string, and date expressions
MENTAL_MODEL: Arithmetic = +, -, *, /, %; compound assignment = +=, -=, *=, /=, %=; type of operand determines result

WHEN_TO_USE:
- Perform numeric calculations: addition, subtraction, multiplication, division, modulus.
- Concatenate Text values with `+`.
- Perform Date-Time arithmetic with `+` / `-`.
- Update a variable in-place with compound assignment.

WHEN_NOT_TO_USE:
- Boolean or List operations — arithmetic operators do not apply.
- `+` with types other than Number, Decimal, Text, or Date-Time — unsupported.

TRIGGER_KEYWORDS:
+=, -=, *=, /=, %=, compound assignment operator, string concatenation +, Date-Time arithmetic, modulus remainder, bigint assignment

RULES:
- `+`: Number, Decimal, Text (concatenation), Date-Time (date addition).
- `-`: Number, Decimal, Date-Time (date subtraction).
- `*`, `/`, `%`: Number and Decimal only.
- Simple assignment `=` supports all Deluge data types.
- `+=` supports Text, Number (bigint), Decimal.
- `-=`, `*=`, `/=`, `%=` support Number (bigint) and Decimal only.

CANONICAL_EXAMPLES:
```deluge
c = 5 + 5;                     // Number: 10
Name = "John" + " " + "Smith"; // Text: "John Smith"
c = 5 - 5;                     // 0
c = 5 * 5;                     // 25
c = 5 / 5;                     // 1
c = 5 % 5;                     // 0

x = 2; x += 1;  // x = 3
x -= 1;         // x = 2
x *= 2;         // x = 4
x /= 2;         // x = 2
x %= 2;         // x = 0
```

FAILURE_MODES:
- Applying `-`, `*`, `/`, or `%` to Text values → type error; only `+` is valid for Text arithmetic.
- Applying `*`, `/`, or `%` to Date-Time values → type error; only `+` and `-` are valid for Date-Time.
- Using `-=`, `*=`, `/=`, or `%=` with Text operand → not supported; only `+=` works with Text compound assignment.
- Applying any compound operator to Boolean, List, or other non-numeric/non-string types → type error.

RELATED_DOCS:
- Arithmetic operators — https://www.zoho.com/deluge/help/operators/arithmetic-operators.html
- Assignment operators — https://www.zoho.com/deluge/help/operators/arithmetic-operators.html

SOURCE:
https://www.zoho.com/deluge/help/operators/arithmetic-operators.html, https://www.zoho.com/deluge/help/operators/assignment-operators.html
