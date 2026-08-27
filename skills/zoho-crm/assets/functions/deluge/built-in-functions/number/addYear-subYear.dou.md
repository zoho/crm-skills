FILE_PURPOSE: Deluge `addYear()` / `subYear()` — shift a DATE-TIME forward or backward by years.
MENTAL_MODEL: `dt.addYear(n)` = dt + n years; `dt.subYear(n)` = dt − n years; negative n reverses direction.

WHEN_TO_USE:
- Advance a DATE-TIME by a number of years.
- Move a DATE-TIME backwards by a number of years.

WHEN_NOT_TO_USE:
- On TIME values — both functions accept DATE-TIME only.

TRIGGER_KEYWORDS:
addYear(), subYear(), year-arithmetic, datetime-app-settings, datetime-00-default, negative-reverses-direction

RULES:
- Return type: DATE-TIME; input: DATE-TIME (dateTimeValue), NUMBER (numberOfYears).
  Note: addYear and subYear source parameter tables list `<variable>` type as "NUMBER" but the Return Type heading states "Date-Time" and the variable description says "returned date-time value"; examples confirm DATE-TIME output.
- Output formatted per Application Settings.
- DATE-TIME input without time component defaults to 00:00:00.
- Negative `numberOfYears` reverses direction: `addYear(-n)` = `subYear(n)` and vice versa.
- Auto-correction (no error raised): hour ≥ 24 → resets to 00:00:00; minutes ≥ 60 → resets mm:ss to 00:00; seconds ≥ 60 → resets ss to 00.
- Runtime errors: hour/minute/second specified in more than 2 digits; date exceeds days in month; year has more than 4 digits.

CANONICAL_EXAMPLES:
```deluge
currentDate     = '01-Jan-2019';
currentDateTime = '01-Jan-2019 15:00:00';

newDate     = currentDate.addYear(100);        // returns '01-Jan-2119 00:00:00'
newDateTime = currentDateTime.addYear(10);     // returns '01-Jan-2029 15:00:00'

currentDate2 = '01-Jan-2019';
newDate2 = currentDate2.subYear(1);            // returns '01-Jan-2018 00:00:00'
```

FAILURE_MODES:
- Runtime error when: hour/minute/second specified in more than 2 digits; date exceeds days in month; year has more than 4 digits.

RELATED_DOCS:
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/addyear.html, https://www.zoho.com/deluge/help/functions/datetime/subyear.html
