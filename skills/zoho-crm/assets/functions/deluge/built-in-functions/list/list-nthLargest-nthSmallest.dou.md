FILE_PURPOSE: Deluge `nthLargest()` / `nthSmallest()` — retrieve the Nth ranked value from a numeric COLLECTION.

MENTAL_MODEL: `col.nthLargest(n)` = nth from top (1-based); `col.nthSmallest(n)` = nth from bottom (1-based); index > size → runtime.

WHEN_TO_USE:
- Need the 2nd largest, 3rd smallest, or any ranked position in a numeric collection
- Ranked value retrieval beyond the absolute max/min

WHEN_NOT_TO_USE:
- Need absolute max → use largest()
- Need absolute min → use smallest()
- Rank 1 from a LIST input — largest() / smallest() accept LIST; nthLargest() / nthSmallest() require COLLECTION

TRIGGER_KEYWORDS: nthLargest(), nthSmallest(), 1-based-rank-index, collection-numeric-rank, rank-exceeds-size-runtime

RULES:
1. Return type: NUMBER / DECIMAL.
2. Input: COLLECTION of numerical values (NUMBER and DECIMAL). Index: NUMBER (1-based).
3. nthLargest(n): sorts values descending, returns element at rank n.
4. nthSmallest(n): sorts values ascending, returns element at rank n.
5. Index starts from 1 (NOT 0).
6. Index cannot exceed the size of the collection → runtime error if exceeded.

CANONICAL_EXAMPLES:
```deluge
// nthLargest — COLLECTION input, 1-based index
marks = Collection(300, 455, 124, 926, 780);
result = marks.nthlargest(5); // → 124 (5th largest of 5 = the minimum)

// nthSmallest — example in source uses list {} notation
marks = {300, 455, 124, 926, 780};
result = marks.nthSmallest(2); // → 300 (2nd smallest after 124)
```

FAILURE_MODES:
- Index starts from 1 — nthLargest(0) or nthSmallest(0) exceeds range → runtime error
- Index > collection size → runtime error
- nthLargest source uses Collection(); nthSmallest source example uses list {} — source inconsistency; Collection is the documented input type

RELATED_DOCS:
- largest() / smallest() — list-largest-smallest.dou.md
- average() / median() — list-average-median.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/nth-largest.html, https://www.zoho.com/deluge/help/functions/number/nth-smallest.html
