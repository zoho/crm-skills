FILE_PURPOSE: Deluge `largest()` / `smallest()` — max and min DECIMAL from a numeric list.

MENTAL_MODEL: `list.largest()` = max DECIMAL; `list.smallest()` = min DECIMAL; input: NUMBER LIST or DECIMAL LIST.

WHEN_TO_USE:
- Finding the maximum value in a numeric list → use largest()
- Finding the minimum value in a numeric list → use smallest()

WHEN_NOT_TO_USE:
- Need the Nth largest or Nth smallest → use nthLargest() / nthSmallest()
- Need mean or median → use average() / median()

TRIGGER_KEYWORDS: largest(), smallest(), list-max-min, decimal-return-number-list, number-list-extremes

RULES:
1. Return type: DECIMAL for both largest() and smallest().
2. Input: NUMBER LIST or DECIMAL LIST. Numerical values can be in double quotes.

CANONICAL_EXAMPLES:
```deluge
numberList = {1, 5, 2, 3};
largestValue  = numberList.largest();  // → 5
smallestValue = numberList.smallest(); // → 1

// Functional forms
l = largest({1, 5, 2, 3});  // → 5
s = smallest({1, 5, 2, 3}); // → 1
```

FAILURE_MODES:
- Passing non-numeric elements → behavior not documented; use NUMBER LIST or DECIMAL LIST only

RELATED_DOCS:
- nthLargest() / nthSmallest() — list-nthLargest-nthSmallest.dou.md
- average() / median() — list-average-median.dou.md
- max() (two-value comparison) — ../number/../number/stat-max-min.dou.md
- min() (two-value comparison) — ../number/../number/stat-max-min.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/largest.html, https://www.zoho.com/deluge/help/functions/number/smallest.html
