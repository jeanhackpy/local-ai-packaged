Content Selection - Crawl4AI Documentation (v0.4.3bx)
Content Selection
Crawl4AI provides multiple ways to
select
,
filter
, and
refine
the content from your crawls. Whether you need to target a specific CSS region, exclude entire tags, filter out external links, or remove certain domains and images,
CrawlerRunConfig
offers a wide range of parameters.
Below, we show how to configure these parameters and combine them for precise control.
1. CSS-Based Selection
A straightforward way to
limit
your crawl results to a certain region of the page is
css\_selector
in
CrawlerRunConfig
:
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
async
def
main
():
config
=
CrawlerRunConfig
(
# e.g., first 30 items from Hacker News
css\_selector
=
".athing:nth-child(-n+30)"
)
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
"https://news.ycombinator.com/newest"
,
config
=
config
)
print
(
"Partial HTML length:"
,
len
(
result
.
cleaned\_html
))
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
Result
: Only elements matching that selector remain in
result.cleaned\_html
.
2. Content Filtering & Exclusions
2.1 Basic Overview
config
=
CrawlerRunConfig
(
# Content thresholds
word\_count\_threshold
=
10
,
# Minimum words per block
# Tag exclusions
excluded\_tags
=
[
'form'
,
'header'
,
'footer'
,
'nav'
],
# Link filtering
exclude\_external\_links
=
True
,
exclude\_social\_media\_links
=
True
,
# Block entire domains
exclude\_domains
=
[
"adtrackers.com"
,
"spammynews.org"
],
exclude\_social\_media\_domains
=
[
"facebook.com"
,
"twitter.com"
],
# Media filtering
exclude\_external\_images
=
True
)
Explanation
:
word\_count\_threshold
: Ignores text blocks under X words. Helps skip trivial blocks like short nav or disclaimers.
excluded\_tags
: Removes entire tags (
,
,
, etc.).
Link Filtering
:
exclude\_external\_links
: Strips out external links and may remove them from
result.links
.
exclude\_social\_media\_links
: Removes links pointing to known social media domains.
exclude\_domains
: A custom list of domains to block if discovered in links.
exclude\_social\_media\_domains
: A curated list (override or add to it) for social media sites.
Media Filtering
:
exclude\_external\_images
: Discards images not hosted on the same domain as the main page (or its subdomains).
By default in case you set
exclude\_social\_media\_links=True
, the following social media domains are excluded:
[
'facebook.com'
,
'twitter.com'
,
'x.com'
,
'linkedin.com'
,
'instagram.com'
,
'pinterest.com'
,
'tiktok.com'
,
'snapchat.com'
,
'reddit.com'
,
]
2.2 Example Usage
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
,
CacheMode
async
def
main
():
config
=
CrawlerRunConfig
(
css\_selector
=
"main.content"
,
word\_count\_threshold
=
10
,
excluded\_tags
=
[
"nav"
,
"footer"
],
exclude\_external\_links
=
True
,
exclude\_social\_media\_links
=
True
,
exclude\_domains
=
[
"ads.com"
,
"spammytrackers.net"
],
exclude\_external\_images
=
True
,
cache\_mode
=
CacheMode
.
BYPASS
)
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
"https://news.ycombinator.com"
,
config
=
config
)
print
(
"Cleaned HTML length:"
,
len
(
result
.
cleaned\_html
))
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
Note
: If these parameters remove too much, reduce or disable them accordingly.
3. Handling Iframes
Some sites embed content in
tags. If you want that inline:
config
=
CrawlerRunConfig
(
# Merge iframe content into the final output
process\_iframes
=
True
,
remove\_overlay\_elements
=
True
)
Usage
:
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
async
def
main
():
config
=
CrawlerRunConfig
(
process\_iframes
=
True
,
remove\_overlay\_elements
=
True
)
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
"https://example.org/iframe-demo"
,
config
=
config
)
print
(
"Iframe-merged length:"
,
len
(
result
.
cleaned\_html
))
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
4. Structured Extraction Examples
You can combine content selection with a more advanced extraction strategy. For instance, a
CSS-based
or
LLM-based
extraction strategy can run on the filtered HTML.
4.1 Pattern-Based with
JsonCssExtractionStrategy
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
# Minimal schema for repeated items
schema
=
{
"name"
:
"News Items"
,
"baseSelector"
:
"tr.athing"
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
"a.storylink"
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
"a.storylink"
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
config
=
CrawlerRunConfig
(
# Content filtering
excluded\_tags
=
[
"form"
,
"header"
],
exclude\_domains
=
[
"adsite.com"
],
# CSS selection or entire page
css\_selector
=
"table.itemlist"
,
# No caching for demonstration
cache\_mode
=
CacheMode
.
BYPASS
,
# Extraction strategy
extraction\_strategy
=
JsonCssExtractionStrategy
(
schema
)
)
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
"https://news.ycombinator.com/newest"
,
config
=
config
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
"Sample extracted item:"
,
data
[:
1
])
# Show first item
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
4.2 LLM-Based Extraction
import
asyncio
import
json
from
pydantic
import
BaseModel
,
Field
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
from
crawl4ai.extraction\_strategy
import
LLMExtractionStrategy
class
ArticleData
(
BaseModel
):
headline
:
str
summary
:
str
async
def
main
():
llm\_strategy
=
LLMExtractionStrategy
(
provider
=
"openai/gpt-4"
,
api\_token
=
"sk-YOUR\_API\_KEY"
,
schema
=
ArticleData
.
schema
(),
extraction\_type
=
"schema"
,
instruction
=
"Extract 'headline' and a short 'summary' from the content."
)
config
=
CrawlerRunConfig
(
exclude\_external\_links
=
True
,
word\_count\_threshold
=
20
,
extraction\_strategy
=
llm\_strategy
)
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
"https://news.ycombinator.com"
,
config
=
config
)
article
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
article
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
Here, the crawler:
Filters out external links (
exclude\_external\_links=True
).
Ignores very short text blocks (
word\_count\_threshold=20
).
Passes the final HTML to your LLM strategy for an AI-driven parse.
5. Comprehensive Example
Below is a short function that unifies
CSS selection
,
exclusion
logic, and a pattern-based extraction, demonstrating how you can fine-tune your final data:
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
extract\_main\_articles
(
url
:
str
):
schema
=
{
"name"
:
"ArticleBlock"
,
"baseSelector"
:
"div.article-block"
,
"fields"
:
[
{
"name"
:
"headline"
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
"summary"
,
"selector"
:
".summary"
,
"type"
:
"text"
},
{
"name"
:
"metadata"
,
"type"
:
"nested"
,
"fields"
:
[
{
"name"
:
"author"
,
"selector"
:
".author"
,
"type"
:
"text"
},
{
"name"
:
"date"
,
"selector"
:
".date"
,
"type"
:
"text"
}
]
}
]
}
config
=
CrawlerRunConfig
(
# Keep only #main-content
css\_selector
=
"#main-content"
,
# Filtering
word\_count\_threshold
=
10
,
excluded\_tags
=
[
"nav"
,
"footer"
],
exclude\_external\_links
=
True
,
exclude\_domains
=
[
"somebadsite.com"
],
exclude\_external\_images
=
True
,
# Extraction
extraction\_strategy
=
JsonCssExtractionStrategy
(
schema
),
cache\_mode
=
CacheMode
.
BYPASS
)
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
url
,
config
=
config
)
if
not
result
.
success
:
print
(
f
"Error:
{
result
.
error\_message
}
"
)
return
None
return
json
.
loads
(
result
.
extracted\_content
)
async
def
main
():
articles
=
await
extract\_main\_articles
(
"https://news.ycombinator.com/newest"
)
if
articles
:
print
(
"Extracted Articles:"
,
articles
[:
2
])
# Show first 2
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
Why This Works
:
-
CSS
scoping with
#main-content
.
- Multiple
exclude\_
parameters to remove domains, external images, etc.
- A
JsonCssExtractionStrategy
to parse repeated article blocks.
6. Scraping Modes
Crawl4AI provides two different scraping strategies for HTML content processing:
WebScrapingStrategy
(BeautifulSoup-based, default) and
LXMLWebScrapingStrategy
(LXML-based). The LXML strategy offers significantly better performance, especially for large HTML documents.
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
,
LXMLWebScrapingStrategy
async
def
main
():
config
=
CrawlerRunConfig
(
scraping\_strategy
=
LXMLWebScrapingStrategy
()
# Faster alternative to default BeautifulSoup
)
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
"https://example.com"
,
config
=
config
)
You can also create your own custom scraping strategy by inheriting from
ContentScrapingStrategy
. The strategy must return a
ScrapingResult
object with the following structure:
from
crawl4ai
import
ContentScrapingStrategy
,
ScrapingResult
,
MediaItem
,
Media
,
Link
,
Links
class
CustomScrapingStrategy
(
ContentScrapingStrategy
):
def
scrap
(
self
,
url
:
str
,
html
:
str
,
\*\*
kwargs
)
->
ScrapingResult
:
# Implement your custom scraping logic here
return
ScrapingResult
(
cleaned\_html
=
"..."
,
# Cleaned HTML content
success
=
True
,
# Whether scraping was successful
media
=
Media
(
images
=
[
# List of images found
MediaItem
(
src
=
"https://example.com/image.jpg"
,
alt
=
"Image description"
,
desc
=
"Surrounding text"
,
score
=
1
,
type
=
"image"
,
group\_id
=
1
,
format
=
"jpg"
,
width
=
800
)
],
videos
=
[],
# List of videos (same structure as images)
audios
=
[]
# List of audio files (same structure as images)
),
links
=
Links
(
internal
=
[
# List of internal links
Link
(
href
=
"https://example.com/page"
,
text
=
"Link text"
,
title
=
"Link title"
,
base\_domain
=
"example.com"
)
],
external
=
[]
# List of external links (same structure)
),
metadata
=
{
# Additional metadata
"title"
:
"Page Title"
,
"description"
:
"Page description"
}
)
async
def
ascrap
(
self
,
url
:
str
,
html
:
str
,
\*\*
kwargs
)
->
ScrapingResult
:
# For simple cases, you can use the sync version
return
await
asyncio
.
to\_thread
(
self
.
scrap
,
url
,
html
,
\*\*
kwargs
)
Performance Considerations
The LXML strategy can be up to 10-20x faster than BeautifulSoup strategy, particularly when processing large HTML documents. However, please note:
LXML strategy is currently experimental
In some edge cases, the parsing results might differ slightly from BeautifulSoup
If you encounter any inconsistencies between LXML and BeautifulSoup results, please
raise an issue
with a reproducible example
Choose LXML strategy when:
- Processing large HTML documents (recommended for >100KB)
- Performance is critical
- Working with well-formed HTML
Stick to BeautifulSoup strategy (default) when:
- Maximum compatibility is needed
- Working with malformed HTML
- Exact parsing behavior is critical
7. Conclusion
By mixing
css\_selector
scoping,
content filtering
parameters, and advanced
extraction strategies
, you can precisely
choose
which data to keep. Key parameters in
CrawlerRunConfig
for content selection include:
1.
css\_selector
– Basic scoping to an element or region.
2.
word\_count\_threshold
– Skip short blocks.
3.
excluded\_tags
– Remove entire HTML tags.
4.
exclude\_external\_links
,
exclude\_social\_media\_links
,
exclude\_domains
– Filter out unwanted links or domains.
5.
exclude\_external\_images
– Remove images from external sources.
6.
process\_iframes
– Merge iframe content if needed.
Combine these with structured extraction (CSS, LLM-based, or others) to build powerful crawls that yield exactly the content you want, from raw or cleaned HTML up to sophisticated JSON structures. For more detail, see
Configuration Reference
. Enjoy curating your data to the max!
Search
Type to start searching