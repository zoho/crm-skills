FILE_PURPOSE: Deluge continue statement — skip the current loop iteration and proceed to the next one
MENTAL_MODEL: continue; = skips remaining statements in current iteration; for-each loop proceeds with next element

WHEN_TO_USE:
- Skip a specific iteration of a for-each loop based on a condition.
- Filter out unwanted elements in a loop without using deeply nested conditional blocks.

WHEN_NOT_TO_USE:
- Outside a for-each loop — continue is only valid inside loops.

TRIGGER_KEYWORDS:
continue, continue loop Deluge, skip iteration, for each continue, loop iteration skip

RULES:
- Syntax: `continue;`
- Skips the remainder of the current iteration and proceeds with the next iteration of the for-each loop.
- Continue skips only the current iteration; contrast with `break` which terminates the entire loop.

CANONICAL_EXAMPLES:
```deluge
// Skip "Red" in the loop
colors = List();
colors.add("Green");
colors.add("Red");
colors.add("Blue");
colors.add("Teal");
for each rec in colors {
  if(rec == "Red") {
    continue;
  }
  info rec;
}
// Returns: Green, Blue, Teal
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- break — break.dou.md
- For each statement — ../list-manipulations/../list-manipulations/for-each-element.dou.md

SOURCE:
https://www.zoho.com/deluge/help/misc-statements/continue.html
