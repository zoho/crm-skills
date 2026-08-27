FILE_PURPOSE: Deluge FILE datatype — files fetched from web or cloud services
MENTAL_MODEL: FILE = remote-fetched file object; uniform across MIME types; produced by invokeUrl/getUrl/integration tasks

WHEN_TO_USE:
- Pass a downloaded file to CRM `attachFile`, FTP/SFTP tasks, or `send mail` attachments.
- Apply file built-in methods to a downloaded file.

WHEN_NOT_TO_USE:
- Local (offline) filesystem files — FILE datatype only represents remotely-fetched files.

TRIGGER_KEYWORDS:
FILE datatype, invokeUrl, getUrl, file-methods, zoho.sign.downloadDocument, zoho.writer.mergeAndDownload

RULES:
- FILE datatype is produced by: `invokeUrl` task, `getUrl` task, or integration tasks returning a file (e.g. `zoho.writer.mergeAndDownload`, `zoho.sign.downloadDocument`).
- FILE type is uniform regardless of MIME type (.pdf, .jpeg, .mp4, etc.); datatype behavior is identical for all formats.

CANONICAL_EXAMPLES:
```deluge
file_variable = invokeUrl[
  url: "https://sample-videos.com/img/Sample-png-image-100kb.png"
  type: GET
];

file_variable = zoho.sign.downloadDocument(2131000000002069);
```

FAILURE_MODES:
- `invokeUrl` against a local path fails; source must be a reachable URL.
- Non-FILE references have no applicable file methods; pass them only to integration tasks or `send mail`.

RELATED_DOCS:
- File built-in functions — https://www.zoho.com/deluge/help/datatypes/file-data-type.html
- invokeUrl task — ../integrations/../integrations/invokeurl-task.dou.md
- getUrl task — ../integrations/../integrations/invokeurl-task.dou.md
- attach file CRM task — ../integrations/zoho-crm/attach-file.dou.md

SOURCE:
https://www.zoho.com/deluge/help/datatypes/file-data-type.html
