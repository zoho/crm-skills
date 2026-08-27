FILE_PURPOSE: Deluge `text()` — format NUMBER, DECIMAL, or DATE-TIME using a custom format pattern string.
MENTAL_MODEL: `expr.text(formatPattern)` = TEXT; format pattern uses `#`/`0` for numbers or datetime literals for dates; mandatory.

WHEN_TO_USE:
- Apply custom numeric formatting (leading zeros, thousands separators, currency symbols) to NUMBER or DECIMAL.
- Format a DATE-TIME value using pattern literals (y, M, d, H, h, E, D, etc.).

WHEN_NOT_TO_USE:
- When `formatText` param is omitted — throws a runtime error.
- On TEXT input — accepted input types are DATE-TIME, DECIMAL, and NUMBER only.

TRIGGER_KEYWORDS:
text(), .text() format, ##,###, $#,##0.00, DDD day-of-year, datetime literal format

RULES:
- Return type: TEXT.
- Input types: DATE-TIME, DECIMAL, NUMBER.
- Syntax: `<expr>.text(<formatText>)`.
  Note: source syntax section shows `<expr>.toText(<formatText>)` but all source examples use `.text()`; `.text()` is treated as the authoritative form.
- `formatText` is mandatory; calling `.text()` with no arguments throws a runtime error.
- Numeric format characters: `#` = digit or nothing; `0` = digit including leading/trailing zeros; `,` = grouping separator; `.` = decimal separator.
- Datetime format letters: `y`/`Y` (year), `M` (month), `d` (day of month), `D` (day of year), `E` (day name), `H`/`h` (hour), `m` (minute), `s` (second), `S` (millisecond), `a` (am/pm), `z`/`Z`/`X` (timezone).
- Text within single quotes in `formatText` is treated as a literal string (e.g., `'at'` outputs "at").

CANONICAL_EXAMPLES:
```deluge
leadingZero    = 2434.text("000000000");              // "000002434"
separateValue  = "123123456".text("##,###");          // "123,123,456"
dayOfYear      = "02/04/2020".text("DDD");            // "035"
dayName        = "02/04/2020".text("EEEE");           // "Tuesday"
currencyFormat = "12345654.1234".text("$#,##0.00");  // "$12,345,654.12"
dateFormat     = zoho.currenttime.text("MM/dd/YY");   // e.g. "02/04/20"
noParam        = zoho.currenttime.text();             // Runtime error: argument count mismatch
```

FAILURE_MODES:
- Calling `.text()` with no arguments throws: "No. of arguments mismatches for the function text".

RELATED_DOCS:
- toText — ../conversion/../conversion/toString-toText.dou.md
- toString — ../conversion/../conversion/toString-toText.dou.md
- Number functions — ../../datatypes/number-decimal.dou.md
- Date-time functions — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/number/text.html
