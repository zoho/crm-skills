FILE_PURPOSE: Deluge extract — unzip a cloud-fetched .zip FILE into a COLLECTION of named file objects
MENTAL_MODEL: extract = zip FILE → COLLECTION {filename TEXT : FILE}; empty COLLECTION if non-zip, empty, or password-protected

WHEN_TO_USE:
- Unzip a .zip file fetched from cloud and access individual files inside it.
- Iterate extracted files for upload, processing, or attachment.

WHEN_NOT_TO_USE:
- Zip is password-protected — extract cannot handle it; returns empty COLLECTION with no error.
- Output would exceed size limit (3 MB) — error.

TRIGGER_KEYWORDS:
extract, zip.extract, COLLECTION key-value extract, 3MB extract limit, password-protected zip

RULES:
- Syntax: `<variable> = <zip_file>.extract();`
- Return type: COLLECTION (key = filename as TEXT, value = FILE object).
- Non-zip input or empty zip → empty COLLECTION returned (no error thrown).
- Password-protected zip → empty COLLECTION returned (no error thrown).
- Size limit: 3 MB; exceeding limit throws an error.

CANONICAL_EXAMPLES:
```deluge
zip = invokeUrl[url:"https://example.com/sample.zip" type:GET];
file_collection = zip.extract();
// key is TEXT (filename), value is FILE object
// e.g.: {"sample.txt":"sample.txt"}

// Upload each extracted file to WorkDrive
for each file in file_collection {
  zoho.workdrive.uploadFile(file, "folderID", file.getFileName(), true, "work");
}
```

FAILURE_MODES:
- Extracted content exceeds 3 MB → error.
- Password-protected zip → empty COLLECTION silently; no error raised.

RELATED_DOCS:
- File Methods — ../datatypes/../datatypes/file.dou.md
- compress — compress.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/file/extract.html
