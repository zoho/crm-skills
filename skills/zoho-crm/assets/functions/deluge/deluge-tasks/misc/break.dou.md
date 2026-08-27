FILE_PURPOSE: Deluge break statement — terminate a for-each loop immediately and resume after the loop
MENTAL_MODEL: break; = exits the current for-each loop entirely; execution continues at first statement after the loop

WHEN_TO_USE:
- Exit a for-each loop as soon as a target condition is met (e.g. first match found).
- Abort loop processing early to avoid unnecessary iterations.

WHEN_NOT_TO_USE:
- Outside a for-each loop — break is only valid inside loops.

TRIGGER_KEYWORDS:
break, break loop Deluge, for each break, loop termination, first match break

RULES:
- Syntax: `break;`
- Terminates execution of the current for-each loop.
- Execution resumes at the first statement after the loop.
- Break terminates the entire loop; contrast with `continue` which only skips the current iteration.

CANONICAL_EXAMPLES:
```deluge
// Exit loop when "Red" is found
colors = List();
colors.add("Green");
colors.add("Red");
colors.add("Blue");
colors.add("Teal");
for each rec in colors {
  if(rec == "Red") {
    break;
  }
  info rec;
}
// Returns: Green
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
- continue — continue.dou.md
- For each statement — ../list-manipulations/../list-manipulations/for-each-element.dou.md

SOURCE:
https://www.zoho.com/deluge/help/misc-statements/break.html
