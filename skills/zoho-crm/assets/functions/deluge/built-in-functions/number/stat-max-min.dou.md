FILE_PURPOSE: Deluge max() and min() — compare two numbers and return the larger or smaller
MENTAL_MODEL: max(a, b) = DECIMAL larger of two; min(a, b) = DECIMAL smaller of two

WHEN_TO_USE:
- Return the larger of exactly two numbers with max().
- Return the smaller of exactly two numbers with min().

WHEN_NOT_TO_USE:
- Finding the extreme value across a list — use largest() or smallest() instead.

TRIGGER_KEYWORDS:
max, min, numberOne.max, numberOne.min, two-number comparison, max-min scalar pair

RULES:
- max() syntax: `<variable> = <numberOne>.max(<numberTwo>);` or `max(<numberOne>, <numberTwo>)`.
- min() syntax: `<variable> = <numberOne>.min(<numberTwo>);` or `min(<numberOne>, <numberTwo>)`.
- Both arguments accept NUMBER or DECIMAL.
- Both return DECIMAL.

CANONICAL_EXAMPLES:
```deluge
numOne = 100;
numTwo = 200;
maxValue = numOne.max(numTwo);  // returns 200
minValue = numOne.min(numTwo);  // returns 100
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- largest — ../list/../list/list-largest-smallest.dou.md
- smallest — ../list/../list/list-largest-smallest.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/max.html, https://www.zoho.com/deluge/help/functions/number/min.html
