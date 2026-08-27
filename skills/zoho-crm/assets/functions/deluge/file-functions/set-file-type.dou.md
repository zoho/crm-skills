FILE_PURPOSE: Deluge setFileType — override the MIME format label of a FILE object for HTTP transmission
MENTAL_MODEL: setFileType = FILE.setFileType(mime) → void; changes MIME metadata only, does NOT convert file format

WHEN_TO_USE:
- Correct the MIME format label of an invokeUrl-fetched file before sending via HTTP request.

WHEN_NOT_TO_USE:
- Converting file format — setFileType changes only the MIME label, not file content or actual format.

TRIGGER_KEYWORDS:
setFileType, file.setFileType, MIME-format metadata, incompatible-format broken-file

RULES:
- Syntax: `<file_variable>.setFileType(<type>);`
- No return value; modifies the file object's MIME metadata in place.
- `<type>` is TEXT; any valid MIME format string is accepted.
- Does NOT convert the file; only overrides the MIME label used in HTTP requests via invokeUrl.
- Input file must be fetched via invokeUrl.

CANONICAL_EXAMPLES:
```deluge
response = invokeUrl[url:"http://www.africau.edu/images/default/sample.pdf" type:GET];
response.setFileType("pdf");
// MIME label overridden; file content unchanged
```

FAILURE_MODES:
- Setting a MIME label incompatible with actual file content → file opens broken; no runtime error from setFileType itself.

RELATED_DOCS:
- File Methods — ../datatypes/../datatypes/file.dou.md
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/set-file-type.html
