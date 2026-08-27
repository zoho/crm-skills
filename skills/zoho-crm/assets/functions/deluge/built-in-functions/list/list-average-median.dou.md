FILE_PURPOSE: Deluge `average()` / `median()` — compute mean and median of a NUMBER or DECIMAL list.

MENTAL_MODEL: `list.average()` = DECIMAL mean; `list.median()` = middle value; even count → mean of two middle values.

WHEN_TO_USE:
- Computing the arithmetic mean of a numeric list → use average()
- Finding the statistical median of a numeric list → use median()

WHEN_NOT_TO_USE:
- Need the maximum value → use largest()
- Need the minimum value → use smallest()
- Need the Nth ranked value → use nthLargest() / nthSmallest()

TRIGGER_KEYWORDS: average(), median(), number-list-aggregate, even-count-median-average, decimal-list-stats

RULES:
1. Return type: DECIMAL for both average() and median().
2. Input: NUMBER LIST or DECIMAL LIST. Numerical values can be in double quotes.
3. median(): sorts list in ascending order internally, then returns the middle element.
4. median() with even number of elements: returns the average of the two middle elements.

CANONICAL_EXAMPLES:
```deluge
numberList = {1, 5, 2, 3};
averageValue = numberList.average(); // → 2.75 (mean: (1+5+2+3)/4)
medianValue  = numberList.median();  // → 2.5  (sorted: 1,2,3,5 → avg of 2 and 3)

// Functional forms
avg = average({1, 5, 2, 3}); // → 2.75
med = median({1, 5, 2, 3});  // → 2.5
```

FAILURE_MODES:
- median() on even-sized list returns average of two middle values, not one of them
- Passing non-numeric elements → behavior not documented; use NUMBER LIST or DECIMAL LIST only

RELATED_DOCS:
- largest() / smallest() — list-largest-smallest.dou.md
- nthLargest() / nthSmallest() — list-nthLargest-nthSmallest.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/average.html, https://www.zoho.com/deluge/help/functions/number/median.html
