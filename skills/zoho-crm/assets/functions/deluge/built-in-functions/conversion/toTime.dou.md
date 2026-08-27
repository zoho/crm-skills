FILE_PURPOSE: Deluge `toTime()` — parse a datetime expression into DATE-TIME with explicit timezone conversion.
MENTAL_MODEL: `expr.toTime(mapping, tz)` = DATE-TIME; `mapping` describes the input structure; `tz` names the input timezone.

WHEN_TO_USE:
- Parse a TEXT datetime string with a custom pattern AND an explicit source timezone into DATE-TIME.
- Convert epoch milliseconds (NUMBER) to a DATE-TIME value.
- Convert a datetime TEXT from a known timezone to the application's default timezone.

WHEN_NOT_TO_USE:
- When no timezone conversion is needed and only date components (y, M, d) matter — use `toDate()`.
- When the expression is already a DATE-TIME: additional parameters are ignored; value is returned as-is.

TRIGGER_KEYWORDS:
toTime, dateTimeMapping toTime, timeZone TZ-database, GMT fallback, epoch-milliseconds toTime, app-settings timezone

RULES:
- Return type: DATE-TIME; formatted and timezone-converted per application settings.
- Input types: TEXT, NUMBER, DATE-TIME.
- NUMBER input: value `1` = `31-Dec-1969`; each increment of `1000` adds 1 second; `dateTimeMapping` is ignored.
- DATE-TIME input: additional parameters are ignored; throws a runtime error if month or day value exceeds valid range.
- `dateTimeMapping` (optional): applies to TEXT input only; applicable literals: `y`, `M`, `d`, `a`, `H`, `h`, `m`, `s`; separator must exactly match the expression separator.
- `timeZone` (optional): applies to TEXT input only; must be an exact TZ database name; if unrecognised, returns time converted to GMT (no error raised).
- Default timezone: application settings timezone.

CANONICAL_EXAMPLES:
```deluge
// App settings: dd-MMM-yyyy, Indian Standard Time (IST = Moscow + 2h 30m)
dateTimeString = "01,11,19 1:30:00 pm";
info toTime(dateTimeString, "MM,d,yyyy hh:mm:ss a", "Europe/Moscow");
// Returns 11-Jan-0019 16:00:00 (1:30 pm Moscow → 16:00 IST)
```

FAILURE_MODES:
- DATE-TIME input with month or day value exceeding valid range throws a runtime error.
- Unrecognised `timeZone` value: silently falls back to GMT; no error is raised.
- `dateTimeMapping` separator that does not exactly match the expression separator causes incorrect or silent mis-parsing.

RELATED_DOCS:
- toDate — toDate.dou.md
- Type conversion functions — https://www.zoho.com/deluge/help/functions/conversion.html

SOURCE:
https://www.zoho.com/deluge/help/functions/common/totime.html
