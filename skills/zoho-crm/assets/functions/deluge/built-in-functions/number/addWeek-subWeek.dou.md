FILE_PURPOSE: Deluge `addWeek()` / `subWeek()` — shift a DATE-TIME forward or backward by weeks.
MENTAL_MODEL: `dt.addWeek(n)` = dt + n×7 days; `dt.subWeek(n)` = dt − n×7 days; negative n reverses direction.

WHEN_TO_USE:
- Advance a DATE-TIME by a number of whole weeks.
- Move a DATE-TIME backwards by a number of whole weeks.

WHEN_NOT_TO_USE:
- On TIME values — both functions accept DATE-TIME only.

TRIGGER_KEYWORDS:
addWeek(), subWeek(), week-arithmetic, datetime-app-settings, datetime-00-default, negative-reverses-direction

RULES:
- Return type: DATE-TIME; input: DATE-TIME (dateTimeValue), NUMBER (numberOfWeeks).
  Note: addWeek() Return Type section states "Number" — documentation error; examples output DATE-TIME (e.g., '12-Mar-2019 00:00:00'), subWeek() correctly states "Date-Time", and variable description says "returned date-time value". DATE-TIME confirmed authoritative.
- `numberOfWeeks` is the number of weeks (not minutes); subWeek() param description stating "minutes" is a source copy-paste error. Function name, overview, and addWeek() confirm weeks.
- Output formatted per Application Settings.
- DATE-TIME input without time component defaults to 00:00:00.
- Negative `numberOfWeeks` reverses direction: `addWeek(-n)` = `subWeek(n)` and vice versa.
- Auto-correction (no error raised): hour ≥ 24 → resets to 00:00:00; minutes ≥ 60 → resets mm:ss to 00:00; seconds ≥ 60 → resets ss to 00.
- Runtime errors: hour/minute/second specified in more than 2 digits; date exceeds days in month; year has more than 4 digits.

CANONICAL_EXAMPLES:
```deluge
currentDate     = '01-Jan-2019';
currentDateTime = '01-Jan-2019 15:00:00';

newDate     = currentDate.addWeek(10);         // returns '12-Mar-2019 00:00:00'
newDateTime = currentDateTime.addWeek(55);     // returns '21-Jan-2020 15:00:00'

currentDate2 = '01-May-2019';
newDate2 = currentDate2.subWeek(4);            // returns '03-Apr-2019 00:00:00'
```

FAILURE_MODES:
- Runtime error when: hour/minute/second specified in more than 2 digits; date exceeds days in month; year has more than 4 digits.

RELATED_DOCS:
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/addweek.html, https://www.zoho.com/deluge/help/functions/datetime/subweek.html
