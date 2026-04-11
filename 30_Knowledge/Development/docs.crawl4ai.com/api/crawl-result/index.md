CrawlResult - Crawl4AI Documentation (v0.4.3bx)
CrawlResult
Reference
The
CrawlResult
class encapsulates everything returned after a single crawl operation. It provides the
raw or processed content
, details on links and media, plus optional metadata (like screenshots, PDFs, or extracted JSON).
Location
:
crawl4ai/crawler/models.py
(for reference)
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
dispatch\_result
:
Optional
[
DispatchResult
]
=
None
...
Below is a
field-by-field
explanation and possible usage patterns.
1. Basic Crawl Info
1.1
url
(str)
What
: The final crawled URL (after any redirects).
Usage
:
print
(
result
.
url
)
# e.g., "https://example.com/"
1.2
success
(bool)
What
:
True
if the crawl pipeline ended without major errors;
False
otherwise.
Usage
:
if
not
result
.
success
:
print
(
f
"Crawl failed:
{
result
.
error\_message
}
"
)
1.3
status\_code
(Optional[int])
What
: The page’s HTTP status code (e.g., 200, 404).
Usage
:
if
result
.
status\_code
==
404
:
print
(
"Page not found!"
)
1.4
error\_message
(Optional[str])
What
: If
success=False
, a textual description of the failure.
Usage
:
if
not
result
.
success
:
print
(
"Error:"
,
result
.
error\_message
)
1.5
session\_id
(Optional[str])
What
: The ID used for reusing a browser context across multiple calls.
Usage
:
# If you used session\_id="login\_session" in CrawlerRunConfig, see it here:
print
(
"Session:"
,
result
.
session\_id
)
1.6
response\_headers
(Optional[dict])
What
: Final HTTP response headers.
Usage
:
if
result
.
response\_headers
:
print
(
"Server:"
,
result
.
response\_headers
.
get
(
"Server"
,
"Unknown"
))
1.7
ssl\_certificate
(Optional[SSLCertificate])
What
: If
fetch\_ssl\_certificate=True
in your CrawlerRunConfig,
result.ssl\_certificate
contains a
SSLCertificate
object describing the site’s certificate. You can export the cert in multiple formats (PEM/DER/JSON) or access its properties like
issuer
,
subject
,
valid\_from
,
valid\_until
, etc.
Usage
:
if
result
.
ssl\_certificate
:
print
(
"Issuer:"
,
result
.
ssl\_certificate
.
issuer
)
2. Raw / Cleaned Content
2.1
html
(str)
What
: The
original
unmodified HTML from the final page load.
Usage
:
# Possibly large
print
(
len
(
result
.
html
))
2.2
cleaned\_html
(Optional[str])
What
: A sanitized HTML version—scripts, styles, or excluded tags are removed based on your
CrawlerRunConfig
.
Usage
:
print
(
result
.
cleaned\_html
[:
500
])
# Show a snippet
2.3
fit\_html
(Optional[str])
What
: If a
content filter
or heuristic (e.g., Pruning/BM25) modifies the HTML, the “fit” or post-filter version.
When
: This is
only
present if your
markdown\_generator
or
content\_filter
produces it.
Usage
:
if
result
.
fit\_html
:
print
(
"High-value HTML content:"
,
result
.
fit\_html
[:
300
])
3. Markdown Fields
3.1 The Markdown Generation Approach
Crawl4AI can convert HTML→Markdown, optionally including:
Raw
markdown
Links as citations
(with a references section)
Fit
markdown if a
content filter
is used (like Pruning or BM25)
3.2
markdown\_v2
(Optional[MarkdownGenerationResult])
What
: The
structured
object holding multiple markdown variants. Soon to be consolidated into
markdown
.
MarkdownGenerationResult
includes:
-
raw\_markdown
(str)
: The full HTML→Markdown conversion.
-
markdown\_with\_citations
(str)
: Same markdown, but with link references as academic-style citations.
-
references\_markdown
(str)
: The reference list or footnotes at the end.
-
fit\_markdown
(Optional[str])
: If content filtering (Pruning/BM25) was applied, the filtered “fit” text.
-
fit\_html
(Optional[str])
: The HTML that led to
fit\_markdown
.
Usage
:
if
result
.
markdown\_v2
:
md\_res
=
result
.
markdown\_v2
print
(
"Raw MD:"
,
md\_res
.
raw\_markdown
[:
300
])
print
(
"Citations MD:"
,
md\_res
.
markdown\_with\_citations
[:
300
])
print
(
"References:"
,
md\_res
.
references\_markdown
)
if
md\_res
.
fit\_markdown
:
print
(
"Pruned text:"
,
md\_res
.
fit\_markdown
[:
300
])
3.3
markdown
(Optional[Union[str, MarkdownGenerationResult]])
What
: In future versions,
markdown
will fully replace
markdown\_v2
. Right now, it might be a
str
or a
MarkdownGenerationResult
.
Usage
:
# Soon, you might see:
if
isinstance
(
result
.
markdown
,
MarkdownGenerationResult
):
print
(
result
.
markdown
.
raw\_markdown
[:
200
])
else
:
print
(
result
.
markdown
)
3.4
fit\_markdown
(Optional[str])
What
: A direct reference to the final filtered markdown (legacy approach).
When
: This is set if a filter or content strategy explicitly writes there. Usually overshadowed by
markdown\_v2.fit\_markdown
.
Usage
:
print
(
result
.
fit\_markdown
)
# Legacy field, prefer result.markdown\_v2.fit\_markdown
Important
: “Fit” content (in
fit\_markdown
/
fit\_html
) only exists if you used a
filter
(like
PruningContentFilter
or
BM25ContentFilter
) within a
MarkdownGenerationStrategy
.
4. Media & Links
4.1
media
(Dict[str, List[Dict]])
What
: Contains info about discovered images, videos, or audio. Typically keys:
"images"
,
"videos"
,
"audios"
.
Common Fields
in each item:
src
(str)
: Media URL
alt
or
title
(str)
: Descriptive text
score
(float)
: Relevance score if the crawler’s heuristic found it “important”
desc
or
description
(Optional[str])
: Additional context extracted from surrounding text
Usage
:
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
if
img
.
get
(
"score"
,
0
)
>
5
:
print
(
"High-value image:"
,
img
[
"src"
])
4.2
links
(Dict[str, List[Dict]])
What
: Holds internal and external link data. Usually two keys:
"internal"
and
"external"
.
Common Fields
:
href
(str)
: The link target
text
(str)
: Link text
title
(str)
: Title attribute
context
(str)
: Surrounding text snippet
domain
(str)
: If external, the domain
Usage
:
for
link
in
result
.
links
[
"internal"
]:
print
(
f
"Internal link to
{
link
[
'href'
]
}
with text
{
link
[
'text'
]
}
"
)
5. Additional Fields
5.1
extracted\_content
(Optional[str])
What
: If you used
extraction\_strategy
(CSS, LLM, etc.), the structured output (JSON).
Usage
:
if
result
.
extracted\_content
:
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
5.2
downloaded\_files
(Optional[List[str]])
What
: If
accept\_downloads=True
in your
BrowserConfig
+
downloads\_path
, lists local file paths for downloaded items.
Usage
:
if
result
.
downloaded\_files
:
for
file\_path
in
result
.
downloaded\_files
:
print
(
"Downloaded:"
,
file\_path
)
5.3
screenshot
(Optional[str])
What
: Base64-encoded screenshot if
screenshot=True
in
CrawlerRunConfig
.
Usage
:
import
base64
if
result
.
screenshot
:
with
open
(
"page.png"
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
base64
.
b64decode
(
result
.
screenshot
))
5.4
pdf
(Optional[bytes])
What
: Raw PDF bytes if
pdf=True
in
CrawlerRunConfig
.
Usage
:
if
result
.
pdf
:
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
5.5
metadata
(Optional[dict])
What
: Page-level metadata if discovered (title, description, OG data, etc.).
Usage
:
if
result
.
metadata
:
print
(
"Title:"
,
result
.
metadata
.
get
(
"title"
))
print
(
"Author:"
,
result
.
metadata
.
get
(
"author"
))
6.
dispatch\_result
(optional)
A
DispatchResult
object providing additional concurrency and resource usage information when crawling URLs in parallel (e.g., via
arun\_many()
with custom dispatchers). It contains:
task\_id
: A unique identifier for the parallel task.
memory\_usage
(float): The memory (in MB) used at the time of completion.
peak\_memory
(float): The peak memory usage (in MB) recorded during the task’s execution.
start\_time
/
end\_time
(datetime): Time range for this crawling task.
error\_message
(str): Any dispatcher- or concurrency-related error encountered.
# Example usage:
for
result
in
results
:
if
result
.
success
and
result
.
dispatch\_result
:
dr
=
result
.
dispatch\_result
print
(
f
"URL:
{
result
.
url
}
, Task ID:
{
dr
.
task\_id
}
"
)
print
(
f
"Memory:
{
dr
.
memory\_usage
:
.1f
}
MB (Peak:
{
dr
.
peak\_memory
:
.1f
}
MB)"
)
print
(
f
"Duration:
{
dr
.
end\_time
-
dr
.
start\_time
}
"
)
Note
: This field is typically populated when using
arun\_many(...)
alongside a
dispatcher
(e.g.,
MemoryAdaptiveDispatcher
or
SemaphoreDispatcher
). If no concurrency or dispatcher is used,
dispatch\_result
may remain
None
.
7. Example: Accessing Everything
async
def
handle\_result
(
result
:
CrawlResult
):
if
not
result
.
success
:
print
(
"Crawl error:"
,
result
.
error\_message
)
return
# Basic info
print
(
"Crawled URL:"
,
result
.
url
)
print
(
"Status code:"
,
result
.
status\_code
)
# HTML
print
(
"Original HTML size:"
,
len
(
result
.
html
))
print
(
"Cleaned HTML size:"
,
len
(
result
.
cleaned\_html
or
""
))
# Markdown output
if
result
.
markdown\_v2
:
print
(
"Raw Markdown:"
,
result
.
markdown\_v2
.
raw\_markdown
[:
300
])
print
(
"Citations Markdown:"
,
result
.
markdown\_v2
.
markdown\_with\_citations
[:
300
])
if
result
.
markdown\_v2
.
fit\_markdown
:
print
(
"Fit Markdown:"
,
result
.
markdown\_v2
.
fit\_markdown
[:
200
])
else
:
print
(
"Raw Markdown (legacy):"
,
result
.
markdown
[:
200
]
if
result
.
markdown
else
"N/A"
)
# Media & Links
if
"images"
in
result
.
media
:
print
(
"Image count:"
,
len
(
result
.
media
[
"images"
]))
if
"internal"
in
result
.
links
:
print
(
"Internal link count:"
,
len
(
result
.
links
[
"internal"
]))
# Extraction strategy result
if
result
.
extracted\_content
:
print
(
"Structured data:"
,
result
.
extracted\_content
)
# Screenshot/PDF
if
result
.
screenshot
:
print
(
"Screenshot length:"
,
len
(
result
.
screenshot
))
if
result
.
pdf
:
print
(
"PDF bytes length:"
,
len
(
result
.
pdf
))
8. Key Points & Future
1.
markdown\_v2
vs
markdown
- Right now,
markdown\_v2
is the more robust container (
MarkdownGenerationResult
), providing
raw\_markdown
,
markdown\_with\_citations
, references, plus possible
fit\_markdown
.
- In future versions, everything will unify under
markdown
. If you rely on advanced features (citations, fit content), check
markdown\_v2
.
2.
Fit Content
-
fit\_markdown
and
fit\_html
appear only if you used a content filter (like
PruningContentFilter
or
BM25ContentFilter
) inside your
MarkdownGenerationStrategy
or set them directly.
- If no filter is used, they remain
None
.
3.
References & Citations
- If you enable link citations in your
DefaultMarkdownGenerator
(
options={"citations": True}
), you’ll see
markdown\_with\_citations
plus a
references\_markdown
block. This helps large language models or academic-like referencing.
4.
Links & Media
-
links["internal"]
and
links["external"]
group discovered anchors by domain.
-
media["images"]
/
["videos"]
/
["audios"]
store extracted media elements with optional scoring or context.
5.
Error Cases
- If
success=False
, check
error\_message
(e.g., timeouts, invalid URLs).
-
status\_code
might be
None
if we failed before an HTTP response.
Use
CrawlResult
to glean all final outputs and feed them into your data pipelines, AI models, or archives. With the synergy of a properly configured
BrowserConfig
and
CrawlerRunConfig
, the crawler can produce robust, structured results here in
CrawlResult
.
Search
Type to start searching