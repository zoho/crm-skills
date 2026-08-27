FILE_PURPOSE: Deluge `textToHex()` — encode a text string to its hexadecimal representation.
MENTAL_MODEL: `str.textToHex()` = hex-encoded TEXT; inverse of `hexToText()`.

WHEN_TO_USE:
- Encode a text string to its hexadecimal representation for transmission or storage.

WHEN_NOT_TO_USE:
- When decoding hex back to text — use `hexToText()` instead.

TRIGGER_KEYWORDS:
textToHex(), text-to-hex encoding, hexToText inverse, hex-string encode, hex-literal output

RULES:
- Return type: TEXT (hexadecimal string).
- Input type: TEXT.
- Both `<text>.textToHex()` and `textToHex(<text>)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
response = textToHex("Zoho CRM");  // Returns "5a6f686f2043524d"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- hexToText — hexToText.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/texttohex.html
