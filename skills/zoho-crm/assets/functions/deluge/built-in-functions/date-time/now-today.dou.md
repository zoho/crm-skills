## FILE_PURPOSE
Deluge now and today — return the current date-time or current date-only value.

## MENTAL_MODEL
now = current DATE-TIME with time; today = current date with time forced to 00:00:00.

## WHEN_TO_USE
- Get the current date and time — use `now`.
- Get the current date with time component set to midnight — use `today`.

## WHEN_NOT_TO_USE
- Computing differences between dates — use daysBetween(), hoursBetween() etc. instead.

## TRIGGER_KEYWORDS
now, today, current datetime, current date no time, zoho.currentdate

## RULES
- `now` syntax: `<variable> = now;` — no parentheses, no arguments.
- `today` syntax: `<variable> = today;` — no parentheses, no arguments.
- Both return DATE-TIME.
- `now` returns the current date and time value.
- `today` returns the current date value with time component set to 00:00:00.
- Both return values in the format specified in application / service settings.
- Return format can be converted to a specific format and time zone using toString().

## CANONICAL_EXAMPLES
```deluge
currentDateTime = now;    // e.g. returns '23-Oct-2023 14:35:22' (current date-time)
currentDate     = today;  // e.g. returns '23-Oct-2023 00:00:00' (current date, time = 00:00:00)
```

## FAILURE_MODES
- `today()` called with parentheses → runtime error `Not able to find 'today' function`; `today` is a keyword (no parentheses), not a function call. Valid forms: `today` (returns current date with time 00:00:00) or `zoho.currentdate` (returns current date-only). Choose based on whether the time component is needed.

## RELATED_DOCS
- toString — ../conversion/../conversion/toString-toText.dou.md
- Date-time functions — https://www.zoho.com/deluge/help/functions/date-time.html

## SOURCE
https://www.zoho.com/deluge/help/functions/datetime/now.html, https://www.zoho.com/deluge/help/functions/datetime/today.html
