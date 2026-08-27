FILE_PURPOSE: Deluge Number and Decimal datatypes — integers and floating-point values
MENTAL_MODEL: Number = integer only; Decimal = fractional; mixed Number+Decimal arithmetic always yields Decimal

WHEN_TO_USE:
- Number: whole-number counters, IDs, index arithmetic, integer comparisons.
- Decimal: currency, percentages, ratio calculations requiring fractional precision.

WHEN_NOT_TO_USE:
- Number for fractional values — assign decimals to Decimal variables.
- Decimal where integer-only type consistency is required downstream.

TRIGGER_KEYWORDS:
Number datatype, Decimal datatype, planPrice, 9223372036854775808, number-to-decimal promotion, mixed arithmetic result, number-decimal shared functions

RULES:
- Number range: −9,223,372,036,854,775,808 to 9,223,372,036,854,775,808; integers only.
- Mixed arithmetic (Number + Decimal) always yields Decimal result.
- Integer division producing a fractional result yields Decimal datatype.
- Number and Decimal share the same built-in functions reference page.

CANONICAL_EXAMPLES:
```deluge
Version   = 5;            // Number
planPrice = 0.99;         // Decimal
discount  = 0.15;

count = 5; rate = 1.25;
total = count * rate;     // Decimal (6.25)

d = 10 / 3;               // Decimal (3.333...)

price       = 49.99;
final_price = price - (price * discount);  // Decimal
```

FAILURE_MODES:
- Value outside Number range — overflow error.
- Assigning a decimal literal to a Number variable silently promotes it to Decimal; downstream Number checks fail.
- Mixed Number + Decimal arithmetic always returns Decimal; type checks expecting Number after mixed arithmetic fail.
- Decimal precision limits not documented; behavior for very large fractional values is undefined per source.

RELATED_DOCS:
- Number and Decimal built-in functions — https://www.zoho.com/deluge/help/datatypes/number.html

SOURCE:
https://www.zoho.com/deluge/help/datatypes/number.html, https://www.zoho.com/deluge/help/datatypes/decimal.html
