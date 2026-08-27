FILE_PURPOSE: Deluge setCharset — set a character encoding on a FILE object for HTTP transmission via invokeUrl
MENTAL_MODEL: setCharset = FILE.setCharSet(charset) → void; encodes file with charset when sent via invokeUrl

WHEN_TO_USE:
- Specify encoding for a file before sending it via invokeUrl to an endpoint that requires a particular charset.

WHEN_NOT_TO_USE:
- Endpoint accepts the file's default encoding — setCharSet is unnecessary.

TRIGGER_KEYWORDS:
setCharset, file.setCharSet, charset encoding, UTF-16, invokeUrl HTTP encoding

RULES:
- Syntax: `<file_variable>.setCharSet(<charset>);` (method name: `setCharSet` with capital 'S').
- No return value; modifies the file object in place.
- `<charset>` is TEXT; accepted values listed in Zoho's supported charsets documentation.
- Encoding is applied when the file is sent in an HTTP request via the invokeUrl task.

CANONICAL_EXAMPLES:
```deluge
response = invokeUrl[url:"http://www.africau.edu/images/default/sample.pdf" type:GET];
response.setCharSet("UTF-16");
// file is now encoded as UTF-16 for subsequent invokeUrl HTTP requests
```

FAILURE_MODES:
- Using an unsupported charset string → behavior undefined per source.

RELATED_DOCS:
- File Methods — ../datatypes/../datatypes/file.dou.md
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/set-charset.html
