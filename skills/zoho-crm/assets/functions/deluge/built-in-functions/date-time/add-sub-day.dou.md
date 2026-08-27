## FILE_PURPOSE
Deluge addDay() and subDay() — add or subtract calendar days from a date-time value.

## MENTAL_MODEL
addDay/subDay(date, n) = DATE-TIME shifted by n calendar days; negative n inverts the direction.

## WHEN_TO_USE
- Add a fixed number of calendar days to a DATE-TIME value.
- Subtract a fixed number of calendar days from a DATE-TIME value.

## WHEN_NOT_TO_USE
- Skipping weekends or holidays — use addBusinessDay()/subBusinessDay() instead.
- Month-level offsets — use addMonth()/subMonth() instead.

## TRIGGER_KEYWORDS
addDay, subDay, numberOfDays, calendar day shift, datetime addDay subDay

## RULES
- addDay() syntax: `<var> = <dateTimeValue>.addDay(<numberOfDays>);`
  or `addDay(<dateTimeValue>, <numberOfDays>)`.
- subDay() syntax: `<var> = <dateTimeValue>.subDay(<numberOfDays>);`
  or `subDay(<dateTimeValue>, <numberOfDays>)`.
- Both functions return DATE-TIME.
- Negative `numberOfDays` in addDay() subtracts that many days.
- Negative `numberOfDays` in subDay() adds that many days.
- Date-time without a time component defaults to time 00:00:00.
- hour ≥ 24 → auto-reset to 00:00:00; minutes ≥ 60 → mm:ss reset to 00:00; seconds ≥ 60 → ss reset to 00.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
currentDate = '01-Jan-2019';
currentDateTime = '01-Jan-2019 15:00:00';

newDate     = currentDate.addDay(11);        // returns '12-Jan-2019 00:00:00'
newDateTime = currentDateTime.addDay(40);    // returns '10-Feb-2019 15:00:00'

newDate = currentDate.subDay(1);             // returns '31-Dec-2018 00:00:00'

// Negative n in addDay → subtracts
info '15-Mar-2019'.addDay(-3);               // returns '12-Mar-2019 00:00:00'
```

## FAILURE_MODES
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.

## RELATED_DOCS
- addBusinessDay — add-sub-business-day.dou.md
- addMonth — add-sub-month.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/addday.html, https://www.zoho.com/deluge/help/functions/datetime/subday.html
