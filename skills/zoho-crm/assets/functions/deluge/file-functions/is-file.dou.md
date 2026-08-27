FILE_PURPOSE: Deluge isFile — check whether a variable holds a valid cloud-fetched FILE object
MENTAL_MODEL: isFile = any variable → BOOLEAN; true if valid cloud FILE, false otherwise; offline files always false

WHEN_TO_USE:
- Validate that an invokeUrl or integration task returned a usable FILE before calling file functions.
- Guard against null or non-file values before compress, extract, or attachment operations.

WHEN_NOT_TO_USE:
- Offline/local files — isFile always returns false for local filesystem files.

TRIGGER_KEYWORDS:
isFile, file_object.isFile, isFile(file_object), BOOLEAN validation, invokeUrl file validation

RULES:
- Two equivalent syntaxes: `<variable> = <file_object>.isFile();` OR `<variable> = isFile(<file_object>);`
- Return type: BOOLEAN (true = valid cloud file; false = not a valid file).
- The file object must be available on the cloud; offline files return false.

CANONICAL_EXAMPLES:
```deluge
file_object = invokeUrl[url:"http://example.com/image.png" type:GET];

// Instance syntax
if(file_object.isFile()) {
  // proceed with file operations
}

// Static syntax
if(isFile(file_object)) {
  // proceed with file operations
}
```

FAILURE_MODES:
- Passing an offline/local file → returns false (not an error; operation is silently invalid).

RELATED_DOCS:
- File Methods — ../datatypes/../datatypes/file.dou.md
- Functions returning boolean — https://www.zoho.com/deluge/help/functions-returning-boolean.html

SOURCE:
https://www.zoho.com/deluge/help/functions/common/is-file.html
