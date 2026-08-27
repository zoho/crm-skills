FILE_PURPOSE: Deluge compress — zip one or more FILE objects into a single .zip FILE (max 2 MB)
MENTAL_MODEL: compress = FILE/LIST/KEY-VALUE → FILE (.zip, max 2 MB); optional directory structure via KEY-VALUE

WHEN_TO_USE:
- Zip a single FILE before attaching to email or uploading.
- Zip multiple files (LIST) into one archive.
- Zip files into a nested directory structure (KEY-VALUE map).

WHEN_NOT_TO_USE:
- Output zip would exceed 2 MB — compress throws an error; split into smaller batches.

TRIGGER_KEYWORDS:
compress, file.compress, LIST compress, KEY-VALUE directory zip, 2MB zip limit, getFileName, invokeUrl file only

RULES:
- Syntax: `<zip_file> = <files>.compress([<compressed_file_name>]);`
- `<files>` accepts FILE (single), LIST of FILEs (multiple), or KEY-VALUE (directory structure).
- For KEY-VALUE input: keys are file names (TEXT) or directory names (TEXT); values are FILE or nested KEY-VALUE.
- `<compressed_file_name>` (optional TEXT): name for the returned .zip; avoid restricted characters.
- Return type: FILE (.zip format).
- Output exceeding 2 MB causes an error.

CANONICAL_EXAMPLES:
```deluge
// Single file
zip_file = file1.compress("compressed_file");

// List of files
filesList = List();
filesList.add(file1);
filesList.add(file2);
zip_file = filesList.compress("compressed_file");

// Directory structure: dir1 contains file1 and nested dir2; dir2 contains file2
directory2 = Map();
directory2.put(file2.getFileName(), file2);
directory1 = Map();
directory1.put(file1.getFileName(), file1);
directory1.put("Directory 2", directory2);
zip_file = directory1.compress("Directory 1");
// Returns: Directory 1.zip
```

FAILURE_MODES:
- Compressed output > 2 MB → error; split files across multiple compress calls.

RELATED_DOCS:
- File Methods — ../datatypes/../datatypes/file.dou.md
- extract — extract.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/file/compress.html
