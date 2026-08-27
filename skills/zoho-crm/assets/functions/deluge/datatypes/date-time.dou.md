FILE_PURPOSE: Deluge Date-Time datatype — single-quoted date and time values with 40+ format support
MENTAL_MODEL: Date-Time = single-quoted temporal literal; missing time defaults to 00:00:00; 40+ formats supported

WHEN_TO_USE:
- Store, compare, or perform arithmetic on date/time values in Deluge Functions.
- Read or write CRM date/date-time fields via API responses.

WHEN_NOT_TO_USE:
- String representation of a date for display only — use Text datatype.

TRIGGER_KEYWORDS:
date-time datatype, single-quote date, dd-MMM-yyyy, yyyy-MM-dd, MM-dd-yyyy, date default 00:00:00, date format mismatch

RULES:
- Date-time literals must be enclosed in single quotes (not double quotes).
- A date without a time component defaults to `00:00:00` time.
- 40+ date formats are supported; if specified format cannot be auto-converted, an error is thrown.
- Key supported formats: `dd-MMM-yyyy`, `yyyy-MM-dd`, `MM-dd-yyyy`, `dd/MM/yyyy`, `MM/dd/yyyy`, `dd MMM yyyy`.
- Format mismatch: Deluge attempts to convert to the closest supported format; if conversion fails, error is thrown.

CANONICAL_EXAMPLES:
```deluge
date1 = '15-Aug-1947';             // time defaults to 00:00:00
appt  = '15-Aug-1947 19:00:00';    // explicit time
iso   = '1947-08-15';              // yyyy-MM-dd format
```

FAILURE_MODES:
- Date-time literal in double quotes (`"15-Aug-1947"`) → interpreted as Text; date built-in functions fail.
- Format not matching any supported format and not auto-convertible → error.
- Date without time silently defaults to `00:00:00`; time-aware comparisons on date-only values produce unexpected results.

RELATED_DOCS:
- Date-Time built-in functions — https://www.zoho.com/deluge/help/datatypes/date-time.html

SOURCE:
https://www.zoho.com/deluge/help/datatypes/date-time.html
