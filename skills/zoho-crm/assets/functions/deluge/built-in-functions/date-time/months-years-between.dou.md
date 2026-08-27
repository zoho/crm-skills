## FILE_PURPOSE
Deluge monthsBetween() and yearsBetween() — count months (30-day) or years (365-day) between dates.

## MENTAL_MODEL
monthsBetween/yearsBetween(start, end) = NUMBER using fixed unit; 1 month = 30 days, 1 year = 365 days.

## WHEN_TO_USE
- Count complete 30-day periods between two dates (monthsBetween()).
- Count complete 365-day periods between two dates (yearsBetween()).

## WHEN_NOT_TO_USE
- Calendar-month or calendar-year counting that respects actual month/year lengths — use totalMonths()/totalYears() instead.
- Time component is significant — both functions ignore the time value.

## TRIGGER_KEYWORDS
monthsBetween, yearsBetween, months between dates, years between dates, fixed 30 day month, 365 day year

## RULES
- monthsBetween() syntax: `<var> = <startDateTimeValue>.monthsBetween(<endDateTimeValue>);`
  or `monthsBetween(<startDateTimeValue>, <endDateTimeValue>)`.
- yearsBetween() syntax: `<var> = <startDateTimeValue>.yearsBetween(<endDateTimeValue>);`
  or `yearsBetween(<startDateTimeValue>, <endDateTimeValue>)`.
- Both return NUMBER; both parameters are DATE-TIME.
- monthsBetween() always treats 1 month as 30 days regardless of actual month length.
  - 01-Feb-2020 to 01-Mar-2020 = 28 days → returns 0 (28 < 30 day threshold).
- yearsBetween() always treats 1 year as 365 days regardless of leap year.
  - 02-Jan-2020 to 01-Jan-2021 = 365 days → returns 1 (fixed 365, ignores leap year).
- monthsBetween(): time value is not taken into account.
- Use monthsDiff() instead when month boundary semantics (not day count) are needed.

## CANONICAL_EXAMPLES
```deluge
// monthsBetween — fixed 30-day month
startDate      = '31-Dec-1989';
endDate        = '01-Jan-1990';
numberOfMonths = monthsBetween(startDate, endDate);    // returns 0 (1 day < 30)

newEndDate = '01-Feb-1990';
numOfMonths = monthsBetween(startDate, newEndDate);    // returns 1 (32 days >= 30)

startDate = '01-Feb-2020';
endDate   = '01-Mar-2020';
info monthsBetween(startDate, endDate);                // returns 0 (Feb 2020 = 28 days < 30)

// yearsBetween — fixed 365-day year
startDate    = '1-Jan-2019';
endDate      = '31-Dec-2019';
numberOfYears = yearsBetween(startDate, endDate);      // returns 0 (364 days < 365)

startDate = '1-Jan-2020';
endDate   = '31-Dec-2020';
numOfYears = yearsBetween(startDate, endDate);         // returns 1 (365 days = 365)
```

## FAILURE_MODES
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.
- monthsBetween(): span < 30 days → returns 0 even if it crosses a calendar month boundary.
- yearsBetween(): 365 days across a leap year counts as 1 year (fixed unit ignores extra day).

## RELATED_DOCS
- monthsDiff — https://www.zoho.com/deluge/help/functions/datetime/monthsdiff.html
- totalMonths — total-months-years.dou.md
- totalYears — total-months-years.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/monthsbetween.html, https://www.zoho.com/deluge/help/functions/datetime/yearsbetween.html
