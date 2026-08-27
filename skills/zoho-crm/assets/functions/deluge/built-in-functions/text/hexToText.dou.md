FILE_PURPOSE: Deluge `hexToText()` — decode a hexadecimal-encoded string to its text equivalent.
MENTAL_MODEL: `hexStr.hexToText()` = TEXT; decodes hex-encoded bytes to their ASCII/text representation.

WHEN_TO_USE:
- Decode a hexadecimal-encoded string back to its human-readable text form.

WHEN_NOT_TO_USE:
- When converting text TO hex — use `textToHex()` instead.

TRIGGER_KEYWORDS:
hexToText(), hex decode, hexadecimal to text, hex literal decode, hex-string conversion, textToHex inverse

RULES:
- Return type: TEXT.
- Input type: TEXT (hexadecimal string).
- Both `<text>.hexToText()` and `hexToText(<text>)` syntaxes are valid.

CANONICAL_EXAMPLES:
```deluge
response = hexToText("5a6f686f2043524d");  // Returns "Zoho CRM"
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- textToHex — textToHex.dou.md
- Text functions — https://www.zoho.com/deluge/help/functions/text.html

SOURCE:
https://www.zoho.com/deluge/help/functions/string/hextotext.html
