FILE_PURPOSE: Deluge zoho.file.convertToPDF — convert an HTML string or public URL into a PDF FILE object
MENTAL_MODEL: zoho.file.convertToPDF(html_or_url, options?) → FILE (PDF); one external API call per execution

WHEN_TO_USE:
- Generate a PDF from an HTML string (reports, invoices, certificates, dynamic documents).
- Convert a publicly accessible URL into a PDF.

WHEN_NOT_TO_USE:
- HTML content exceeds 12,000,000 characters → error.
- URL exceeds 25,000 characters → error.
- URL is not publicly accessible → PDF generation fails.

TRIGGER_KEYWORDS:
zoho.file.convertToPDF, options_collection, 12000000 HTML chars, 25000 URL chars, 301 seconds, external-calls quota

RULES:
- Syntax: `zoho.file.convertToPDF(<content_or_url>, <options_collection>);`
- First parameter: HTML STRING or public URL STRING (mutually exclusive).
- `options_collection` (optional KEY-VALUE): 20+ layout parameters — see table below.
- Return type: FILE (PDF).
- Max HTML content: 12,000,000 characters.
- Max URL length: 25,000 characters.
- Max processing time: 301 seconds; conversion exceeding this → timeout error.
- Counts as one external API call per execution (deducted from external calls quota).
- Returned FILE supports setFileName() and other file operations.
- Key options_collection parameters:
  - `scale` NUMBER (default 1), `landscape` BOOLEAN (default false).
  - `top-margin`, `bottom-margin`, `left-margin`, `right-margin` NUMBER (default 0).
  - `page-width` NUMBER (default 210), `page-height` NUMBER (default 297), `units` STRING (default "mm"; accepts px, in, cm, mm).
  - `header`/`footer` STRING (HTML content for header/footer sections).
  - `single-page-pdf` BOOLEAN (default false) — fits all content into one page.
  - `print-background` BOOLEAN (default true) — includes background colors/images.
  - `disable-javascript` BOOLEAN (default false).
  - `page-ranges` STRING — e.g. "4-8" or "2,3,4" or "2, 4-5".

CANONICAL_EXAMPLES:
```deluge
// Convert HTML string
content = "<html><body>Page One <div style='page-break-after:always'></div> Page Two</body></html>";
file = zoho.file.convertToPDF(content);
info file.isFile(); // true

// Convert URL and rename output
file = zoho.file.convertToPDF("https://www.zoho.com/deluge/");
file.setFileName("DelugeHomepage");

// With custom layout options
params = collection();
params.insert("top-margin":"5");
params.insert("page-width":"3.3");
params.insert("single-page-pdf":true);
file = zoho.file.convertToPDF(content, params);
```

FAILURE_MODES:
- URL length > 25,000 characters → `{"Message":"Unable to process your request","details":{"param name":"url","Error":"More than maximum length","StatusCode":400}}`.
- HTML content > 12,000,000 characters → error.
- Processing exceeds 301 seconds → timeout error.
- Non-public URL → PDF generation fails (explicit error not documented in source).
- Excessive calls exhaust external-calls quota for the invoking service.

RELATED_DOCS:
- Get File Content — get-file-content.dou.md
- setFileName — set-file-name.dou.md
- File Methods — ../datatypes/../datatypes/file.dou.md

SOURCE:
https://www.zoho.com/deluge/help/functions/file/convert-to-pdf.html
