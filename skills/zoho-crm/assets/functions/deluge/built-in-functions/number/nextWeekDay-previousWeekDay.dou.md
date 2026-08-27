FILE_PURPOSE: Deluge `nextWeekDay()` / `previousWeekDay()` — seek next or previous date by weekday name.

MENTAL_MODEL: `dt.nextWeekDay(day)` = next date on that weekday; `.previousWeekDay(day)` = previous date on that weekday.

WHEN_TO_USE:
- Finding the next or previous occurrence of a specific named weekday from a date
- Scheduling or calendar calculations targeting a named day (including weekends)

WHEN_NOT_TO_USE:
- Need to add N business days → use workday() / addBusinessDay()
- Need day-of-week number for a date → use weekday() / getDayOfWeek()

TRIGGER_KEYWORDS: nextWeekDay(), previousWeekDay(), inputDay-weekday-label, non-business-day, day-of-week-seek

RULES:
1. FLAG: return type contradiction in source — Return Type section states TEXT; parameter table states DATE-TIME.
   Candidates:
     a) Return type is TEXT (Return Type header is authoritative).
     b) Return type is DATE-TIME (parameter table entry is authoritative).
2. Input: DATE-TIME (inputDate), TEXT (inputDay — one of: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday).
3. NOT related to business days — inputDay can be any weekday including Saturday and Sunday.
4. nextWeekDay(): if inputDate already falls on inputDay, returns the NEXT occurrence (inputDate itself is NOT returned).
5. previousWeekDay(): if inputDate already falls on inputDay, returns the PREVIOUS occurrence (inputDate itself is NOT returned).

CANONICAL_EXAMPLES:
```deluge
// nextWeekDay: current date 20-Jul-2021 (Tuesday) → next Monday
info zoho.currentdate.nextWeekDay("Monday"); // → 26-Jul-2021

// Same-day: 20-Jul-2021 (Tuesday).nextWeekDay("Tuesday") → next Tuesday, not same day
inputDate = '20-Jul-2021';
info inputDate.nextWeekDay("Tuesday"); // → 27-Jul-2021

// previousWeekDay: current date 21-Jul-2021 (Wednesday) → previous Monday
info zoho.currentdate.previousWeekDay("Monday"); // → 19-Jul-2021

// Same-day: 21-Jul-2021 (Wednesday).previousWeekDay("Wednesday") → previous Wednesday
inputDate = '21-Jul-2021';
info inputDate.previousWeekDay("Wednesday"); // → 14-Jul-2021
```

FAILURE_MODES:
- Return type ambiguity — source documents both TEXT and DATE-TIME; resolve FLAG before chaining operations
- Calling nextWeekDay("Monday") when inputDate is already Monday → returns NEXT Monday, not inputDate
- Calling previousWeekDay("Monday") when inputDate is already Monday → returns PREVIOUS Monday, not inputDate
- inputDay value outside allowed list (Sunday–Saturday) → behavior not documented in source

RELATED_DOCS:
- weekday() / getDayOfWeek() — weekday.dou.md
- workday() — workday.dou.md
- Date-time built-in functions — https://www.zoho.com/deluge/help/functions/date-time.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/nextWeekDay.html, https://www.zoho.com/deluge/help/functions/number/previousWeekDay.html
