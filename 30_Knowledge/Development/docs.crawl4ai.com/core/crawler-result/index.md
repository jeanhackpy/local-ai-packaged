Crawler Result - Crawl4AI Documentation (v0.4.3bx)
Crawl Result and Output
When you call
arun()
on a page, Crawl4AI returns a
CrawlResult
object containing everything you might need—raw HTML, a cleaned version, optional screenshots or PDFs, structured extraction results, and more. This document explains those fields and how they map to different output types.
1. The
CrawlResult
Model
Below is the core schema. Each field captures a different aspect of the crawl’s result:
class
MarkdownGenerationResult
(
BaseModel
):
raw\_markdown
:
str
markdown\_with\_citations
:
str
references\_markdown
:
str
fit\_markdown
:
Optional
[
str
]
=
None
fit\_html
:
Optional
[
str
]
=
None
class
CrawlResult
(
BaseModel
):
url
:
str
html
:
str
success
:
bool
cleaned\_html
:
Optional
[
str
]
=
None
media
:
Dict
[
str
,
List
[
Dict
]]
=
{}
links
:
Dict
[
str
,
List
[
Dict
]]
=
{}
downloaded\_files
:
Optional
[
List
[
str
]]
=
None
screenshot
:
Optional
[
str
]
=
None
pdf
:
Optional
[
bytes
]
=
None
markdown
:
Optional
[
Union
[
str
,
MarkdownGenerationResult
]]
=
None
markdown\_v2
:
Optional
[
MarkdownGenerationResult
]
=
None
extracted\_content
:
Optional
[
str
]
=
None
metadata
:
Optional
[
dict
]
=
None
error\_message
:
Optional
[
str
]
=
None
session\_id
:
Optional
[
str
]
=
None
response\_headers
:
Optional
[
dict
]
=
None
status\_code
:
Optional
[
int
]
=
None
ssl\_certificate
:
Optional
[
SSLCertificate
]
=
None
class
Config
:
arbitrary\_types\_allowed
=
True
Table: Key Fields in
CrawlResult
Field (Name & Type)
Description
url (
str
)
The final or actual URL crawled (in case of redirects).
html (
str
)
Original, unmodified page HTML. Good for debugging or custom processing.
success (
bool
)
True
if the crawl completed without major errors, else
False
.
cleaned\_html (
Optional[str]
)
Sanitized HTML with scripts/styles removed; can exclude tags if configured via
excluded\_tags
etc.
media (
Dict[str, List[Dict]]
)
Extracted media info (images, audio, etc.), each with attributes like
src
,
alt
,
score
, etc.
links (
Dict[str, List[Dict]]
)
Extracted link data, split by
internal
and
external
. Each link usually has
href
,
text
, etc.
downloaded\_files (
Optional[List[str]]
)
If
accept\_downloads=True
in
BrowserConfig
, this lists the filepaths of saved downloads.
screenshot (
Optional[str]
)
Screenshot of the page (base64-encoded) if
screenshot=True
.
pdf (
Optional[bytes]
)
PDF of the page if
pdf=True
.
markdown (
Optional[str or MarkdownGenerationResult]
)
For now,
markdown\_v2
holds a
MarkdownGenerationResult
. Over time, this will be consolidated into
markdown
. The generator can provide raw markdown, citations, references, and optionally
fit\_markdown
.
markdown\_v2 (
Optional[MarkdownGenerationResult]
)
Legacy field for detailed markdown output. This will be replaced by
markdown
soon.
extracted\_content (
Optional[str]
)
The output of a structured extraction (CSS/LLM-based) stored as JSON string or other text.
metadata (
Optional[dict]
)
Additional info about the crawl or extracted data.
error\_message (
Optional[str]
)
If
success=False
, contains a short description of what went wrong.
session\_id (
Optional[str]
)
The ID of the session used for multi-page or persistent crawling.
response\_headers (
Optional[dict]
)
HTTP response headers, if captured.
status\_code (
Optional[int]
)
HTTP status code (e.g., 200 for OK).
ssl\_certificate (
Optional[SSLCertificate]
)
SSL certificate info if
fetch\_ssl\_certificate=True
.
2. HTML Variants
html
: Raw HTML
Crawl4AI preserves the exact HTML as
result.html
. Useful for:
Debugging page issues or checking the original content.
Performing your own specialized parse if needed.
cleaned\_html
: Sanitized
If you specify any cleanup or exclusion parameters in
CrawlerRunConfig
(like
excluded\_tags
,
remove\_forms
, etc.), you’ll see the result here:
config
=
CrawlerRunConfig
(
excluded\_tags
=
[
"form"
,
"header"
,
"footer"
],
keep\_data\_attributes
=
False
)
result
=
await
crawler
.
arun
(
"https://example.com"
,
config
=
config
)
print
(
result
.
cleaned\_html
)
# Freed of forms, header, footer, data-\* attributes
3. Markdown Generation
3.1
markdown\_v2
(Legacy) vs
markdown
markdown\_v2
: The current location for detailed markdown output, returning a
MarkdownGenerationResult
object.
markdown
: Eventually, we’re merging these fields. For now, you might see
result.markdown\_v2
used widely in code examples.
MarkdownGenerationResult
Fields:
Field
Description
raw\_markdown
The basic HTML→Markdown conversion.
markdown\_with\_citations
Markdown including inline citations that reference links at the end.
references\_markdown
The references/citations themselves (if
citations=True
).
fit\_markdown
The filtered/“fit” markdown if a content filter was used.
fit\_html
The filtered HTML that generated
fit\_markdown
.
3.2 Basic Example with a Markdown Generator
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
from
crawl4ai.markdown\_generation\_strategy
import
DefaultMarkdownGenerator
config
=
CrawlerRunConfig
(
markdown\_generator
=
DefaultMarkdownGenerator
(
options
=
{
"citations"
:
True
,
"body\_width"
:
80
}
# e.g. pass html2text style options
)
)
result
=
await
crawler
.
arun
(
url
=
"https://example.com"
,
config
=
config
)
md\_res
=
result
.
markdown\_v2
# or eventually 'result.markdown'
print
(
md\_res
.
raw\_markdown
[:
500
])
print
(
md\_res
.
markdown\_with\_citations
)
print
(
md\_res
.
references\_markdown
)
Note
: If you use a filter like
PruningContentFilter
, you’ll get
fit\_markdown
and
fit\_html
as well.
4. Structured Extraction:
extracted\_content
If you run a JSON-based extraction strategy (CSS, XPath, LLM, etc.), the structured data is
not
stored in
markdown
—it’s placed in
result.extracted\_content
as a JSON string (or sometimes plain text).
Example: CSS Extraction with
raw://
HTML
import
asyncio
import
json
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
,
CacheMode
from
crawl4ai.extraction\_strategy
import
JsonCssExtractionStrategy
async
def
main
():
schema
=
{
"name"
:
"Example Items"
,
"baseSelector"
:
"div.item"
,
"fields"
:
[
{
"name"
:
"title"
,
"selector"
:
"h2"
,
"type"
:
"text"
},
{
"name"
:
"link"
,
"selector"
:
"a"
,
"type"
:
"attribute"
,
"attribute"
:
"href"
}
]
}
raw\_html
=
"

Item 1
------

[Link 1](https://example.com/item1)"
async
with
AsyncWebCrawler
()
as
crawler
:
result
=
await
crawler
.
arun
(
url
=
"raw://"
+
raw\_html
,
config
=
CrawlerRunConfig
(
cache\_mode
=
CacheMode
.
BYPASS
,
extraction\_strategy
=
JsonCssExtractionStrategy
(
schema
)
)
)
data
=
json
.
loads
(
result
.
extracted\_content
)
print
(
data
)
if
\_\_name\_\_
==
"\_\_main\_\_"
:
asyncio
.
run
(
main
())
Here:
-
url="raw://..."
passes the HTML content directly, no network requests.
- The
CSS
extraction strategy populates
result.extracted\_content
with the JSON array
[{"title": "...", "link": "..."}]
.
5. More Fields: Links, Media, and More
5.1
links
A dictionary, typically with
"internal"
and
"external"
lists. Each entry might have
href
,
text
,
title
, etc. This is automatically captured if you haven’t disabled link extraction.
print
(
result
.
links
[
"internal"
][:
3
])
# Show first 3 internal links
5.2
media
Similarly, a dictionary with
"images"
,
"audio"
,
"video"
, etc. Each item could include
src
,
alt
,
score
, and more, if your crawler is set to gather them.
images
=
result
.
media
.
get
(
"images"
,
[])
for
img
in
images
:
print
(
"Image URL:"
,
img
[
"src"
],
"Alt:"
,
img
.
get
(
"alt"
))
5.3
screenshot
and
pdf
If you set
screenshot=True
or
pdf=True
in
CrawlerRunConfig
, then:
result.screenshot
contains a base64-encoded PNG string.
result.pdf
contains raw PDF bytes (you can write them to a file).
with
open
(
"page.pdf"
,
"wb"
)
as
f
:
f
.
write
(
result
.
pdf
)
5.4
ssl\_certificate
If
fetch\_ssl\_certificate=True
,
result.ssl\_certificate
holds details about the site’s SSL cert, such as issuer, validity dates, etc.
6. Accessing These Fields
After you run:
result
=
await
crawler
.
arun
(
url
=
"https://example.com"
,
config
=
some\_config
)
Check any field:
if
result
.
success
:
print
(
result
.
status\_code
,
result
.
response\_headers
)
print
(
"Links found:"
,
len
(
result
.
links
.
get
(
"internal"
,
[])))
if
result
.
markdown\_v2
:
print
(
"Markdown snippet:"
,
result
.
markdown\_v2
.
raw\_markdown
[:
200
])
if
result
.
extracted\_content
:
print
(
"Structured JSON:"
,
result
.
extracted\_content
)
else
:
print
(
"Error:"
,
result
.
error\_message
)
Remember
: Use
result.markdown\_v2
for now. It will eventually become
result.markdown
.
7. Next Steps
Markdown Generation
: Dive deeper into how to configure
DefaultMarkdownGenerator
and various filters.
Content Filtering
: Learn how to use
BM25ContentFilter
and
PruningContentFilter
.
Session & Hooks
: If you want to manipulate the page or preserve state across multiple
arun()
calls, see the hooking or session docs.
LLM Extraction
: For complex or unstructured content requiring AI-driven parsing, check the LLM-based strategies doc.
Enjoy
exploring all that
CrawlResult
offers—whether you need raw HTML, sanitized output, markdown, or fully structured data, Crawl4AI has you covered!
Search
Type to start searching