## FILE_PURPOSE
Deluge daysBetween() and hoursBetween() — count calendar days or whole hours between two date-times.

## MENTAL_MODEL
daysBetween/hoursBetween(start, end) = NUMBER; hoursBetween truncates minutes and seconds.

## WHEN_TO_USE
- Count the number of calendar days between two DATE-TIME values.
- Count the number of whole hours between two DATE-TIME values (ignoring partial minutes/seconds).

## WHEN_NOT_TO_USE
- Month-level or year-level span counting — use monthsBetween()/totalMonths() instead.
- Exact sub-hour time difference — hoursBetween() truncates minutes and seconds.

## TRIGGER_KEYWORDS
daysBetween, hoursBetween, date difference days, hours between dates, start end datetime count

## RULES
- daysBetween() syntax: `<var> = <startDateValue>.daysBetween(<endDateValue>);`
  or `daysBetween(<startDateValue>, <endDateValue>)`.
- hoursBetween() syntax: `<var> = <startDateTimeValue>.hoursBetween(<endDateTimeValue>);`
  or `hoursBetween(<startDateTimeValue>, <endDateTimeValue>)`.
- Both return NUMBER; both parameters are DATE-TIME.
- days360() is an alternative to daysBetween() and behaves the same way.
- hoursBetween() does NOT calculate the minutes and seconds difference; result is truncated to whole hours.
- hoursBetween(): if startDateTimeValue > endDateTimeValue → returns a negative number.

## CANONICAL_EXAMPLES
```deluge
// daysBetween
startDate    = '1-Jan-2019';
endDate      = '31-Dec-2019';
numberOfDays = daysBetween(startDate, endDate);    // returns 364

newStartDate = '1-Jan-2020';
newEndDate   = '31-Dec-2020';
numOfDays    = daysBetween(newStartDate, newEndDate); // returns 365 (leap year)

// hoursBetween — truncates minutes/seconds
start_time   = '18-Dec-2019 07:00:00';
end_time     = '18-Dec-2019 08:59:59';
total_hours  = hoursBetween(start_time, end_time); // returns 1 (59:59 of partial hour discarded)

start_time   = '18-Dec-2019 09:00:00';
end_time     = '19-Dec-2019 10:00:00';
total_hours  = hoursBetween(start_time, end_time); // returns 25
```

## FAILURE_MODES
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error (daysBetween) / incorrect year error (hoursBetween).

## RELATED_DOCS
- days360 — ../number/../number/days360.dou.md
- monthsBetween — months-years-between.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/daysbetween.html, https://www.zoho.com/deluge/help/functions/datetime/hoursbetween.html
