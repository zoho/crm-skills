FILE_PURPOSE: Deluge `day()` / `month()` — extract day-of-month or month NUMBER from DATE-TIME.
MENTAL_MODEL: `dt.day()` = day-of-month NUMBER; `dt.month()` = month NUMBER (1–12); both have getDay/getMonth aliases.

WHEN_TO_USE:
- Extract the day-of-month integer from a DATE-TIME value.
- Extract the month number (1–12) from a DATE-TIME value.

WHEN_NOT_TO_USE:
- When null from malformed input is not guarded — certain invalid formats return null silently rather than raising errors.

TRIGGER_KEYWORDS:
day(), month(), getDay(), getMonth(), day-of-month, month-number, null-invalid-format

RULES:
- Both return type: NUMBER; input: DATE-TIME.
- `day()` and `getDay()` are aliases; `month()` and `getMonth()` are aliases.
- Runtime errors (NOT null): 2-digit date exceeds days in that month; incorrect month value specified in 3 or more characters.
- Returns null (no runtime error) when: month value specified in fewer than 3 characters; hour/minute/second in more than 2 digits; date in more than 2 digits; year has more than 4 digits.

CANONICAL_EXAMPLES:
```deluge
currentDate = '01-Jan-2019';
date = currentDate.day();             // returns 1

currentDate2 = '14-Dec-2023';
monthNumber = currentDate2.month();
info monthNumber;                     // returns 12
```

FAILURE_MODES:
- Returns null (no error) when: month specified in fewer than 3 characters; time components in more than 2 digits; date in more than 2 digits; year in more than 4 digits.
- Runtime error (not null) when: date value exceeds days in month; incorrect month value given in 3+ characters.

RELATED_DOCS:
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/day.html, https://www.zoho.com/deluge/help/functions/datetime/month.html, https://www.zoho.com/deluge/help/functions/datetime/getday.html, https://www.zoho.com/deluge/help/functions/datetime/getmonth.html
