FILE_PURPOSE: Deluge `getWeekOfYear()` — get week-of-year NUMBER (1–52) with optional start-day override.

MENTAL_MODEL: `dt.getWeekOfYear([start_day])` = 1–52; default start Sunday.

WHEN_TO_USE:
- Need the week number for a date within the year
- Grouping or comparing dates by week number
- Custom fiscal-week calculations where week start differs from Sunday

WHEN_NOT_TO_USE:
- Need day-of-week → use weekday() / getDayOfWeek()
- Need day-of-year → use getDayOfYear()
TRIGGER_KEYWORDS: getWeekOfYear(), week-of-year, start_day-optional, Sunday-default-start

RULES:
1. Return type: NUMBER (1–52 representing the week number within the year).
2. Input: DATE-TIME. Optional second param [start_day] TEXT (default: "Sunday").
3. Weeks start from Sunday by default; dates from the previous year that fall in the first week of the new year return 1.
4. Returns NULL (not error) when: month is < 3 chars; hour/min/sec is > 2 digits; date is > 2 digits; year is > 4 digits.
5. Runtime error when: 2-digit date exceeds days in the month; month specified in 3+ chars but incorrect.

CANONICAL_EXAMPLES:
// Week 7 of 2021 (default Sunday start)
weekNum = '7-Feb-2021'.getWeekOfYear(); // → 7

// Functional form with Monday start 
weekNum = getWeekOfYear('7-Feb-2021', "Monday"); // → 6

// Dot notation with Monday start
weekNum = '7-Feb-2021'.getWeekOfYear("Monday"); // → 6

// Previous year's date in first week of new year returns 1
weekNum = '01-Jan-2023'.getWeekOfYear(); // → 1

FAILURE_MODES:
- Month in < 3 chars → null
- Hour/min/sec in > 2 digits → null
- Date in > 2 digits → null
- Year in > 4 digits → null
- 2-digit date exceeds days in month → runtime error
- Incorrect month string (3+ chars) → runtime error

RELATED_DOCS:
- getDayOfYear() — getDayOfYear.dou.md
- weekday() / getDayOfWeek() — weekday.dou.md
- Date-time data type — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/getweekofyear.html
