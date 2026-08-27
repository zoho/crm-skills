FILE_PURPOSE: Deluge `toHex()` — convert a NUMBER to its hexadecimal string representation.
MENTAL_MODEL: `num.toHex()` = TEXT containing the hex representation of the integer `num`.

WHEN_TO_USE:
- Convert an integer NUMBER to its hexadecimal representation for hex-based encoding or display.

WHEN_NOT_TO_USE:
- When encoding a TEXT string to hex — use `textToHex()` instead.
- When the input is a DECIMAL — input type is NUMBER only.

TRIGGER_KEYWORDS:
toHex(), number to hex, integer hex conversion, hex-string output, toHex number

RULES:
- Return type: TEXT.
- Input type: NUMBER.
- Both `<number>.toHex()` and `toHex(<number>)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
number = 100;
hexValue = number.toHex();  // returns "64"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- textToHex — ../text/../text/textToHex.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/tohex.html
