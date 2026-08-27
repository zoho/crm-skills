FILE_PURPOSE: Deluge setFilePassword — encrypt a PDF or ZIP FILE object with a password in place
MENTAL_MODEL: setFilePassword = FILE.setFilePassword(password) → void; encrypts PDF or ZIP; no return; irreversible

WHEN_TO_USE:
- Password-protect a PDF or ZIP file object before emailing or sharing sensitive documents.
- Apply dynamic passwords to compressed reports or payslips generated in scripts.

WHEN_NOT_TO_USE:
- File is already password-protected — cannot apply a second password; existing passwords cannot be removed.
- File is not PDF or ZIP — unsupported file types.

TRIGGER_KEYWORDS:
setFilePassword, file.setFilePassword, PDF 32 char password, ZIP password encrypt, encrypt PDF Deluge

RULES:
- Syntax: `<file>.setFilePassword(<password>);`
- No return value; encrypts the file object in place.
- Supported file types: PDF and ZIP only.
- PDF password: maximum 32 characters; passwords longer than 32 characters are silently truncated to first 32.
- Cannot be applied to already-password-protected files.
- Existing passwords cannot be modified, replaced, or removed using this task.
- Applicable to all Zoho services.

CANONICAL_EXAMPLES:
```deluge
// Password-protect a PDF
pdfFile = invokeUrl[url:"https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" type:GET];
pdfFile.setFilePassword("mySecret123");

// Compress then password-protect a ZIP with a dynamic password
fileVariable = "Sample content".toFile("sample.txt");
zipFile = fileVariable.compress("compressed_file");
password = "Report" + zoho.currentdate.toString("ddMMyyyy");
zipFile.setFilePassword(password);
```

FAILURE_MODES:
- File already password-protected → error; cannot add or modify password.
- PDF password > 32 characters → silently truncated to first 32 characters (no error raised).
- Non-PDF, non-ZIP file → unsupported; behavior not documented; do not apply on other file types.

RELATED_DOCS:
- Encryption tasks — https://www.zoho.com/deluge/help/encryption-tasks.html
- compress — compress.dou.md
- Invoke URL — ../integrations/../integrations/invokeurl-task.dou.md

SOURCE:
https://www.zoho.com/deluge/help/file/set-file-password.html
