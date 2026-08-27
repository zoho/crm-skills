FILE_PURPOSE: Deluge `getDayOfYear()` — get day-of-year NUMBER (1–366) from a DATE-TIME value.

MENTAL_MODEL: `dt.getDayOfYear()` = 1–365 (normal year) or 1–366 (leap year); no alias; time defaults 00:00:00.

WHEN_TO_USE:
- Need the ordinal day of year (1-based) from a DATE-TIME value
- Calculating whether a year is a leap year (getDayOfYear('31-Dec-YYYY') == 366)
- Comparing Julian day positions across dates within a year

WHEN_NOT_TO_USE:
- Need day-of-month → use getDay() / day()
- Need day-of-week → use weekday() / getDayOfWeek()
- Need week-of-year → use getWeekOfYear()

TRIGGER_KEYWORDS: getDayOfYear(), day-of-year, leap-year-366, datetime-ordinal, null-invalid-datetime-format

RULES:
1. Return type: NUMBER (1–365 for non-leap years; 1–366 for leap years).
2. Input: DATE-TIME only — no TIME variant exists.
3. If no time component is provided, defaults to 00:00:00.
4. Returns NULL (not error) when: month is < 3 chars; hour/min/sec is > 2 digits; date is > 2 digits; year is > 4 digits.
5. Runtime error when: 2-digit date exceeds days in the month; month specified in 3+ chars but incorrect.
6. No alias — only getDayOfYear() syntax (no shorthand like dayOfYear()).

CANONICAL_EXAMPLES:
// Day 366 of a leap year (2020)
result = '31-Dec-2020'.getDayOfYear(); // → 366

// Functional form
result = getDayOfYear('31-Dec-2020'); // → 366

// Jan 1 always returns 1
result = '01-Jan-2021'.getDayOfYear(); // → 1

// No time provided — defaults to 00:00:00
result = '15-Jun-2023'.getDayOfYear(); // → 166

FAILURE_MODES:
- Month in < 3 chars (e.g., '01-Ja-2019') → null, not an error
- Hour/min/sec in > 2 digits → null
- Date in > 2 digits → null
- Year in > 4 digits → null
- 2-digit date exceeds days in that month → runtime error
- Incorrect month string (3+ chars) → runtime error
- Calling on a TIME value → not supported (no TIME variant)

RELATED_DOCS:
- getDay() / day() — day-month.dou.md
- getWeekOfYear() — getWeekOfYear.dou.md
- weekday() / getDayOfWeek() — weekday.dou.md
- Date-time data type — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/getdayofyear.html
