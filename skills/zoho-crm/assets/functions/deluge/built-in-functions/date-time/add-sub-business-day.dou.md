## FILE_PURPOSE
Deluge addBusinessDay() and subBusinessDay() — advance or retreat a date by business days.

## MENTAL_MODEL
addBusinessDay/subBusinessDay(date, n, weekends, holidays) = DATE-TIME skipping non-business days.

## WHEN_TO_USE
- Advance a date-time by a number of business days, skipping weekends and optional holidays.
- Retreat a date-time by a number of business days, skipping weekends and optional holidays.

## WHEN_NOT_TO_USE
- Simple calendar day arithmetic that should not skip weekends — use addDay()/subDay() instead.
- Hourly business-time calculations — use addBusinessHour() instead.

## TRIGGER_KEYWORDS
addBusinessDay, subBusinessDay, numberOfBusinessDays, weekends collection, holidays collection, business day skip

## RULES
- addBusinessDay() syntax: `<var> = <dateTimeValue>.addBusinessDay(<n>[, <weekends>[, <holidays>]]);`
  or `addBusinessDay(<dateTimeValue>, <n>[, <weekends>[, <holidays>]])`.
- subBusinessDay() syntax: `<var> = <dateTimeValue>.subBusinessDay(<n>[, <weekends>[, <holidays>]]);`
  or `subBusinessDay(<dateTimeValue>, <n>[, <weekends>[, <holidays>]])`.
- Both functions return DATE-TIME.
- Default business days: Monday–Friday (weekends = Saturday and Sunday).
- `weekends` (optional) — COLLECTION OF TEXT; defaults to `{"Saturday", "Sunday"}`.
- `holidays` (optional) — COLLECTION OF DATES; if omitted, all non-weekend days are working days.
- Negative `numberOfBusinessDays` in addBusinessDay() → returns given date-time unchanged.
- Negative `numberOfBusinessDays` in subBusinessDay() → returns given date-time unchanged.
- subBusinessDay() only: `numberOfBusinessDays` cannot exceed 365.
- Date-time without a time component defaults to time 00:00:00.
- hour ≥ 24 → auto-reset to 00:00:00; minutes ≥ 60 → mm:ss reset to 00:00; seconds ≥ 60 → ss reset to 00.
- Return value format follows application settings.

## CANONICAL_EXAMPLES
```deluge
// addBusinessDay: Friday + 1 business day = next Monday
currentDate = '15-Mar-2019';
newDate = currentDate.addBusinessDay(1);          // returns '18-Mar-2019 00:00:00'

// addBusinessDay with custom weekends and a holiday
newDate = zoho.currentdate.addBusinessDay(5, {"Sunday"}, {'25-May-2020'});
// if starting from 23-May-2020, returns '30-May-2020 00:00:00'

// subBusinessDay: default weekends
info '21-Jul-2021'.subBusinessDay(5);             // returns '14-Jul-2021 00:00:00'

// subBusinessDay with custom weekends and holidays
info '21-Jul-2021'.subBusinessDay(5, {"Sunday"}, {'20-Jul-2021', '19-Jul-2021'});
// returns '13-Jul-2021 00:00:00'

// Negative n in addBusinessDay → returns date-time unchanged
info '15-Mar-2019'.addBusinessDay(-3);            // returns '15-Mar-2019 00:00:00'
```

## FAILURE_MODES
- Negative `numberOfBusinessDays` → returns the original date-time unchanged (no error thrown).
- subBusinessDay(): `numberOfBusinessDays` > 365 → runtime error.
- hour/minute/second value specified in more than 2 digits → runtime error.
- Date value exceeds the number of days in that month → runtime error.
- Incorrect month value → runtime error.
- Year value has more than 4 digits → runtime error.

## RELATED_DOCS
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html
- addDay — add-sub-day.dou.md
- addBusinessHour — https://www.zoho.com/deluge/help/functions/datetime/addbusinesshour.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/addbusinessday.html, https://www.zoho.com/deluge/help/functions/datetime/subBusinessDay.html
