FILE_PURPOSE: Deluge info statement — debug task to print expression values during script execution
MENTAL_MODEL: info <expression>; = print any value to debug output visible in the Functions execution log

WHEN_TO_USE:
- Print variable values, intermediate results, or debug messages during script development.
- Inspect list, map, or collection contents at any point in a workflow.

WHEN_NOT_TO_USE:
- Providing user-facing messages — use `alert` for notifications visible to non-admin users.

TRIGGER_KEYWORDS:
info, info statement, debug output, 500KB info limit, info truncation, admin-visible output

RULES:
- Syntax: `info <expression>;`
- `<expression>` accepts any value, variable, or expression that evaluates to a value.
- Combined response of `info` and `alert` statements in a single function is capped at 500 KB; when exceeded, output is truncated with the message: "The info message has been truncated because its size exceeded 500 KB."
- In Schedules and Approvals events, the info task is listed under Miscellaneous (not Debug).
- File Upload field values display in the format `<file-id>_<file-name>.<file-type>`.

CANONICAL_EXAMPLES:
```deluge
info "Hello World";  // Returns Hello World
info 1;              // Returns 1
```

FAILURE_MODES:
- Combined info + alert output exceeds 500 KB → output truncated, note appended.
- Used in Schedules or Approvals events → listed under Miscellaneous, not Debug.

RELATED_DOCS:
*(none)*

SOURCE:
https://www.zoho.com/deluge/help/debug/info.html
