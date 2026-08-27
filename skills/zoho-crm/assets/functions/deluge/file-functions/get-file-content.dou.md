FILE_PURPOSE: Deluge getFileContent — read file body as a TEXT string from a cloud-fetched FILE object
MENTAL_MODEL: getFileContent = FILE → TEXT; accurate for text-based files; junk characters for binary/image files

WHEN_TO_USE:
- Extract raw text from .txt, .csv, or other text-based file objects.
- Read file body before parsing or processing as a string.

WHEN_NOT_TO_USE:
- Binary or image-based files (.pdf, .jpg, etc.) — output is garbled characters, not usable content.

TRIGGER_KEYWORDS:
getFileContent, file.getFileContent, invokeUrl file content, junk binary output

RULES:
- Syntax: `<response> = <file_object>.getFileContent();`
- Return type: TEXT.
- Text-based files (.txt, .csv, etc.) return content accurately.
- Image/binary files (.pdf, .png, etc.) return garbled/junk characters (not an error).

CANONICAL_EXAMPLES:
```deluge
fileVariable = invokeUrl[url:"http://example.com/sample.csv" type:GET];
response = fileVariable.getFileContent();
// response is a TEXT string of the CSV content
```

FAILURE_MODES:
- Binary file body → getFileContent succeeds but returns garbled TEXT; not an error, but content is unusable.

RELATED_DOCS:
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md
- File Methods — ../datatypes/../datatypes/file.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/get-file-content.html
