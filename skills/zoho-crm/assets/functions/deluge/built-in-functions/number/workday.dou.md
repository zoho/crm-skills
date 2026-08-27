FILE_PURPOSE: Deluge `workday()` — add business days to DATE-TIME with optional weekend and holiday lists.

MENTAL_MODEL: `dt.workday(n, [weekends], [holidays])` = DATE-TIME n business days ahead; n < 0 returns dt unchanged.

WHEN_TO_USE:
- Calculating a deadline N business days from a given date
- Custom weekend or holiday configurations needed for business-day arithmetic

WHEN_NOT_TO_USE:
- Need to add calendar days (not business) → use addDay()
- Need to subtract business days → workday() does not go backward (use subBusinessDay())
- Need count of business days between two dates → use workDaysBetween()

TRIGGER_KEYWORDS: workday(), add-business-days, workday-weekends-param, workday-holidays-param, negative-numberOfBusinessDays-no-op

RULES:
1. Return type: DATE-TIME (date only — time component not taken into account).
2. Params: DATE-TIME (start), NUMBER (numberOfBusinessDays), optional COLLECTION<TEXT> (weekends), optional COLLECTION<DATE> (holidays).
3. Default weekends: {"Saturday", "Sunday"}. Override by passing a custom weekends COLLECTION.
4. Default holidays: empty — any non-weekend day is a working day if no holidays provided.
5. CRITICAL: A negative numberOfBusinessDays returns the input date unchanged (does NOT subtract business days).
6. Runtime error when: h/m/s in > 2 digits; date exceeds days in month; incorrect month; year > 4 digits.

CANONICAL_EXAMPLES:
```deluge
// 15-Mar-2019 is Friday; +1 business day → Monday 18-Mar-2019
newDate = '15-Mar-2019'.workday(1); // → '18-Mar-2019'

// Custom weekend (Sunday only) with holiday list
// Assuming current date is 23-May-2020
newDate = zoho.currentdate.workday(5, {"Sunday"}, {'25-May-2020'}); // → '30-May-2020'

// Functional form
newDate = workday('15-Mar-2019', 1); // → '18-Mar-2019'

// Negative N returns input unchanged — does NOT go backward
same = '15-Mar-2019'.workday(-3); // → '15-Mar-2019' (not 12-Mar)
```

FAILURE_MODES:
- Negative numberOfBusinessDays does NOT subtract business days — returns input date unchanged
- Date exceeds days in that month → runtime error
- Hour/min/sec in > 2 digits → runtime error
- Incorrect month → runtime error
- Year in > 4 digits → runtime error

RELATED_DOCS:
- addBusinessDay() — ../date-time/../date-time/add-sub-business-day.dou.md
- subBusinessDay() — https://www.zoho.com/deluge/help/functions/datetime/subbusinessday.html
- workDaysBetween() — https://www.zoho.com/deluge/help/functions/datetime/workdaysbetween.html
- Date-time data type — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/workday.html
