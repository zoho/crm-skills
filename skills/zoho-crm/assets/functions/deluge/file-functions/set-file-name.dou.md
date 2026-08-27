FILE_PURPOSE: Deluge setFileName — rename a FILE object in place before downstream use
MENTAL_MODEL: setFileName = FILE.setFileName(name) → void; mutates the file object's name label, no return

WHEN_TO_USE:
- Rename a file object before attaching to email, uploading to WorkDrive, or passing to convertToPDF output.
- Apply a meaningful filename to an invokeUrl-fetched file before further processing.

WHEN_NOT_TO_USE:
- The filename is irrelevant to downstream processing — skip if no renaming needed.

TRIGGER_KEYWORDS:
setFileName, file.setFileName, restricted characters filename, invokeUrl rename, setFileName void

RULES:
- Syntax: `<file_variable>.setFileName(<name>);`
- No return value; modifies the file object's name in place.
- `<name>` is TEXT; avoid restricted characters (source states restriction but does not enumerate them).

CANONICAL_EXAMPLES:
```deluge
response = invokeUrl[url:"http://www.africau.edu/images/default/sample.pdf" type:GET];
response.setFileName("sampleFile");
// file object is now named "sampleFile"
```

FAILURE_MODES:

RELATED_DOCS:
- File Methods — ../datatypes/../datatypes/file.dou.md
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/set-file-name.html
