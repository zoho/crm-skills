FILE_PURPOSE: Deluge `hour()` / `minute()` / `second()` — get hour, minute, second from a DATE-TIME value.
MENTAL_MODEL: `dt.hour()` = 0–23; `dt.minute()` = 0–59; `dt.second()` = 0–59.

WHEN_TO_USE:
- Extract the hour, minute, or second component as a NUMBER from a DATE-TIME value.

WHEN_NOT_TO_USE:
- Need week or day number — use getWeekOfYear() or day() instead.

TRIGGER_KEYWORDS:
hour(), minute(), second(), getHour(), getMinutes(), getSeconds()

RULES:
- All three return type: NUMBER; input: DATE-TIME.
- Aliases: `hour()` = `getHour()`; `minute()` = `getMinutes()`; `second()` = `getSeconds()`.
- DATE-TIME without time component defaults to 00:00:00 (returns 0 for all three).
- DATE-TIME runtime errors: hour/minute/second in more than 2 digits; date exceeds days in month; year more than 4 digits.

CANONICAL_EXAMPLES:
```deluge
// DATE-TIME examples
currentDate = '01-Jan-2019';
info currentDate.getHour();     // Returns 00
info currentDate.getMinutes();  // Returns 00
info currentDate.getSeconds();  // Returns 00

currentDate = '01-Jan-2019 23:15:10';
info currentDate.hour();        // Returns 23
info currentDate.minute();      // Returns 15
info currentDate.second();      // Returns 10


```

FAILURE_MODES:
- DATE-TIME with hour/minute/second in more than 2 digits throws runtime error.

RELATED_DOCS:
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/hour.html, https://www.zoho.com/deluge/help/functions/datetime/minute.html, https://www.zoho.com/deluge/help/functions/datetime/second.html, https://www.zoho.com/deluge/help/functions/datetime/gethour.html, https://www.zoho.com/deluge/help/functions/datetime/getminutes.html, https://www.zoho.com/deluge/help/functions/datetime/getseconds.html
