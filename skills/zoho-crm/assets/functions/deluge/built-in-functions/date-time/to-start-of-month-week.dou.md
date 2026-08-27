## FILE_PURPOSE
Deluge toStartOfMonth() and toStartOfWeek() — get first day of a date's month or week.

## MENTAL_MODEL
toStartOfMonth/toStartOfWeek(date) = DATE-TIME at midnight on period start; week starts Sunday.

## WHEN_TO_USE
- Get the first day of the month a given date falls in.
- Get the first day of the week a given date falls in (week starts on Sunday).

## WHEN_NOT_TO_USE
- Getting end of month — use eomonth() instead.
- Getting current period start — combine with now or today: `now.toStartOfMonth()`.

## TRIGGER_KEYWORDS
toStartOfMonth, toStartOfWeek, first day of month, first day of week, Sunday week start

## RULES
- toStartOfMonth() syntax: `<var> = <dateTimeValue>.toStartOfMonth();`
  or `toStartOfMonth(<dateTimeValue>)`.
- toStartOfWeek() syntax: `<var> = <dateTimeValue>.toStartOfWeek();`
  or `toStartOfWeek(<dateTimeValue>)`.
- Both return DATE-TIME; time component of the result is always 00:00:00.
- Time value of the input is not taken into account.
- toStartOfWeek(): Sunday is the first day of the week.
- Runtime error: 2-digit date value exceeds number of days in that month → runtime error.
- Runtime error: month value specified in 3 or more characters that is incorrect → runtime error.
- Returns null (NOT a runtime error) if: month value < 3 characters; hour/min/sec > 2 digits;
  date value > 2 digits; year value > 4 digits.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
// toStartOfMonth
currentDate = '15-Mar-2019 15:00:00';
startDate   = currentDate.toStartOfMonth();  // returns '01-Mar-2019 00:00:00'

// toStartOfWeek (15-Mar-2019 is Friday; week start = Sunday 10-Mar-2019)
startDate   = currentDate.toStartOfWeek();   // returns '10-Mar-2019 00:00:00'
```

## FAILURE_MODES
- 2-digit date value exceeds days in that month → runtime error.
- Month value in 3+ characters that is incorrect → runtime error.
- Month value specified in fewer than 3 characters → returns null (no error thrown).
- hour/min/sec value > 2 digits → returns null (no error thrown).
- Date value specified in more than 2 digits → returns null (no error thrown).
- Year value > 4 digits → returns null (no error thrown).

## RELATED_DOCS
- eomonth — eomonth.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/tostartofmonth.html, https://www.zoho.com/deluge/help/functions/datetime/tostartofweek.html
