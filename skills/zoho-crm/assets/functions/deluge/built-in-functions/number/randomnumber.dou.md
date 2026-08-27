FILE_PURPOSE: Deluge randomNumber() — generate a random number within an inclusive-start exclusive-end range
MENTAL_MODEL: randomNumber(start, end) = random in [start, end); NUMBER if both integers, DECIMAL if either is decimal

WHEN_TO_USE:
- Generate a random integer within a whole-number range.
- Generate a random decimal within a fractional range.

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
randomNumber, randomnumber, start_limit end_limit, exclusive end_limit, random decimal range

RULES:
- Syntax: `<variable> = randomNumber(<start_limit>, <end_limit>);`
- Both `<start_limit>` and `<end_limit>` accept NUMBER or DECIMAL.
- Returns NUMBER if both arguments are whole numbers.
- Returns DECIMAL if either argument is a decimal value.
- The generated value includes start_limit and any values between, but is NEVER equal to end_limit (end is exclusive).

CANONICAL_EXAMPLES:
```deluge
response1 = randomnumber(1, 3);           // returns 1 or 2 (never 3)
response2 = randomnumber(1.789, 34.54);   // random decimal in [1.789, 34.54)
response3 = randomnumber(5, 123.4);       // random decimal in [5, 123.4)
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/randomnumber.html
