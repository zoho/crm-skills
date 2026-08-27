## FILE_PURPOSE
Deluge totalMonths() and totalYears() — count calendar months or years respecting actual day counts.

## MENTAL_MODEL
totalMonths/totalYears(start, end) = NUMBER using actual calendar units; leap years and month lengths respected.

## WHEN_TO_USE
- Count exact complete calendar months between two dates, where each month's length is its actual day count.
- Count exact complete calendar years between two dates, accounting for leap years.

## WHEN_NOT_TO_USE
- Fixed-unit counting where 1 month = 30 days or 1 year = 365 days — use monthsBetween()/yearsBetween() instead.
- Time component is significant — both functions ignore the time value.

## TRIGGER_KEYWORDS
totalMonths, totalYears, exact calendar months, leap year aware years, calendar month count

## RULES
- totalMonths() syntax: `<var> = <startDateTimeValue>.totalMonths(<endDateTimeValue>);`
  or `totalMonths(<startDateTimeValue>, <endDateTimeValue>)`.
- totalYears() syntax: `<var> = <startDateTimeValue>.totalYears(<endDateTimeValue>);`
  or `totalYears(<startDateTimeValue>, <endDateTimeValue>)`.
- Both return NUMBER; both parameters are DATE-TIME.
- totalMonths() considers actual days in each month (not a fixed 30).
  - 01-Feb-2020 to 01-Mar-2020: Feb 2020 has 28 days; 28 = 1 full Feb → returns 1.
  - Compare: monthsBetween() returns 0 for this case (28 < 30).
- totalYears() considers actual year length including leap years.
  - 02-Jan-2020 to 01-Jan-2021: leap year 2020 has 366 days; 365 < 366 → returns 0.
  - Compare: yearsBetween() returns 1 for this case (365 = fixed 365).
- Time value is not taken into account for either function.

## CANONICAL_EXAMPLES
```deluge
// totalMonths
startDate  = '31-Dec-1989';
endDate    = '01-Jan-1990';
numMonths  = totalMonths(startDate, endDate);       // returns 0 (1 day < full month)

newEndDate = '01-Feb-1990';
numMonths2 = totalMonths(startDate, newEndDate);    // returns 1

startDate = '01-Feb-2020';
endDate   = '01-Mar-2020';
info totalMonths(startDate, endDate);               // returns 1 (Feb 2020 = 28 days, full month)

// totalYears
startDate = '1-Jan-2019';
endDate   = '31-Dec-2019';
numYears  = totalYears(startDate, endDate);         // returns 0 (364 days)

newStartDate = '1-Jan-2019';
newEndDate   = '1-Jan-2020';
numYears2 = totalYears(newStartDate, newEndDate);   // returns 1
```

## FAILURE_MODES
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.
- totalYears(): 365 days spanning a leap year is not a full year → returns 0, not 1.

## RELATED_DOCS
- monthsBetween — months-years-between.dou.md
- yearsBetween — months-years-between.dou.md
- monthsDiff — https://www.zoho.com/deluge/help/functions/datetime/monthsdiff.html
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/totalmonth.html, https://www.zoho.com/deluge/help/functions/datetime/totalyear.html
