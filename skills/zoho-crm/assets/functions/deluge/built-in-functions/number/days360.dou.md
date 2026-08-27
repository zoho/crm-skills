FILE_PURPOSE: Deluge `days360()` — count days between two DATE-TIME values; equivalent to `daysBetween()`.

MENTAL_MODEL: `start.days360(end)` = NUMBER of calendar days between dates; identical to `daysBetween()`.

WHEN_TO_USE:
- Need the number of calendar days between two dates
- Computing date intervals or duration in days

WHEN_NOT_TO_USE:
- Need business days only → use workDaysBetween()
- Need hours between → use hoursBetween()
- Need months between → use monthsBetween()

TRIGGER_KEYWORDS: days360(), daysBetween-equivalent, date-interval-days, two-datetime-params, days360-runtime-validation

RULES:
1. Return type: NUMBER (days between startDateTimeValue and endDateTimeValue).
2. Params: DATE-TIME (start), DATE-TIME (end). Both required; no optional params.
3. Exactly equivalent to daysBetween() — both functions behave identically.
4. Despite the name, days360() is NOT a 360-day financial year calculator — it counts actual calendar days.
5. Runtime error when: hour/min/sec in > 2 digits; date exceeds days in the month; incorrect month; year > 4 digits.

CANONICAL_EXAMPLES:
// Dot notation
startDate = '31-Dec-1989';
endDate = '01-Jan-1990';
n = startDate.days360(endDate); // → 1

// Functional form
n = days360('31-Dec-1989', '01-Jan-1990'); // → 1

// Equivalent daysBetween call — same result
n = daysBetween('31-Dec-1989', '01-Jan-1990'); // → 1

FAILURE_MODES:
- Expecting Excel-style 360-day year behavior — Deluge days360() counts actual calendar days, not a 360-day year
- Hour/min/sec in > 2 digits → runtime error
- Date exceeds days in that month → runtime error
- Incorrect month → runtime error
- Year in > 4 digits → runtime error

RELATED_DOCS:
- daysBetween() (identical behavior) — ../date-time/../date-time/days-hours-between.dou.md
- workDaysBetween() — https://www.zoho.com/deluge/help/functions/datetime/workdaysbetween.html
- hoursBetween() — ../date-time/../date-time/days-hours-between.dou.md
- monthsBetween() — ../date-time/../date-time/months-years-between.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/days360.html
