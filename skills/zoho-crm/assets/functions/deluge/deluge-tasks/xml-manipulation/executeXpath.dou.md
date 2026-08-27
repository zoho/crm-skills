FILE_PURPOSE: Deluge `executeXpath()` — query XML or JSON text using XPath expressions to extract node values.
MENTAL_MODEL: `xmlText.executeXPath(xpathExpr)` = evaluate XPath against XML/JSON string; always returns TEXT.

WHEN_TO_USE:
- Extract specific elements from an XML API response using standard XPath expressions.
- Parse a JSON response with XPath by prepending `/root` to the path.
- Chain two `executeXPath()` calls to navigate nested XML structures or extract attribute values.

WHEN_NOT_TO_USE:
- When the response is already a Deluge Key-Value map — access keys directly without XPath.
- When no node selection is needed and the full string is sufficient.

TRIGGER_KEYWORDS:
executeXPath, /root JSON XPath prefix, XPath-attribute extraction, chained-XPath calls, XML node traversal, invalid-XPath runtime

RULES:
- Syntax: `<variable> = <xml_or_json>.executeXPath(<xpath>);`
- Return type: TEXT always.
- JSON input requires `/root` prepended to the XPath; the returned value is wrapped in XML-style tags matching the key (e.g. `<city>Surat</city>`), not a raw string.
- An invalid XPath expression raises a runtime error.
- `executeXPath()` calls can be chained: `response.executeXPath(expr1).executeXPath(expr2)`.

CANONICAL_EXAMPLES:
```deluge
// XML: fetch node values from a web resource
xmlResp = invokeurl[url: "https://www.w3schools.com/xml/cd_catalog.xml" type: GET];
info xmlResp.executexpath("/CATALOG/CD/TITLE");

// JSON: add /root prefix; result is tag-wrapped
jsonResp = invokeurl[url: "https://tools.learningcontainer.com/sample-json.json" type: GET];
info jsonResp.executexpath("/root/address/city");
// returns <city>Surat</city>

// Fetch attribute value (chained calls)
text = "<a href=\"https://example.com/file.pdf\" target=\"_blank\">Title</a>";
info text.executeXPath("/a/@href").executeXpath("/href/text()");
// returns https://example.com/file.pdf

// Fetch 3rd book node then extract its title
info xmlString.executeXPath("/bookstore/book[3]").executeXPath("/book/title/text()");
// returns: Learning XML
```

FAILURE_MODES:
- An invalid XPath expression raises a runtime error at execution time.
- JSON input without the `/root` prefix produces an incorrect or empty result silently.
- JSON return values are wrapped in XML-style tags (e.g. `<city>Surat</city>`); chain `.executeXPath("/tagname/text()")` to extract the raw string without the tags.

RELATED_DOCS:
- XML manipulation overview — https://www.zoho.com/deluge/help/xml-manipulation/executexpath.html
- invokeUrl task — ../../integrations/invokeurl-task.dou.md

SOURCE:
https://www.zoho.com/deluge/help/xml-manipulation/executexpath.html
