FILE_PURPOSE: Deluge `toDateTimeString()` — convert Unix epoch milliseconds to formatted TEXT with timezone.

MENTAL_MODEL: `toDateTimeString(epochMs, fmt, tz)` = TEXT; input is NUMBER (ms); inverse of unixEpoch().

WHEN_TO_USE:
- Converting a Unix timestamp (milliseconds) to a human-readable or service-compatible date string
- Formatting an epoch value in a specific timezone or date-time pattern

WHEN_NOT_TO_USE:
- Input is a DATE-TIME or TEXT date (not epoch ms) → use toString() / toText() instead
- Need the reverse (date text → epoch ms) → use unixEpoch()

TRIGGER_KEYWORDS: toDateTimeString(), unix-epoch-to-text, epoch-milliseconds-input, dateTimeFormat-literal, TZ-database-conversion

RULES:
1. Return type: TEXT.
2. Input: NUMBER (epochMs — Unix timestamp in milliseconds ONLY).
3. Epoch 0 = 01-Jan-1970 00:00:00 UTC. Each +1000 adds one second; each -1000 subtracts one second.
4. dateTimeFormat param: datetime pattern literals — y (year), M (month), d (day), H (hour 0-23), h (hour 1-12), m (minute), s (second), z (timezone), E (day name), a (am/pm). Optional; defaults to application settings if omitted.
5. timeZone param: TZ database name (e.g. "IST", "UTC+8", "America/New_York", "GMT+5:30").
6. DST is applied automatically wherever applicable.
7. Output (month names, timezone labels, day names) is always in English regardless of user locale.
8. Applicable to all Zoho services.

CANONICAL_EXAMPLES:
```deluge
ctime = 1693905560373; // Unix ms timestamp

result = toDateTimeString(ctime, "MMM dd, yy 'at' hh:mm:ss z, E", "IST");
// → "Sep 05, 23 at 02:49:20 IST, Tue"

// Dot notation
result = ctime.toDateTimeString("dd-MMM-yyyy HH:mm:ss", "UTC+8");

// Epoch 0 = Unix origin
result = toDateTimeString(0, "dd-MMM-yyyy HH:mm:ss", "GMT"); // → "01-Jan-1970 00:00:00"
```

FAILURE_MODES:
- Passing epoch in seconds (not milliseconds) → result off by factor of 1000
- Passing TEXT or DATE-TIME as input instead of NUMBER → not the intended use; behavior not documented
- Invalid TZ database name → behavior not documented in source; validate TZ string before use
- Unsupported format literal in dateTimeFormat → output unpredictable

RELATED_DOCS:
- unixEpoch() (inverse: date text → epoch ms) — ../number/../number/unixEpoch.dou.md
- toString() — toString-toText.dou.md
- toDateTime() — https://www.zoho.com/deluge/help/functions/common/to-date-time.html
- Date-time data type — ../../datatypes/date-time.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/common/todatetimestring.html
