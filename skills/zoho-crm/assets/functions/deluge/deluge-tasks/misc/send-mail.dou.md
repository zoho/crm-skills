FILE_PURPOSE: Deluge sendmail task — send email to recipients with optional CC, BCC, and attachments
MENTAL_MODEL: sendmail[from:... to:... subject:... message:...] = structured email dispatch; from must be verified or admin/login user ID

WHEN_TO_USE:
- Send emails from Deluge scripts across all Zoho services.

WHEN_NOT_TO_USE:
- Gmail address as sender — not allowed from February 1, 2024.
- Unverified from addresses in restricted services → sendmail task fails.

TRIGGER_KEYWORDS:
sendmail, from zoho.adminuserid, from zoho.loginuserid, verified email sendmail, attachments file, reply to 20 limit

RULES:
- Syntax: `sendmail[from: <from_address> to: <to_address> cc: <cc> bcc: <bcc> reply to: <reply_to_address> subject: <subject> message: <message> content type: <content_type> attachments: <attachment>]`
- `from`: TEXT; must be `zoho.adminuserid`, `zoho.loginuserid`* (not portal users), or a verified email address; format "Name <email>" sets display name in recipient's inbox.
- `to`, `cc`, `bcc`: TEXT or LIST; multiple addresses via comma-separated string or LIST.
- `reply to`: TEXT, LIST, or comma-separated TEXT; maximum 20 reply-to addresses.
- `content type`: default `HTML`; specify `Plain Text` to send HTML tags unrendered.
- `attachments`: FILE; maximum size 15 MB; if exceeded, emails delivered without attachments.
- In services other than Zoho Cliq, Connect, Mail, Sheet, CRM: `from` must be `zoho.adminuserid`, `zoho.loginuserid`*, or verified email; otherwise → fails.
- In Zoho Cliq, Connect, Mail, Sheet, CRM: `from` must be `zoho.loginuserid` or verified email.

CANONICAL_EXAMPLES:
```deluge
// Basic send with CC and reply-to
sendmail [
  from: zoho.adminuserid
  to: "shawn@zylker.com"
  cc: "salesmanager@zoho.com"
  reply to: "support@zylker.com"
  subject: "Your CRM record is ready"
  message: "<p>Registration successful.</p>"
]

// With file attachment fetched via invokeUrl
fileResp = invokeUrl[url:"https://example.com/file.png" type:GET];
sendmail [
  from: zoho.adminuserid
  to: candidate_email
  subject: "Welcome aboard"
  message: "Here is your welcome file."
  Attachments: file: fileResp
]
```

FAILURE_MODES:
- Gmail address as `from` → fails from February 1, 2024.
- Unverified/non-admin from address in restricted services → error while saving or runtime error.
- Attachments exceed 15 MB → email delivered without attachments.
- More than 20 `reply to` addresses → maximum of 20 accepted.

RELATED_DOCS:
- Send SMS — https://www.zoho.com/deluge/help/misc-statements/send-mail.html

SOURCE:
https://www.zoho.com/deluge/help/misc-statements/send-mail.html
