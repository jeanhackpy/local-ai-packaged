Simple Crawling - Crawl4AI Documentation (v0.4.3bx)
Simple Crawling
This guide covers the basics of web crawling with Crawl4AI. You'll learn how to set up a crawler, make your first request, and understand the response.
Basic Usage
Set up a simple crawl using
BrowserConfig
and
CrawlerRunConfig
:
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
from
crawl4ai.async\_configs
import
BrowserConfig
,
CrawlerRunConfig
async
def
main
():
browser\_config
=
BrowserConfig
()
# Default browser configuration
run\_config
=
CrawlerRunConfig
()
# Default crawl run configuration
async
with
AsyncWebCrawler
(
config
=
browser\_config
)
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
run\_config
)
print
(
result
.
markdown
)
# Print clean markdown content
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
Understanding the Response
The
arun()
method returns a
CrawlResult
object with several useful properties. Here's a quick overview (see
CrawlResult
for complete details):
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
CrawlerRunConfig
(
fit\_markdown
=
True
)
)
# Different content formats
print
(
result
.
html
)
# Raw HTML
print
(
result
.
cleaned\_html
)
# Cleaned HTML
print
(
result
.
markdown
)
# Markdown version
print
(
result
.
fit\_markdown
)
# Most relevant content in markdown
# Check success status
print
(
result
.
success
)
# True if crawl succeeded
print
(
result
.
status\_code
)
# HTTP status code (e.g., 200, 404)
# Access extracted media and links
print
(
result
.
media
)
# Dictionary of found media (images, videos, audio)
print
(
result
.
links
)
# Dictionary of internal and external links
Adding Basic Options
Customize your crawl using
CrawlerRunConfig
:
run\_config
=
CrawlerRunConfig
(
word\_count\_threshold
=
10
,
# Minimum words per content block
exclude\_external\_links
=
True
,
# Remove external links
remove\_overlay\_elements
=
True
,
# Remove popups/modals
process\_iframes
=
True
# Process iframe content
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
run\_config
)
Handling Errors
Always check if the crawl was successful:
run\_config
=
CrawlerRunConfig
()
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
run\_config
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
"Crawl failed:
{
result
.
error\_message
}
"
)
print
(
f
"Status code:
{
result
.
status\_code
}
"
)
Logging and Debugging
Enable verbose logging in
BrowserConfig
:
browser\_config
=
BrowserConfig
(
verbose
=
True
)
async
with
AsyncWebCrawler
(
config
=
browser\_config
)
as
crawler
:
run\_config
=
CrawlerRunConfig
()
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
run\_config
)
Complete Example
Here's a more comprehensive example demonstrating common usage patterns:
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
from
crawl4ai.async\_configs
import
BrowserConfig
,
CrawlerRunConfig
,
CacheMode
async
def
main
():
browser\_config
=
BrowserConfig
(
verbose
=
True
)
run\_config
=
CrawlerRunConfig
(
# Content filtering
word\_count\_threshold
=
10
,
excluded\_tags
=
[
'form'
,
'header'
],
exclude\_external\_links
=
True
,
# Content processing
process\_iframes
=
True
,
remove\_overlay\_elements
=
True
,
# Cache control
cache\_mode
=
CacheMode
.
ENABLED
# Use cache if available
)
async
with
AsyncWebCrawler
(
config
=
browser\_config
)
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
run\_config
)
if
result
.
success
:
# Print clean content
print
(
"Content:"
,
result
.
markdown
[:
500
])
# First 500 chars
# Process images
for
image
in
result
.
media
[
"images"
]:
print
(
f
"Found image:
{
image
[
'src'
]
}
"
)
# Process links
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
"Internal link:
{
link
[
'href'
]
}
"
)
else
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
Search
Type to start searching