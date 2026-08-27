## FILE_PURPOSE
Deluge eomonth() — shift a date by N months and return that month's last day.

## MENTAL_MODEL
eomonth(date, n) = DATE-TIME of last day in month (date + n months); n negative subtracts.

## WHEN_TO_USE
- Find the last day of the month that is N months ahead of a given date.
- Find the last day of the current month using offset 0: `eomonth(today, 0)`.
- Find the last day of a prior month using a negative offset.

## WHEN_NOT_TO_USE
- Getting start of month — use toStartOfMonth() instead.
- Adding months without needing the last-day snap — use addMonth() instead.

## TRIGGER_KEYWORDS
eomonth, end of month, last day of month, month offset last day, numberOfMonths eomonth

## RULES
- Syntax: `<var> = <dateTimeValue>.eomonth(<numberOfMonths>);`
  or `eomonth(<dateTimeValue>, <numberOfMonths>)`.
- Returns DATE-TIME (date value only; time component is not included in the output).
- Time value of the input is not taken into account.
- Negative `numberOfMonths` subtracts months from dateTimeValue before returning the last day.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
currentDate = '01-Jan-2019';
newDate = currentDate.eomonth(1);   // adds 1 month → Feb 2019; returns '28-Feb-2019'
```

## FAILURE_MODES
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- hour/min/sec value specified in more than 2 digits → runtime error.
- Year value has more than 4 digits → runtime error.

## RELATED_DOCS
- toStartOfMonth — to-start-of-month-week.dou.md
- addMonth — add-sub-month.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/eomonth.html
