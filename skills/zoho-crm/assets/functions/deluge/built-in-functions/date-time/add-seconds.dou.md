## FILE_PURPOSE
Deluge addSeconds() — add (or subtract) seconds from a DATE-TIME value.

## MENTAL_MODEL
addSeconds(dateTime, n) = DATE-TIME shifted by n seconds; negative n subtracts.

## WHEN_TO_USE
- Add a number of seconds to a DATE-TIME value.
- Subtract seconds by passing a negative number.

## WHEN_NOT_TO_USE
- Adding/subtracting minutes — use addMinutes()/subMinutes() instead.
- Adding/subtracting hours — use addHour()/subHour() instead.

## TRIGGER_KEYWORDS
addSeconds, numberOfSecs, datetime seconds shift, negative seconds subtract

## RULES
- Syntax: `<var> = <dateTimeValue>.addSeconds(<numberOfSecs>);` or `addSeconds(<dateTimeValue>, <numberOfSecs>)`.
- Return type: DATE-TIME.
- Negative `numberOfSecs` subtracts that many seconds.
- Date-time without a time component defaults to 00:00:00.
- hour ≥ 24 → auto-reset to 00:00:00; minutes ≥ 60 → mm:ss reset to 00:00; seconds ≥ 60 → ss reset to 00.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
// DATE-TIME examples
currentDate = '01-Jan-2019';
info currentDate.addSeconds(70);          // returns '01-Jan-2019 00:01:10'

currentDate = '01-Jan-2019 23:15:10';
info currentDate.addSeconds(2);           // returns '01-Jan-2019 23:15:12'


```

## FAILURE_MODES
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.

## RELATED_DOCS
- subSeconds — ../number/../number/subSeconds.dou.md
- addMinutes — add-sub-minutes.dou.md
- addHour — add-sub-hour.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/addseconds.html
