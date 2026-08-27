## FILE_PURPOSE
Deluge addHour() and subHour() — add or subtract hours from a DATE-TIME value.

## MENTAL_MODEL
addHour/subHour(dateTime, n) = DATE-TIME shifted by n hours; negative n inverts direction.

## WHEN_TO_USE
- Add or subtract a number of hours from a DATE-TIME value.

## WHEN_NOT_TO_USE
- Adding/subtracting minutes — use addMinutes()/subMinutes() instead.

## TRIGGER_KEYWORDS
addHour, subHour, numberOfHours, datetime hour shift

## RULES
- addHour() syntax: `<var> = <dateTimeValue>.addHour(<n>);` or `addHour(<dateTimeValue>, <n>)`.
- subHour() syntax: `<var> = <dateTimeValue>.subHour(<n>);` or `subHour(<dateTimeValue>, <n>)`.
- Return type: DATE-TIME.
- Negative `numberOfHours` in addHour() subtracts; negative in subHour() adds.
- Date-time without a time component defaults to 00:00:00.
- hour ≥ 24 → auto-reset to 00:00:00; minutes ≥ 60 → mm:ss reset to 00:00; seconds ≥ 60 → ss reset to 00.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
// DATE-TIME examples
currentDate = '01-Jan-2019';
info currentDate.addHour(1);             // returns '01-Jan-2019 01:00:00'

currentDate = '01-Jan-2019 23:15:10';
info currentDate.addHour(2);             // returns '02-Jan-2019 01:15:10'

currentDate = '02-Jan-2019';
info currentDate.subHour(1);             // returns '01-Jan-2019 23:00:00'


```

## FAILURE_MODES
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.

## RELATED_DOCS
- addMinutes — add-sub-minutes.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/addhour.html, https://www.zoho.com/deluge/help/functions/datetime/subhour.html
