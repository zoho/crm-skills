## FILE_PURPOSE
Deluge addMonth() and subMonth() — add or subtract calendar months from a date-time value.

## MENTAL_MODEL
addMonth/subMonth(date, n) = DATE-TIME shifted by n months counted at month boundaries, not day count.

## WHEN_TO_USE
- Add a number of calendar months to a DATE-TIME value.
- Subtract a number of calendar months from a DATE-TIME value.

## WHEN_NOT_TO_USE
- Day-based arithmetic — use addDay()/subDay() instead.
- Year-level offsets — use addYear()/subYear() instead.

## TRIGGER_KEYWORDS
addMonth, subMonth, numberOfMonths, calendar month boundary, datetime month shift

## RULES
- addMonth() syntax: `<var> = <dateTimeValue>.addMonth(<numberOfMonths>);`
  or `addMonth(<dateTimeValue>, <numberOfMonths>)`.
- subMonth() syntax: `<var> = <dateTimeValue>.subMonth(<numberOfMonths>);`
  or `subMonth(<dateTimeValue>, <numberOfMonths>)`.
- Both functions return DATE-TIME.
- Negative `numberOfMonths` in addMonth() subtracts; negative in subMonth() adds.
- Month arithmetic counts calendar month boundaries, not the number of days in each month.
  (01-Jan→01-Feb = 1 month; 01-Feb→01-Mar = 1 month, even though day counts differ.)
- Date-time without a time component defaults to 00:00:00.
- hour ≥ 24 → auto-reset to 00:00:00; minutes ≥ 60 → mm:ss reset to 00:00; seconds ≥ 60 → ss reset to 00.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
currentDate     = '01-Jan-2019';
currentDateTime = '01-Jan-2019 15:00:00';

newDate     = currentDate.addMonth(11);       // returns '01-Dec-2019 00:00:00'
newDateTime = currentDateTime.addMonth(13);   // returns '01-Feb-2020 15:00:00'

newDate = currentDate.subMonth(1);            // returns '01-Dec-2018 00:00:00'

// Negative n in addMonth → subtracts
info '01-Mar-2019'.addMonth(-2);              // returns '01-Jan-2019 00:00:00'
```

## FAILURE_MODES
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.

## RELATED_DOCS
- addDay — add-sub-day.dou.md
- addYear — ../number/../number/addYear-subYear.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/addmonth.html, https://www.zoho.com/deluge/help/functions/datetime/submonth.html
