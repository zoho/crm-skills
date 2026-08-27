FILE_PURPOSE: Deluge `subSeconds()` — subtract seconds from a DATE-TIME value; negative value adds seconds.
MENTAL_MODEL: `dt.subSeconds(n)` = dt minus n seconds; negative n adds.

WHEN_TO_USE:
- Subtract a number of seconds from a DATE-TIME value.

WHEN_NOT_TO_USE:
- Subtracting minutes — use subMinutes() instead.
- Subtracting hours — use subHour() instead.

TRIGGER_KEYWORDS:
subSeconds(), negative-adds-seconds, datetime-subtraction, datetime-00-default

RULES:
- Return type: DATE-TIME.
- Input types: DATE-TIME (dateTimeValue), NUMBER (numberOfSecs).
- DATE-TIME input without time component defaults to 00:00:00.
- Negative `numberOfSecs` adds that many seconds instead of subtracting.
- DATE-TIME auto-correction (no error): hour ≥ 24 → resets to 00:00:00; minutes ≥ 60 → resets mm:ss to 00:00; seconds ≥ 60 → resets ss to 00.
- DATE-TIME runtime errors: hour/minute/second in more than 2 digits; date exceeds days in month; year more than 4 digits.

CANONICAL_EXAMPLES:
```deluge
// DATE-TIME examples
currentDate = '02-Jan-2019';
info currentDate.subSeconds(70);     // Returns '01-Jan-2019 23:58:50'

currentDate = '01-Jan-2019 23:15:10';
info currentDate.subSeconds(2);      // Returns '01-Jan-2019 23:15:08'


```

FAILURE_MODES:
- DATE-TIME with hour/minute/second in more than 2 digits throws a runtime error.
- DATE-TIME date value exceeding days in that month throws a runtime error.

RELATED_DOCS:
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/subseconds.html
