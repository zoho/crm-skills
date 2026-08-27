FILE_PURPOSE: Deluge typed list declarations — List:String, List:Int, List:Float, List:date, List:Bool
MENTAL_MODEL: List:Type() = list constrained to one data type; auto-converts some types; rejects others at runtime

WHEN_TO_USE:
- Enforce a single data type for all list elements to prevent type-mismatch errors downstream.

WHEN_NOT_TO_USE:
- When list elements have mixed data types — use generic `List()` instead.

TRIGGER_KEYWORDS:
List:String(), List:Int(), List:Float(), List:date(), List:Bool(), typed list, type-constrained list

RULES:
- **Text list (`List:String()`)**: Text in quotes accepted. Numbers/Decimals without quotes auto-converted to Text. Date-time in single quotes auto-converted to Text. Booleans auto-converted to Text.
- **Number list (`List:Int()`)**: Only whole numbers accepted; any other data type causes a runtime error.
- **Decimal list (`List:Float()`)**: Numeric values accepted with or without quotes. Date-time in single quotes auto-converted to equivalent numeric milliseconds value. Other data types cause a runtime error.
- **Date-time list (`List:date()`)**: Date-time values in single or double quotes accepted. Numbers allowed: epoch offset where 1000 = +1 second from 31-Dec-1969 16:00:00. Number or Text in single/double quotes causes a runtime error. Missing time component defaults to 00:00:00.
- **Boolean list (`List:Bool()`)**: Only `'True'` or `'False'` values accepted (with or without quotes). Any other value in quotes causes a runtime error.

CANONICAL_EXAMPLES:
```deluge
var = List:Float();
var.add('1-Jan-2019');   // adds 1546329600000 (epoch ms equivalent)

listVar = List:String();
listVar.add(1);          // adds "1" (number auto-converted to string)
```

FAILURE_MODES:
- Adding an incompatible data type to a typed list → runtime error.
- Number or Text in single/double quotes in `List:date()` → runtime error.
- Non-boolean value in `List:Bool()` → runtime error.

RELATED_DOCS:
- Create List — create-list.dou.md

SOURCE:
https://www.zoho.com/deluge/help/create-list-datatype.html
