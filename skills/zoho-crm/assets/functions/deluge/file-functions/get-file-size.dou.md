FILE_PURPOSE: Deluge getFileSize — get the byte size of a cloud-fetched FILE object as a TEXT string
MENTAL_MODEL: getFileSize = FILE → TEXT (numeric string of file size in bytes, e.g. "545")

WHEN_TO_USE:
- Check file size before uploading or processing to enforce size constraints.
- Log or compare file sizes programmatically.

WHEN_NOT_TO_USE:
- Comparing sizes for non-numeric logic — return is TEXT; convert with toLong() before arithmetic.

TRIGGER_KEYWORDS:
getFileSize, file.getFileSize, size in bytes TEXT, invokeUrl file size, bytes as TEXT string

RULES:
- Syntax: `<response> = <file_object>.getFileSize();`
- Return type: TEXT (numeric string representing bytes, e.g. "545").

CANONICAL_EXAMPLES:
```deluge
fileVariable = invokeUrl[url:"http://example.com/sample.csv" type:GET];
response = fileVariable.getFileSize(); // returns "545" (bytes as TEXT)
```

FAILURE_MODES:
- Return is TEXT, not NUMBER — arithmetic requires toLong() conversion first.

RELATED_DOCS:
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md
- File Methods — ../datatypes/../datatypes/file.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/get-file-size.html
