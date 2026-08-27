FILE_PURPOSE: Deluge getFileName — retrieve the filename string of a cloud-fetched FILE object
MENTAL_MODEL: getFileName = FILE → TEXT (filename with extension, e.g. "sample.png")

WHEN_TO_USE:
- Read filename of an invokeUrl-fetched file for logging, naming, or directory keying in compress.
- Use the returned filename as the KEY when building a KEY-VALUE map for compress directory structure.

WHEN_NOT_TO_USE:
- Building a name from external metadata — use string operations on the fetched URL instead.

TRIGGER_KEYWORDS:
getFileName, file.getFileName, invokeUrl filename

RULES:
- Syntax: `<response> = <file_object>.getFileName();`
- Return type: TEXT (e.g. "Sample-png-image-100kb.png").

CANONICAL_EXAMPLES:
```deluge
fileVariable = invokeUrl[url:"https://sample-videos.com/img/Sample-png-image-100kb.png" type:GET];
response = fileVariable.getFileName(); // returns "Sample-png-image-100kb.png"
```

FAILURE_MODES:
- File variable is null (failed invokeUrl) → calling getFileName → runtime error.

RELATED_DOCS:
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md
- File Methods — ../datatypes/../datatypes/file.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/get-file-name.html
