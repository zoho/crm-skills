FILE_PURPOSE: Deluge toFile — wrap TEXT or COLLECTION content into a named FILE object
MENTAL_MODEL: toFile = TEXT/COLLECTION.toFile(filename) → FILE; wraps content only, does not convert format

WHEN_TO_USE:
- Create a FILE object from a string or collection when no cloud-fetched file is available.
- Build a CSV, text report, or structured data file for attachment or upload from generated content.

WHEN_NOT_TO_USE:
- Cloud-fetched files already available — prefer invokeUrl-fetched files over toFile per source guidance.
- Expecting file-format conversion — toFile wraps content only; mismatched content and extension produces a broken/corrupted file.

TRIGGER_KEYWORDS:
toFile, string.toFile, collection.toFile, 50MB limit

RULES:
- Syntax: `<variable> = <value>.toFile(<file_name>);`
- `<value>` accepts TEXT or COLLECTION.
- `<file_name>` is TEXT; sets the file name and extension (e.g. "report.csv").
- Return type: FILE.
- Input limit is 50 MB.
- File is named with the provided file_name including its extension.
- Does NOT perform format conversion; wrapping incompatible content with an extension may produce a broken file.

CANONICAL_EXAMPLES:
```deluge
// TEXT to file
file_object = "Report content line 1\nline 2".toFile("report.txt");

// COLLECTION to file
changes = collection();
changes.insert("Provide UI builder");
changes.insert("introduce different font families");
file_object = changes.toFile("feedback");
info file_object;
// Creates a FILE named "feedback" containing the collection data
```

FAILURE_MODES:
- Content incompatible with specified extension (e.g. binary data wrapped as .png) → broken file; no runtime error from toFile itself.

RELATED_DOCS:
- Upload File in Zoho Workdrive — https://www.zoho.com/deluge/help/workdrive/upload-file.html
- File Methods — ../datatypes/../datatypes/file.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/file/to-file.html
