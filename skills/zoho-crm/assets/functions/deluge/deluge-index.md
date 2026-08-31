# Deluge DOU Node Index

Complete DOU node index for Deluge — all built-in functions, data types, operators, variables, tasks, file functions, and integrations.
Maintenance: add every new DOU node here first; also add to [functions.md#dou-reference-nodes](../../../references/functions.md#dou-reference-nodes) only if it belongs to a high-frequency section (categories, patterns, integrations, File Functions, built-in Conversion/Date-Time/List/Map/Number(utility)/Text).

### Function Category Templates

| Task | Read This File |
|---|---|
| All 7 category signatures + return types | [#canonical-examples](../functions-categories.dou.md#canonical-examples) |
| Button | [#button](../functions-categories.dou.md#button) |
| Automation | [#automation](../functions-categories.dou.md#automation) |
| Schedule | [#schedule](../functions-categories.dou.md#schedule) |
| Related List | [#related-list](../functions-categories.dou.md#related-list) |
| Standalone (toString, invokeFunction) | [#standalone](../functions-categories.dou.md#standalone) |
| Sales Signals | [#sales-signals](../functions-categories.dou.md#sales-signals) |
| Validation Rule (crmAPIRequest + Map return) | [#validation-rule](../functions-categories.dou.md#validation-rule) |

### Common Patterns

| Task | Read This File |
|---|---|
| Read-then-write | [#pattern-1-read-then-write](../functions-patterns.dou.md#pattern-1-read-then-write) |
| Call external API and store result | [#pattern-2-external-api-and-store-result](../functions-patterns.dou.md#pattern-2-external-api-and-store-result) |
| Guard clause / early exit | [#pattern-3-conditional-guard-clause](../functions-patterns.dou.md#pattern-3-conditional-guard-clause) |
| Loop over search results and update | [#pattern-4-loop-over-search-results-and-update](../functions-patterns.dou.md#pattern-4-loop-over-search-results-and-update) |
| Bulk create with explicit trigger | [#pattern-5-bulk-create-with-trigger-automation](../functions-patterns.dou.md#pattern-5-bulk-create-with-trigger-automation) |
| Two-step cross-module retrieval (Who_Id) | [#pattern-6-two-step-cross-module-retrieval](../functions-patterns.dou.md#pattern-6-two-step-cross-module-retrieval) |

Distilled Operational Understanding nodes for the Deluge scripting language, grouped by category.

### Data Types

| Task | Read This File |
|---|---|
| Work with Collection data type | [collection.dou.md](./datatypes/collection.dou.md) |
| Work with Date-Time data type | [date-time.dou.md](./datatypes/date-time.dou.md) |
| Work with File data type | [file.dou.md](./datatypes/file.dou.md) |
| Work with Key-Value (Map) data type | [key-value.dou.md](./datatypes/key-value.dou.md) |
| Work with List data type | [list.dou.md](./datatypes/list.dou.md) |
| Work with Number / Decimal data types | [number-decimal.dou.md](./datatypes/number-decimal.dou.md) |
| Work with Text / Boolean data types | [text-boolean.dou.md](./datatypes/text-boolean.dou.md) |

### Operators

| Task | Read This File |
|---|---|
| Use arithmetic and assignment operators | [arithmetic-assignment-operators.dou.md](./operators/arithmetic-assignment-operators.dou.md) |
| Use logical and relational operators | [logical-relational-operators.dou.md](./operators/logical-relational-operators.dou.md) |

### Variables

| Task | Read This File |
|---|---|
| Declare and use Deluge variables | [deluge-variables.dou.md](./variables/deluge-variables.dou.md) |

### Deluge Tasks — Conditions

| Task | Read This File |
|---|---|
| Write conditional statements (if / else if / else) | [conditional-statements.dou.md](./deluge-tasks/conditions/conditional-statements.dou.md) |
| Write criteria-based conditional statements | [criteria-conditional-statements.dou.md](./deluge-tasks/conditions/criteria-conditional-statements.dou.md) |

### Deluge Tasks — Misc

| Task | Read This File |
|---|---|
| Break out of a loop | [break.dou.md](./deluge-tasks/misc/break.dou.md) |
| Call a function from within Deluge | [call-function.dou.md](./deluge-tasks/misc/call-function.dou.md) |
| Continue to the next loop iteration | [continue.dou.md](./deluge-tasks/misc/continue.dou.md) |
| Return a value from a function | [return.dou.md](./deluge-tasks/misc/return.dou.md) |
| Send an email from Deluge | [send-mail.dou.md](./deluge-tasks/misc/send-mail.dou.md) |
| Set a variable | [set-variable.dou.md](./deluge-tasks/misc/set-variable.dou.md) |
| Handle exceptions with try-catch | [try-catch.dou.md](./deluge-tasks/misc/try-catch.dou.md) |

### File Functions

| Task | Read This File |
|---|---|
| Compress files | [compress.dou.md](./file-functions/compress.dou.md) |
| Convert a file to PDF | [convert-to-pdf.dou.md](./file-functions/convert-to-pdf.dou.md) |
| Extract a compressed file | [extract.dou.md](./file-functions/extract.dou.md) |
| Get file content | [get-file-content.dou.md](./file-functions/get-file-content.dou.md) |
| Get file name | [get-file-name.dou.md](./file-functions/get-file-name.dou.md) |
| Get file size | [get-file-size.dou.md](./file-functions/get-file-size.dou.md) |
| Get file type | [get-file-type.dou.md](./file-functions/get-file-type.dou.md) |
| Check if a value is a file | [is-file.dou.md](./file-functions/is-file.dou.md) |
| Set charset on a file | [set-charset.dou.md](./file-functions/set-charset.dou.md) |
| Set file name | [set-file-name.dou.md](./file-functions/set-file-name.dou.md) |
| Set file password | [set-file-password.dou.md](./file-functions/set-file-password.dou.md) |
| Set file type | [set-file-type.dou.md](./file-functions/set-file-type.dou.md) |
| Convert a value to a file | [to-file.dou.md](./file-functions/to-file.dou.md) |

### Integrations

| Task | Read This File |
|---|---|
| Use a named Connection in invokeUrl | [connections.dou.md](./integrations/connections.dou.md) |
| Transfer files via FTP / SFTP | [ftp-sftp-tasks.dou.md](./integrations/ftp-sftp-tasks.dou.md) |
| Call an API using the invokeApi task | [invokeapi-task.dou.md](./integrations/invokeapi-task.dou.md) |
| Call an external URL using the invokeUrl task | [invokeurl-task.dou.md](./integrations/invokeurl-task.dou.md) |

### Integrations — Zoho CRM Tasks

| Task | Read This File |
|---|---|
| Attach a file to a CRM record | [attach-file.dou.md](./integrations/zoho-crm/attach-file.dou.md) |
| Bulk create CRM records | [bulk-create-records.dou.md](./integrations/zoho-crm/bulk-create-records.dou.md) |
| Bulk update CRM records | [bulk-update-records.dou.md](./integrations/zoho-crm/bulk-update-records.dou.md) |
| Convert a Lead to a Contact | [convert-lead.dou.md](./integrations/zoho-crm/convert-lead.dou.md) |
| Create a CRM record | [create-record.dou.md](./integrations/zoho-crm/create-record.dou.md) |
| Get CRM field metadata | [get-fields.dou.md](./integrations/zoho-crm/get-fields.dou.md) |
| Get a CRM record by ID | [get-record-by-id.dou.md](./integrations/zoho-crm/get-record-by-id.dou.md) |
| Get CRM records (list) | [get-records.dou.md](./integrations/zoho-crm/get-records.dou.md) |
| Get related records from a CRM module | [get-related-records.dou.md](./integrations/zoho-crm/get-related-records.dou.md) |
| Search CRM records | [search-records.dou.md](./integrations/zoho-crm/search-records.dou.md) |
| Update a CRM record | [update-record.dou.md](./integrations/zoho-crm/update-record.dou.md) |
| Update a related record | [update-related-record.dou.md](./integrations/zoho-crm/update-related-record.dou.md) |
| Upsert a CRM record | [upsert-record.dou.md](./integrations/zoho-crm/upsert-record.dou.md) |

### Function Lifecycle and Best Practices

| Task | Read This File |
|---|---|
| Understanding CRM Functions architecture — categories, trigger types, language choices, execution lifecycle, and return type semantics per category | [functions-overview.dou.md](../functions-overview.dou.md) |
| Designing production-quality CRM Functions — idempotency, credential hygiene, performance, logging discipline, and naming conventions | [functions-best-practices.dou.md](../functions-best-practices.dou.md) |
| Building multi-function pipelines, migrating Workflow Rules to Functions, or implementing bulk-record pagination and chunking | [functions-strategies.dou.md](../functions-strategies.dou.md) |

### Deluge Errors

| Task | Read This File |
|---|---|
| Deluge error message reference — save errors, runtime errors, and built-in function type errors | [errors.dou.md](./errors.dou.md) |

### Built-in Functions — Conversion

| Task | Read This File |
|---|---|
| Parse TEXT, NUMBER, or DATE-TIME expression into a DATE-TIME value | [toDate.dou.md](./built-in-functions/conversion/toDate.dou.md) |
| Convert Unix epoch milliseconds to formatted TEXT with timezone | [toDateTimeString.dou.md](./built-in-functions/conversion/toDateTimeString.dou.md) |
| Convert a NUMBER, DECIMAL, or numeric TEXT to a DECIMAL value | [toDecimal.dou.md](./built-in-functions/conversion/toDecimal.dou.md) |
| Convert a NUMBER to its hexadecimal string representation | [toHex.dou.md](./built-in-functions/conversion/toHex.dou.md) |
| Convert a JSON-formatted TEXT array into a Deluge LIST | [toJSONList.dou.md](./built-in-functions/conversion/toJSONList.dou.md) |
| Split a TEXT string by a separator into a LIST | [toList.dou.md](./built-in-functions/conversion/toList.dou.md) |
| Split a comma-separated TEXT or LIST into a LIST of TEXT elements | [toListString.dou.md](./built-in-functions/conversion/toListString.dou.md) |
| Deluge `toLowerCase()` / `toUpperCase()` — convert all string letters to lower or upper case | [toLowerCase-toUpperCase.dou.md](./built-in-functions/conversion/toLowerCase-toUpperCase.dou.md) |
| Convert a JSON-formatted TEXT string into a KEY-VALUE map | [toMap.dou.md](./built-in-functions/conversion/toMap.dou.md) |
| Deluge `toNumber()` / `toLong()` — convert any expression to an integer NUMBER, truncating decimals | [toNumber-toLong.dou.md](./built-in-functions/conversion/toNumber-toLong.dou.md) |
| Deluge `toString()` / `toText()` — convert any expression to TEXT with optional datetime formatting | [toString-toText.dou.md](./built-in-functions/conversion/toString-toText.dou.md) |
| Parse a datetime expression into DATE-TIME with explicit timezone conversion | [toTime.dou.md](./built-in-functions/conversion/toTime.dou.md) |
| Convert NUMBER or DECIMAL to words in a target language | [toWords.dou.md](./built-in-functions/conversion/toWords.dou.md) |

### Built-in Functions — Date-Time

| Task | Read This File |
|---|---|
| Add (or subtract) seconds from a DATE-TIME value | [add-seconds.dou.md](./built-in-functions/date-time/add-seconds.dou.md) |
| Deluge addBusinessDay() and subBusinessDay() — advance or retreat a date by business days | [add-sub-business-day.dou.md](./built-in-functions/date-time/add-sub-business-day.dou.md) |
| Deluge addDay() and subDay() — add or subtract calendar days from a date-time value | [add-sub-day.dou.md](./built-in-functions/date-time/add-sub-day.dou.md) |
| Deluge addHour() and subHour() — add or subtract hours from a DATE-TIME value | [add-sub-hour.dou.md](./built-in-functions/date-time/add-sub-hour.dou.md) |
| Deluge addMinutes() and subMinutes() — add or subtract minutes from a DATE-TIME value | [add-sub-minutes.dou.md](./built-in-functions/date-time/add-sub-minutes.dou.md) |
| Deluge addMonth() and subMonth() — add or subtract calendar months from a date-time value | [add-sub-month.dou.md](./built-in-functions/date-time/add-sub-month.dou.md) |
| Deluge daysBetween() and hoursBetween() — count calendar days or whole hours between two date-times | [days-hours-between.dou.md](./built-in-functions/date-time/days-hours-between.dou.md) |
| Shift a date by N months and return that month's last day | [eomonth.dou.md](./built-in-functions/date-time/eomonth.dou.md) |
| Deluge monthsBetween() and yearsBetween() — count months (30-day) or years (365-day) between dates | [months-years-between.dou.md](./built-in-functions/date-time/months-years-between.dou.md) |
| Deluge now and today — return the current date-time or current date-only value | [now-today.dou.md](./built-in-functions/date-time/now-today.dou.md) |
| Deluge toStartOfMonth() and toStartOfWeek() — get first day of a date's month or week | [to-start-of-month-week.dou.md](./built-in-functions/date-time/to-start-of-month-week.dou.md) |
| Deluge totalMonths() and totalYears() — count calendar months or years respecting actual day counts | [total-months-years.dou.md](./built-in-functions/date-time/total-months-years.dou.md) |

### Built-in Functions — List

| Task | Read This File |
|---|---|
| Deluge list add() and addAll() — append element(s) to a list in place | [list-add-addall.dou.md](./built-in-functions/list/list-add-addall.dou.md) |
| Deluge `average()` / `median()` — compute mean and median of a NUMBER or DECIMAL list | [list-average-median.dou.md](./built-in-functions/list/list-average-median.dou.md) |
| Deluge list contains() — exact membership test for a list element | [list-contains.dou.md](./built-in-functions/list/list-contains.dou.md) |
| Deluge list get() size() clear() — index access, element count, and list emptying | [list-get-size-clear.dou.md](./built-in-functions/list/list-get-size-clear.dou.md) |
| Deluge `indexOf()` / `lastIndexOf()` — find first or last index of element in a LIST | [list-indexOf-lastIndexOf.dou.md](./built-in-functions/list/list-indexOf-lastIndexOf.dou.md) |
| Deluge list intersect() and subList() — get common elements or a slice of a list | [list-intersect-sublist.dou.md](./built-in-functions/list/list-intersect-sublist.dou.md) |
| Deluge `largest()` / `smallest()` — max and min DECIMAL from a numeric list | [list-largest-smallest.dou.md](./built-in-functions/list/list-largest-smallest.dou.md) |
| Deluge `notContains()` / `isEmpty()` — boolean membership absence and empty checks on TEXT/LIST/MAP | [list-notContains-isEmpty.dou.md](./built-in-functions/list/list-notContains-isEmpty.dou.md) |
| Deluge `nthLargest()` / `nthSmallest()` — retrieve the Nth ranked value from a numeric COLLECTION | [list-nthLargest-nthSmallest.dou.md](./built-in-functions/list/list-nthLargest-nthSmallest.dou.md) |
| Deluge `remove()` / `removeAll()` / `removeElement()` — three ways to remove from a LIST | [list-remove-removeAll-removeElement.dou.md](./built-in-functions/list/list-remove-removeAll-removeElement.dou.md) |
| Deluge list sort() and distinct() — sort elements or return unique values from a list | [list-sort-distinct.dou.md](./built-in-functions/list/list-sort-distinct.dou.md) |

### Built-in Functions — Map

| Task | Read This File |
|---|---|
| Deluge map containKey() containValue() notContains() — membership test for keys and values | [map-containkey-containvalue-notcontains.dou.md](./built-in-functions/map/map-containkey-containvalue-notcontains.dou.md) |
| Deluge map get() keys() size() isEmpty() — read access and state inspection | [map-get-keys-size-isempty.dou.md](./built-in-functions/map/map-get-keys-size-isempty.dou.md) |
| Deluge map put() and putAll() — insert or merge key-value pairs in place | [map-put-putall.dou.md](./built-in-functions/map/map-put-putall.dou.md) |
| Deluge map remove() and clear() — delete a key-value pair or empty the entire map | [map-remove-clear.dou.md](./built-in-functions/map/map-remove-clear.dou.md) |

### Built-in Functions — Number

| Task | Read This File |
|---|---|
| Deluge `abs()` / `frac()` — extract the magnitude or fractional part of a number | [abs-frac.dou.md](./built-in-functions/number/abs-frac.dou.md) |
| Deluge `addWeek()` / `subWeek()` — shift a DATE-TIME forward or backward by weeks | [addWeek-subWeek.dou.md](./built-in-functions/number/addWeek-subWeek.dou.md) |
| Deluge `addYear()` / `subYear()` — shift a DATE-TIME forward or backward by years | [addYear-subYear.dou.md](./built-in-functions/number/addYear-subYear.dou.md) |
| Angle from positive x-axis to point (x,y) in radians | [atan2.dou.md](./built-in-functions/number/atan2.dou.md) |
| Deluge `ceil()` / `floor()` — round a DECIMAL to the nearest integer above or below | [ceil-floor.dou.md](./built-in-functions/number/ceil-floor.dou.md) |
| Deluge `day()` / `month()` — extract day-of-month or month NUMBER from DATE-TIME | [day-month.dou.md](./built-in-functions/number/day-month.dou.md) |
| Count days between two DATE-TIME values; equivalent to `daysBetween()` | [days360.dou.md](./built-in-functions/number/days360.dou.md) |
| Add N months to a DATE-TIME; negative N subtracts months | [edate.dou.md](./built-in-functions/number/edate.dou.md) |
| Compute e raised to the power of a given number | [exp.dou.md](./built-in-functions/number/exp.dou.md) |
| Get day-of-year NUMBER (1–366) from a DATE-TIME value | [getDayOfYear.dou.md](./built-in-functions/number/getDayOfYear.dou.md) |
| Get week-of-year NUMBER (1–52) with optional start-day override | [getWeekOfYear.dou.md](./built-in-functions/number/getWeekOfYear.dou.md) |
| Extract year as NUMBER from a DATE-TIME value; alias `year()` | [getYear.dou.md](./built-in-functions/number/getYear.dou.md) |
| Deluge `hour()` / `minute()` / `second()` — get hour, minute, second from a DATE-TIME value | [hour-minute-second.dou.md](./built-in-functions/number/hour-minute-second.dou.md) |
| Deluge cosh() and acosh() — hyperbolic cosine and inverse hyperbolic cosine | [hyperbolic-cosh-acosh.dou.md](./built-in-functions/number/hyperbolic-cosh-acosh.dou.md) |
| Deluge sinh() and asinh() — hyperbolic sine and inverse hyperbolic sine | [hyperbolic-sinh-asinh.dou.md](./built-in-functions/number/hyperbolic-sinh-asinh.dou.md) |
| Deluge tanh() and atanh() — hyperbolic tangent and inverse hyperbolic tangent | [hyperbolic-tanh-atanh.dou.md](./built-in-functions/number/hyperbolic-tanh-atanh.dou.md) |
| Return BOOLEAN true when expression is a valid DATE-TIME value | [isDate.dou.md](./built-in-functions/number/isDate.dou.md) |
| Check whether an expression evaluates to a valid numeric value | [isnumber.dou.md](./built-in-functions/number/isnumber.dou.md) |
| Deluge `log()` / `log10()` — compute the natural or base-10 logarithm of a number | [log-log10.dou.md](./built-in-functions/number/log-log10.dou.md) |
| Deluge `nextWeekDay()` / `previousWeekDay()` — seek next or previous date by weekday name | [nextWeekDay-previousWeekDay.dou.md](./built-in-functions/number/nextWeekDay-previousWeekDay.dou.md) |
| Deluge `power()` / `sqrt()` — exponentiate a number or compute its square root | [power-sqrt.dou.md](./built-in-functions/number/power-sqrt.dou.md) |
| Generate a random number within an inclusive-start exclusive-end range | [randomnumber.dou.md](./built-in-functions/number/randomnumber.dou.md) |
| Round a number to a specified decimal or integer precision | [round.dou.md](./built-in-functions/number/round.dou.md) |
| Deluge max() and min() — compare two numbers and return the larger or smaller | [stat-max-min.dou.md](./built-in-functions/number/stat-max-min.dou.md) |
| Subtract seconds from a DATE-TIME value; negative value adds seconds | [subSeconds.dou.md](./built-in-functions/number/subSeconds.dou.md) |
| Deluge cos() and acos() — trigonometric cosine and arccosine in radians | [trig-cos-acos.dou.md](./built-in-functions/number/trig-cos-acos.dou.md) |
| Deluge sin() and asin() — trigonometric sine and arcsine in radians | [trig-sin-asin.dou.md](./built-in-functions/number/trig-sin-asin.dou.md) |
| Deluge tan() and atan() — trigonometric tangent and arctangent in radians | [trig-tan-atan.dou.md](./built-in-functions/number/trig-tan-atan.dou.md) |
| Convert a TEXT date to Unix milliseconds since 1970-01-01 UTC | [unixEpoch.dou.md](./built-in-functions/number/unixEpoch.dou.md) |
| Get day-of-week NUMBER (1=Sunday, 7=Saturday) from DATE-TIME | [weekday.dou.md](./built-in-functions/number/weekday.dou.md) |
| Add business days to DATE-TIME with optional weekend and holiday lists | [workday.dou.md](./built-in-functions/number/workday.dou.md) |

### Built-in Functions — Text

| Task | Read This File |
|---|---|
| Join two TEXT strings into a single concatenated string | [concat.dou.md](./built-in-functions/text/concat.dou.md) |
| Deluge `contains()` / `containsIgnoreCase()` — check if a TEXT string contains a substring | [contains-containsIgnoreCase.dou.md](./built-in-functions/text/contains-containsIgnoreCase.dou.md) |
| Deluge `endsWith()` / `endsWithIgnoreCase()` — check if a TEXT string ends with a specific suffix | [endsWith-endsWithIgnoreCase.dou.md](./built-in-functions/text/endsWith-endsWithIgnoreCase.dou.md) |
| Compare two TEXT strings for equality, ignoring case differences | [equalsIgnoreCase.dou.md](./built-in-functions/text/equalsIgnoreCase.dou.md) |
| Deluge `find()` / `indexOf()` — return the 0-based index of a searchString's first occurrence | [find-indexOf.dou.md](./built-in-functions/text/find-indexOf.dou.md) |
| Deluge `getAlpha()` / `getAlphaNumeric()` — extract letters or alphanumeric characters from a string | [getAlpha-getAlphaNumeric.dou.md](./built-in-functions/text/getAlpha-getAlphaNumeric.dou.md) |
| Count occurrences of a substring within a text string | [getOccurenceCount.dou.md](./built-in-functions/text/getOccurenceCount.dou.md) |
| Deluge `getPrefix()` / `getSuffix()` — split a string on the first delimiter occurrence | [getPrefix-getSuffix.dou.md](./built-in-functions/text/getPrefix-getSuffix.dou.md) |
| Decode a hexadecimal-encoded string to its text equivalent | [hexToText.dou.md](./built-in-functions/text/hexToText.dou.md) |
| Return the 0-based index of the LAST occurrence of a searchString | [lastIndexOf.dou.md](./built-in-functions/text/lastIndexOf.dou.md) |
| Return a specified number of characters from a string's left side | [left.dou.md](./built-in-functions/text/left.dou.md) |
| Add leading whitespace to a text string for alignment | [leftpad.dou.md](./built-in-functions/text/leftpad.dou.md) |
| Deluge `len()` / `length()` — return the character count (including spaces) of a text string | [len-length.dou.md](./built-in-functions/text/len-length.dou.md) |
| Remove all leading whitespace characters from the left side of a string | [ltrim.dou.md](./built-in-functions/text/ltrim.dou.md) |
| Test if a string matches a regex pattern exactly | [matches.dou.md](./built-in-functions/text/matches.dou.md) |
| Extract a substring between two 0-based character indices | [mid.dou.md](./built-in-functions/text/mid.dou.md) |
| Convert a string to title/start case | [proper.dou.md](./built-in-functions/text/proper.dou.md) |
| Strip all alphabetic letters from a string | [remove-all-alpha.dou.md](./built-in-functions/text/remove-all-alpha.dou.md) |
| Strip all letters and digits from a string | [remove-all-alphanumeric.dou.md](./built-in-functions/text/remove-all-alphanumeric.dou.md) |
| Remove only the first matching substring occurrence | [remove-first-occurence.dou.md](./built-in-functions/text/remove-first-occurence.dou.md) |
| Remove only the last matching substring occurrence | [remove-last-occurence.dou.md](./built-in-functions/text/remove-last-occurence.dou.md) |
| Remove all occurrences of a substring from a string | [remove.dou.md](./built-in-functions/text/remove.dou.md) |
| Replace all occurrences of a substring in a string | [replace-all.dou.md](./built-in-functions/text/replace-all.dou.md) |
| Replace only the first occurrence of a substring | [replace-first.dou.md](./built-in-functions/text/replace-first.dou.md) |
| Return a specified number of characters from a string's right side | [right.dou.md](./built-in-functions/text/right.dou.md) |
| Add trailing whitespace to a text string for alignment | [rightpad.dou.md](./built-in-functions/text/rightpad.dou.md) |
| Remove all trailing whitespace characters from the right side of a string | [rtrim.dou.md](./built-in-functions/text/rtrim.dou.md) |
| Deluge `startsWith()` / `startsWithIgnoreCase()` — check if a TEXT string starts with a prefix | [startsWith-startsWithIgnoreCase.dou.md](./built-in-functions/text/startsWith-startsWithIgnoreCase.dou.md) |
| Deluge `subString()` / `subText()` — extract a substring between two 0-based character indices | [subString-subText.dou.md](./built-in-functions/text/subString-subText.dou.md) |
| Format NUMBER, DECIMAL, or DATE-TIME using a custom format pattern string | [text.dou.md](./built-in-functions/text/text.dou.md) |
| Encode a text string to its hexadecimal representation | [textToHex.dou.md](./built-in-functions/text/textToHex.dou.md) |
| Remove all leading and trailing whitespace from a text string | [trim.dou.md](./built-in-functions/text/trim.dou.md) |

### Deluge Tasks — Debug

| Task | Read This File |
|---|---|
| Deluge info statement — debug task to print expression values during script execution | [info.dou.md](./deluge-tasks/debug/info.dou.md) |

### Deluge Tasks — List Manipulations

| Task | Read This File |
|---|---|
| Deluge typed list declarations — List:String, List:Int, List:Float, List:date, List:Bool | [create-list-typed.dou.md](./deluge-tasks/list-manipulations/create-list-typed.dou.md) |
| Declare an empty or pre-populated heterogeneous list variable | [create-list.dou.md](./deluge-tasks/list-manipulations/create-list.dou.md) |
| Each-element loop — iterate over list elements or CSV file rows | [for-each-element.dou.md](./deluge-tasks/list-manipulations/for-each-element.dou.md) |
| Each-index loop — iterate over list element indices (0-based positions) | [for-each-index.dou.md](./deluge-tasks/list-manipulations/for-each-index.dou.md) |
| Permanently remove all elements from a list | [list-clear.dou.md](./deluge-tasks/list-manipulations/list-clear.dou.md) |
| Remove the first matching element by value | [list-remove-element.dou.md](./deluge-tasks/list-manipulations/list-remove-element.dou.md) |
| Remove and return the element at a specified index | [list-remove-index.dou.md](./deluge-tasks/list-manipulations/list-remove-index.dou.md) |

### Deluge Tasks — Map Manipulations

| Task | Read This File |
|---|---|
| Manipulation tasks — create, insert, merge, delete, and clear map entries | [map-manipulations.dou.md](./deluge-tasks/map-manipulations/map-manipulations.dou.md) |

### Deluge Tasks — Open URL

| Task | Read This File |
|---|---|
| Browser-navigate to a URL in a target window | [openUrl.dou.md](./deluge-tasks/open-url/openUrl.dou.md) |

### Deluge Tasks — XML Manipulation

| Task | Read This File |
|---|---|
| Query XML or JSON text using XPath expressions to extract node values | [executeXpath.dou.md](./deluge-tasks/xml-manipulation/executeXpath.dou.md) |
