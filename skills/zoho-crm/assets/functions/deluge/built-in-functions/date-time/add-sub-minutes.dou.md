## FILE_PURPOSE
Deluge addMinutes() and subMinutes() — add or subtract minutes from a DATE-TIME value.

## MENTAL_MODEL
addMinutes/subMinutes(dateTime, n) = DATE-TIME shifted by n minutes; negative n inverts direction.

## WHEN_TO_USE
- Add or subtract a number of minutes from a DATE-TIME value.

## WHEN_NOT_TO_USE
- Adding/subtracting hours — use addHour()/subHour() instead.
- Adding/subtracting seconds — use addSeconds() instead.

## TRIGGER_KEYWORDS
addMinutes, subMinutes, numberOfMins, datetime minutes shift

## RULES
- addMinutes() syntax: `<var> = <dateTimeValue>.addMinutes(<n>);` or `addMinutes(<dateTimeValue>, <n>)`.
- subMinutes() syntax: `<var> = <dateTimeValue>.subMinutes(<n>);` or `subMinutes(<dateTimeValue>, <n>)`.
- Return type: DATE-TIME.
- Negative `numberOfMins` in addMinutes() subtracts; negative in subMinutes() adds.
- Date-time without a time component defaults to 00:00:00.
- hour ≥ 24 → auto-reset to 00:00:00; minutes ≥ 60 → mm:ss reset to 00:00; seconds ≥ 60 → ss reset to 00.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
// DATE-TIME examples
currentDate = '01-Jan-2019';
info currentDate.addMinutes(1);          // returns '01-Jan-2019 00:01:00'

currentDate = '01-Jan-2019 23:59:10';
info currentDate.addMinutes(2);          // returns '02-Jan-2019 00:01:10'

currentDate = '02-Jan-2019';
info currentDate.subMinutes(1);          // returns '01-Jan-2019 23:59:00'

currentDate = '01-Jan-2019 23:59:10';
info currentDate.subMinutes(2);          // returns '01-Jan-2019 23:57:10'


```

## FAILURE_MODES
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.

## RELATED_DOCS
- addHour — add-sub-hour.dou.md
- addSeconds — add-seconds.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/addminutes.html, https://www.zoho.com/deluge/help/functions/datetime/subminutes.html
