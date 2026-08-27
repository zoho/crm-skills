FILE_PURPOSE: Deluge `edate()` — add N months to a DATE-TIME; negative N subtracts months.

MENTAL_MODEL: `dt.edate(n)` = DATE-TIME n months ahead; n < 0 subtracts; time component stripped from output.

WHEN_TO_USE:
- Advancing or retreating a date by whole calendar months
- Month-based deadline or period calculations

WHEN_NOT_TO_USE:
- Need to add calendar days → use addDay()
- Need to add business days → use workday() / addBusinessDay()
- Need to add years → use addYear()

TRIGGER_KEYWORDS: edate(), add-months-datetime, negative-month-subtraction, edate-time-stripped, month-offset-DATE-TIME

RULES:
1. Return type: DATE-TIME (date only — time component is NOT retained in the output).
2. Input: DATE-TIME (base), NUMBER (numberOfMonths). No optional params.
3. Negative numberOfMonths subtracts that number of months from the base date.
4. Time value in the input is NOT taken into account — output is always a date without time.
5. Output format follows application settings.
6. Runtime error when: date exceeds days in that month; incorrect month; h/m/s in > 2 digits; year > 4 digits.

CANONICAL_EXAMPLES:
```deluge
currentDate = '01-Jan-2019';
newDate = currentDate.edate(11); // → '01-Dec-2019'

currentDateTime = '01-Jan-2019 15:00:00';
newDateTime = currentDateTime.edate(13); // → '01-Feb-2020' (time stripped from output)

// Functional form
newDate = edate('01-Jan-2019', 11); // → '01-Dec-2019'

// Negative N subtracts months
prev = '01-Mar-2019'.edate(-2); // → '01-Jan-2019'
```

FAILURE_MODES:
- Time component in input is silently dropped from output (not preserved)
- Date exceeds days in that month → runtime error
- Incorrect month string → runtime error
- Hour/min/sec in > 2 digits → runtime error
- Year in > 4 digits → runtime error

RELATED_DOCS:
- addMonth() — ../date-time/../date-time/add-sub-month.dou.md
- subMonth() — ../date-time/../date-time/add-sub-month.dou.md
- Date-time data type — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/edate.html
