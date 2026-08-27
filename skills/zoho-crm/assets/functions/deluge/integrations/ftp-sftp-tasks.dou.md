FILE_PURPOSE: Deluge ftp and sftp tasks — file upload and download to/from FTP or SFTP servers
MENTAL_MODEL: ftp/sftp = connection-authenticated file transfer tasks; 5 MB download cap; path must start with /

WHEN_TO_USE:
- Upload files to a remote FTP (port 21) or SFTP (port 22) server from a Deluge Function.
- Download files from a remote FTP or SFTP server.

WHEN_NOT_TO_USE:
- Zoho Flow — neither `ftp` nor `sftp` tasks are supported there.
- Files exceeding 5 MB for download — size limit enforced.

TRIGGER_KEYWORDS:
ftp action upload, ftp action download, sftp port 22, ftp port 21, ftp connection, sftp not Zoho Flow, ftp path slash-required, file transfer protocol

RULES:
- `ftp` uses FTP, default port 21; `sftp` uses SSH FTP, default port 22.
- Download size limit: 5 MB for both tasks.
- Neither task is applicable in Zoho Flow.
- `path` must start with `/`; if omitted, root directory is used as destination.
- `files` is mandatory for upload action; optional for download.
- FTP upload success: text `"File has been uploaded successfully"` + code `226`.
- SFTP upload success: text `"File has been uploaded successfully"` + code `200`.
- Download response: `responseText` contains the downloaded file.

CANONICAL_EXAMPLES:
```deluge
// FTP upload
uploadFtp = ftp[
  action:upload host:"ftp.examplehost.com" port:21
  path:"/home/uploads/" files:textFile connection:"ftp_connection"
];

// FTP download
downloadFtp = ftp[
  action:download host:"ftp.examplehost.com" port:21
  path:"/home/uploads/example.png" connection:"ftp_connection"
];
info downloadFtp.getFileContent();

// Convert invokeUrl response to file before FTP upload
ftpFile  = invokeUrl[url:"https://example.com/file.txt" type:GET];
ftpFile  = ftpFile.toFile("filename.txt");
uploadFtp = ftp[action:upload host:"ftp.examplehost.com" port:21 path:"" files:ftpFile connection:"ftp_connection"];
```

FAILURE_MODES:
- `ftp`/`sftp` tasks used in Zoho Flow → runtime error.
- `files` omitted for upload action → upload failure.
- `path` not starting with `/` → path resolution error on server.
- Download exceeds 5 MB → runtime error.
- Relative paths (no leading `/`) on Linux FTP servers → file-not-found.
- File path case mismatch on Linux FTP servers → file-not-found.
- `invokeUrl` response passed directly to `files` without `.toFile("<name>")` conversion → fails.

RELATED_DOCS:
- FTP task — https://www.zoho.com/deluge/help/ftp-task.html
- SFTP task — https://www.zoho.com/deluge/help/ftp-task.html

SOURCE:
https://www.zoho.com/deluge/help/ftp-task.html, https://www.zoho.com/deluge/help/sftp-task.html
