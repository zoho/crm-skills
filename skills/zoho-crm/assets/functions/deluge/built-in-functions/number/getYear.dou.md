FILE_PURPOSE: Deluge `getYear()` — extract year as NUMBER from a DATE-TIME value; alias `year()`.

MENTAL_MODEL: `dt.getYear()` = 4-digit year NUMBER; time component ignored; `year()` is an alias.

WHEN_TO_USE:
- Need the year component from a DATE-TIME value
- Year-based comparisons, grouping, or arithmetic

WHEN_NOT_TO_USE:
- Need month → use getMonth() / month()
- Need day-of-month → use getDay() / day()
- Need day-of-year → use getDayOfYear()

TRIGGER_KEYWORDS: getYear(), year(), datetime-year-extract, getYear-alias, null-invalid-datetime-format

RULES:
1. Return type: NUMBER (the 4-digit year, e.g., 2019).
2. Input: DATE-TIME only — no TIME variant. Time component is NOT taken into account.
3. Aliases: getYear() and year() are equivalent; both forms supported.
4. Returns NULL (not error) when: month is < 3 chars; hour/min/sec is > 2 digits; date is > 2 digits; year is > 4 digits.
5. Runtime error when: 2-digit date exceeds days in the month; month specified in 3+ chars but incorrect.

CANONICAL_EXAMPLES:
// Dot notation
currentDate = '01-Jan-2019';
yearVal = currentDate.getYear(); // → 2019

// Alias form
yearVal = '01-Jan-2019'.year(); // → 2019

// Functional form
yearVal = getYear('01-Jan-2019'); // → 2019

// Time component is ignored
yearVal = '01-Jan-2019 23:59:59'.getYear(); // → 2019

FAILURE_MODES:
- Month in < 3 chars (e.g., '01-Ja-2019') → null, not error
- Hour/min/sec in > 2 digits → null
- Date in > 2 digits → null
- Year in > 4 digits → null
- 2-digit date exceeds days in month → runtime error
- Incorrect month string (3+ chars) → runtime error
- Calling on a TIME value → not supported (no TIME variant)

RELATED_DOCS:
- getDay() / day() — day-month.dou.md
- getMonth() / month() — day-month.dou.md
- getDayOfYear() — getDayOfYear.dou.md
- Date-time data type — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/getYear.html
