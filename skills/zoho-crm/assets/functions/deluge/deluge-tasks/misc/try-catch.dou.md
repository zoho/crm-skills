FILE_PURPOSE: Deluge try-catch — handle runtime errors with structured exception handling
MENTAL_MODEL: try { risky code } catch(e) { error handler }; catch runs only on error; code after try-catch always executes

WHEN_TO_USE:
- Wrap Deluge code that might throw runtime errors in a try block.
- Inspect error details (line number, message) in the catch block.
- Continue overall function execution even when a section throws a runtime error.

WHEN_NOT_TO_USE:
*(none in source)*

TRIGGER_KEYWORDS:
try catch, exception_variable.lineNo, exception_variable.message, runtime exception handler, catch block Deluge

RULES:
- Syntax: `try { <code> } catch(<exception_variable>) { <code> }`
- Catch block executes only when the try block throws a runtime error; skipped if no error occurs.
- Exception variable attributes:
  - `<exception_variable>.lineNo` → line number of the statement that caused the error.
  - `<exception_variable>.message` → error message text.
  - `<exception_variable>` alone → both line number and error message combined.
- Code written after the try-catch block executes regardless of whether an error was caught.

CANONICAL_EXAMPLES:
```deluge
try {
  products = {"Leads", "Contacts", "Deals"};
  products = products.get(10); // index out of bounds → error
  products.add("Sheet");       // not reached
} catch(e) {
  info e.lineNo;    // line number of statement that caused error
  info e.message;   // error message text
  info e;           // both line number and message
}
// e holds: "Error at line : 6, Given index 10 is greater than the list size"
// Code after try-catch still executes
```

FAILURE_MODES:
*(none in source)*

RELATED_DOCS:
*(none in source)*

SOURCE:
https://www.zoho.com/deluge/help/misc-statements/try-catch.html
