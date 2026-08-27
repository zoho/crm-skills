FILE_PURPOSE: Deluge `toString()` / `toText()` — convert any expression to TEXT with optional datetime formatting.
MENTAL_MODEL: `expr.toString()` = TEXT representation; DATE-TIME input accepts optional format pattern and timezone for output control.

WHEN_TO_USE:
- Convert any Deluge value (number, date-time, boolean, etc.) to its text representation.
- Format a DATE-TIME value with a custom pattern (e.g., `"MMM dd, yy"`) or specific timezone.
- Convert epoch milliseconds to a human-readable datetime string.

TRIGGER_KEYWORDS:
toString, toText, dateTimeFormat pattern, TZ-database timezone, epoch-milliseconds format, datetime-literal null

RULES:
- Return type: TEXT.
- Input types: ALL DATA TYPES.
- `toString()` and `toText()` are aliases; all four syntaxes are equivalent.
- `dateTimeFormat` (optional): applies when input is DATE-TIME or NUMBER (milliseconds); uses date-time pattern letters (y, M, d, H, h, m, s, etc.); text within single quotes is treated as literal; non-literal characters outside single quotes cause `null` to be returned for those characters.
- `timeZone` (optional): must be an exact TZ database name (e.g., `"Europe/Moscow"`); applies when input is DATE-TIME; defaults to application settings timezone if omitted.
- NUMBER (milliseconds) with `dateTimeFormat`/`timeZone`: supported.
- TEXT in date-time format as input: `dateTimeFormat`/`timeZone` params take effect.
- Unrecognized date-time value → error.

CANONICAL_EXAMPLES:
```deluge
marks = 100;
info toString(marks);   // Returns "100"

dateValue = '01-Jan-2019 10:15:30';
info toString(dateValue, "MMM dd, yy 'at' hh:mm:ss, E", "Europe/Moscow");
// Returns "Jan 01, 19 at 07:45:30, Fri"

milliValue = 1596719471334;
info toString(milliValue, "MMM dd, yy 'at' hh:mm:ss, E", "Europe/Moscow");
// Returns "Aug 06, 20 at 03:41:11, Thu"
```

FAILURE_MODES:
- Non-literal characters in `dateTimeFormat` outside single quotes return `null` for those characters in the output.
- Unrecognized date-time value throws an error.

RELATED_DOCS:
- Type conversion functions — https://www.zoho.com/deluge/help/functions/conversion.html
- toDate — toDate.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/common/tostring.html, https://www.zoho.com/deluge/help/functions/common/to-text.html
