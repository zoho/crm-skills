FILE_PURPOSE: Deluge `weekday()` — get day-of-week NUMBER (1=Sunday, 7=Saturday) from DATE-TIME.

MENTAL_MODEL: `dt.weekday()` = 1 (Sun) through 7 (Sat); time ignored; alias: `getDayOfWeek()`.

WHEN_TO_USE:
- Need a numeric day-of-week from a DATE-TIME (1-based, Sunday=1)
- Conditional logic based on whether a date is a weekday or weekend
- Scheduling checks for specific weekdays

WHEN_NOT_TO_USE:
- Need week-of-year number → use getWeekOfYear()
- Need day-of-month → use getDay() / day()
- Need next/previous business day → use nextWeekDay() / previousWeekDay()

TRIGGER_KEYWORDS: weekday(), getDayOfWeek(), day-of-week-number, Sunday-equals-1, Saturday-equals-7

RULES:
1. Return type: NUMBER — 1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday.
2. Input: DATE-TIME only. Time component is NOT taken into account.
3. Aliases: weekday() and getDayOfWeek() are equivalent.
4. Returns NULL (not error) when: month is < 3 chars; hour/min/sec is > 2 digits; date is > 2 digits; year is > 4 digits.
5. Runtime error when: 2-digit date exceeds days in the month; month specified in 3+ chars but incorrect.

CANONICAL_EXAMPLES:
// 15-Mar-2019 is Friday → returns 6
dayNum = '15-Mar-2019'.weekday(); // → 6

// Alias getDayOfWeek()
dayNum = '15-Mar-2019'.getDayOfWeek(); // → 6

// Functional form
dayNum = weekday('15-Mar-2019'); // → 6

// Weekend check: 1=Sunday, 7=Saturday
dayNum = today.weekday();
if (dayNum == 1 || dayNum == 7) { /* weekend */ }

FAILURE_MODES:
- Expecting day name strings — function returns NUMBER 1–7, not "Monday" etc.
- Off-by-one: Deluge convention is 1=Sunday, NOT 0=Sunday or 1=Monday
- Month in < 3 chars → null
- Hour/min/sec in > 2 digits → null
- Date in > 2 digits → null
- Year in > 4 digits → null
- 2-digit date exceeds days in month → runtime error
- Incorrect month string (3+ chars) → runtime error

RELATED_DOCS:
- getWeekOfYear() — getWeekOfYear.dou.md
- getDayOfYear() — getDayOfYear.dou.md
- nextWeekDay() — https://www.zoho.com/deluge/help/functions/datetime/nextweekday.html
- Date-time data type — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/weekday.html
