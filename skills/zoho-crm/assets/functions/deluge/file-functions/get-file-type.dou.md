FILE_PURPOSE: Deluge getFileType — retrieve the MIME format string of a cloud-fetched FILE object
MENTAL_MODEL: getFileType = FILE → TEXT (MIME format string, e.g. "image/png")

WHEN_TO_USE:
- Identify the content format of a fetched file before processing or routing.
- Validate file format before passing to a function that requires a specific MIME format.

WHEN_NOT_TO_USE:
- The MIME type is irrelevant to the operation — skip validation if not needed.

TRIGGER_KEYWORDS:
getFileType, file.getFileType, image/png MIME, text/plain MIME, invokeUrl getFileType

RULES:
- Syntax: `<response> = <file_object>.getFileType();`
- Return type: TEXT (MIME format string, e.g. "image/png", "text/csv").

CANONICAL_EXAMPLES:
```deluge
fileVariable = invokeUrl[url:"https://sample-videos.com/img/Sample-png-image-100kb.png" type:GET];
response = fileVariable.getFileType(); // returns "image/png"
```

FAILURE_MODES:
- File variable is null (failed invokeUrl) → calling getFileType → runtime error.

RELATED_DOCS:
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md
- File Methods — ../datatypes/../datatypes/file.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/get-file-type.html
