## FILE_PURPOSE
Deluge list sort() and distinct() — sort elements or return unique values from a list.

## MENTAL_MODEL
sort(bool) = LIST ordered asc/desc; distinct() = LIST with duplicates removed; cross-type dedup applies.

## WHEN_TO_USE
- Sort a list in ascending or descending order (sort()).
- Remove duplicate values from a list, retaining one of each unique value (distinct()).

## WHEN_NOT_TO_USE
- Sorting a list with mixed data types — sort() returns null for such lists.

## TRIGGER_KEYWORDS
list.sort, list.distinct, sort ascending descending, remove duplicates list, list unique values

## RULES
- sort() syntax: `<variable> = <listVariable>.sort(<booleanValue>);`
  — both `<variable>` and `<booleanValue>` are optional.
- distinct() syntax: `<variable> = <listVariable>.distinct();`
- Both return LIST.
- sort(): `true` → ascending; `false` → descending; omitted → ascending.
- sort(): for text lists, letter case is checked before the actual letter (case-aware ordering).
  Sort order: `! " # $ % & ' ( ) * + , - . / : ; < = > ? @ <capitals> [ ] ^ _ ` <lowercase> { | } ~`
- sort(): if list contains elements of different data types → returns null.
- distinct(): treats STRING and NUMBER representations of the same value as duplicates.
  - Input `{"1", 1, 1, 2, 2, 3}` → output `{1, 1, 2, 3}` (text "1" treated as duplicate of number 1).

## CANONICAL_EXAMPLES
```deluge
// sort() — uppercase letters sort before lowercase
listVar   = {"Leads", "crm", "Zoho Leads"};
sortOrder = listVar.sort(true);
// returns {"Leads", "Zoho Leads", "crm"}
// Explanation: "Leads" and "Zoho Leads" (capital L/Z) sort before "crm" (lowercase c)

// distinct() — cross-type: text "1" and number 1 treated as duplicates
listVar    = {"1", 1, 1, 2, 2, 3};
uniqueList = listVar.distinct();
// returns {1, 1, 2, 3}
```

## FAILURE_MODES
- sort(): list contains mixed data types → returns null.
- distinct(): string and number representations of the same value are treated as duplicates;
  one instance is removed, which produces counter-intuitive results for mixed-type lists.

## RELATED_DOCS
- List functions — https://www.zoho.com/deluge/help/functions/list.html

## SOURCE
https://www.zoho.com/deluge/help/functions/list/sort.html, https://www.zoho.com/deluge/help/functions/list/distinct.html
