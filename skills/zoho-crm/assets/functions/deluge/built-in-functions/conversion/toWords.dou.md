FILE_PURPOSE: Deluge `toWords()` — convert NUMBER or DECIMAL to words in a target language.
MENTAL_MODEL: `num.toWords(langCode)` = TEXT; converts numeric value to human-readable words; supports 11 languages.

WHEN_TO_USE:
- Render a NUMBER or DECIMAL as words for display in documents, invoices, or reports.
- Generate locale-specific word representations (e.g., Indian numbering with `en-in`).

WHEN_NOT_TO_USE:
- When the NUMBER exceeds 18 integer digits — not supported.
- When the DECIMAL input's whole and decimal parts combined exceed 15 digits — not supported.

TRIGGER_KEYWORDS:
toWords(), number to words, toWords locale-tag, en-us toWords, en-in crore format, decimal to words

RULES:
- Return type: TEXT.
- Input types: NUMBER or DECIMAL (number), NUMBER or TEXT (language code).
- Both `<number>.toWords(<language>)` and `toWords(<number>, <language>)` syntaxes are valid.
- NUMBER input: value can contain up to 18 digits.
- DECIMAL input: whole and decimal parts collectively can be up to 15 digits.
- Supported language codes: `en-gb`, `en-us`, `fr`, `de`, `it`, `ja`, `ko`, `zh`, `en-in`, `es`, `pt`.
- Indian English (`en-in`) uses the Indian numbering system (e.g., 10,000,000 → "one crore").
- Negative numbers are supported (e.g., -12 → "minus twelve" in en-gb).
- DECIMAL values include "point" separator in English output (e.g., 1989.13 → "...point one three").

CANONICAL_EXAMPLES:
```deluge
whole_number = 1989;
info whole_number.toWords("en-us");
// returns "one thousand nine hundred eighty-nine"

decimal_number = 1989.13;
info decimal_number.toWords("en-us");
// returns "one thousand nine hundred eighty-nine point one three"

negative_number = -12;
info negative_number.toWords("en-gb");
// returns "minus twelve"

info (24).toWords("ko");
// returns "이십사"

info (10000000).toWords("en-gb");
// returns "ten million"

info (10000000).toWords("en-in");
// returns "one crore"
```

FAILURE_MODES:
- NUMBER input exceeding 18 digits is not supported.
- DECIMAL input where whole and decimal parts combined exceed 15 digits is not supported.

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/towords.html
