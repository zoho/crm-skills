FILE_PURPOSE: Deluge `unixEpoch()` — convert a TEXT date to Unix milliseconds since 1970-01-01 UTC.

MENTAL_MODEL: `dateText.unixEpoch([tz])` = milliseconds since epoch; input must be TEXT; invalid TZ defaults GMT.

WHEN_TO_USE:
- Need a Unix timestamp (milliseconds) from a date string for external system interop
- Timezone-aware epoch conversion from a known date-time text

WHEN_NOT_TO_USE:
- Input is a DATE-TIME typed variable → must convert to TEXT first (via toString())
- Need to reverse the operation (epoch → formatted date string) → use toDateTimeString()

TRIGGER_KEYWORDS: unixEpoch(), unix-milliseconds, text-only-input, TZ-database-key, invalid-TZ-defaults-GMT

RULES:
1. Return type: NUMBER (milliseconds elapsed since 1970-01-01 00:00:00 UTC).
2. Input: TEXT (dateText), optional TEXT (timeZone — TZ database name e.g. "Asia/Calcutta", "GMT+5:30", "EST").
3. CRITICAL: Input MUST be TEXT format. Passing a DATE-TIME typed value (single-quoted literal or DATE-TIME variable) → runtime error.
4. No timezone or invalid timezone → silently defaults to GMT (no error thrown).
5. If the function cannot recognize the datetime string → returns the input value as text (no error, no ms returned).
6. Leap seconds are NOT included in elapsed time.

CANONICAL_EXAMPLES:
```deluge
currentDate = "03-Feb-2020 03:48:12"; // TEXT (double-quoted)

indiaTime  = currentDate.unixEpoch("Asia/Calcutta"); // → 1580681892000
gmtMinus8  = currentDate.unixEpoch("GMT-8");         // → 1580730492000
defaultGMT = currentDate.unixEpoch();                // → 1580730492000 (defaults to GMT)
utcPlus8   = currentDate.unixEpoch("UTC+8");         // → 1580701692000
indiaGMT   = currentDate.unixEpoch("GMT+5:30");      // → 1580681892000

// Invalid timezone → silently defaults to GMT
invalidTZ = currentDate.unixEpoch("Hello"); // → 1580730492000

// DATE-TIME typed literal (single-quoted) → runtime error
// '03-Feb-2020 03:48:12'.unixEpoch("GMT") → runtime error
```

FAILURE_MODES:
- Single-quoted date literal or DATE-TIME variable as input → runtime error (TEXT required)
- Invalid timezone string → silently defaults to GMT; no error raised
- Unrecognized datetime format in TEXT → returns original text, not milliseconds
- Leap seconds not counted; results near leap-second boundaries differ from strict UTC

RELATED_DOCS:
- toDateTimeString() (inverse: epoch ms → text) — https://www.zoho.com/deluge/help/functions/datetime/todatetimestring.html
- Date-time data type — ../../datatypes/date-time.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/datetime/unix-epoch.html
