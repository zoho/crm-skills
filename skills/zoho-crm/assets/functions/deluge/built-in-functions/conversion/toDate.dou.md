FILE_PURPOSE: Deluge `toDate()` — parse TEXT, NUMBER, or DATE-TIME expression into a DATE-TIME value.
MENTAL_MODEL: `expr.toDate(mapping)` = DATE-TIME; `mapping` tells the parser which text segment corresponds to year/month/day.

WHEN_TO_USE:
- Parse a custom-formatted date string (e.g., `"01,11,2019"`) into a DATE-TIME using a `dateTimeMapping`.
- Convert epoch milliseconds (NUMBER) to a DATE-TIME value.
- Normalise a date-time expression to the application's configured date format.

WHEN_NOT_TO_USE:
- When the mapping must include time components (hours, minutes, seconds, am/pm) — use `toTime()` which supports `a`, `H`, `h`, `m`, `s` literals.
- When the expression is already a DATE-TIME: additional parameters are ignored and the value is returned as-is.

TRIGGER_KEYWORDS:
toDate, dateTimeMapping toDate, y M d literals, epoch-milliseconds toDate, text-to-datetime parse, app-settings date format

RULES:
- Return type: DATE-TIME; output format follows application settings.
- Input types: TEXT, NUMBER, DATE-TIME.
- NUMBER input: value `1` = `31-Dec-1969`; each increment of `1000` adds 1 second; `dateTimeMapping` is ignored.
- DATE-TIME input: additional parameters are ignored; throws a runtime error if month value exceeds months in a year or day value exceeds days in a month.
- TEXT input: `dateTimeMapping` specifies component mapping; applicable literals: `y` (year), `M` (month), `d` (day).
- `dateTimeMapping` separator must exactly match the separator used in the expression string.
- Numeric month: use `M` or `MM`; text month (e.g., "Jan"): use `MMM` or more `M`s.

CANONICAL_EXAMPLES:
```deluge
dateTimeString = "01,11,2019 1:30:00 pm";
info toDate(dateTimeString, "MM,d,yyyy");
// MM=01 (January), d=11, yyyy=2019
// Returns 11-Jan-2019 (assuming app settings format is dd-MMM-yyyy)
```

FAILURE_MODES:
- DATE-TIME input with a month value exceeding the number of months in a year throws a runtime error.
- DATE-TIME input with a day value exceeding the number of days in a month throws a runtime error.
- `dateTimeMapping` separator that does not exactly match the expression separator causes incorrect or silent mis-parsing.

RELATED_DOCS:
- toTime — toTime.dou.md
- Type conversion functions — https://www.zoho.com/deluge/help/functions/conversion.html

SOURCE:
https://www.zoho.com/deluge/help/functions/common/todate.html
