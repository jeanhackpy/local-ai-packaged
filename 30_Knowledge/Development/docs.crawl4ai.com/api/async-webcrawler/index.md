AsyncWebCrawler - Crawl4AI Documentation (v0.4.3bx)
AsyncWebCrawler
The
AsyncWebCrawler
is the core class for asynchronous web crawling in Crawl4AI. You typically create it
once
, optionally customize it with a
BrowserConfig
(e.g., headless, user agent), then
run
multiple
arun()
calls with different
CrawlerRunConfig
objects.
Recommended usage
:
1.
Create
a
BrowserConfig
for global browser settings.
2.
Instantiate
AsyncWebCrawler(config=browser\_config)
.
3.
Use
the crawler in an async context manager (
async with
) or manage start/close manually.
4.
Call
arun(url, config=crawler\_run\_config)
for each page you want.
1. Constructor Overview
class
AsyncWebCrawler
:
def
\_\_init\_\_
(
self
,
crawler\_strategy
:
Optional
[
AsyncCrawlerStrategy
]
=
None
,
config
:
Optional
[
BrowserConfig
]
=
None
,
always\_bypass\_cache
:
bool
=
False
,
# deprecated
always\_by\_pass\_cache
:
Optional
[
bool
]
=
None
,
# also deprecated
base\_directory
:
str
=
...
,
thread\_safe
:
bool
=
False
,
\*\*
kwargs
,
):
"""
Create an AsyncWebCrawler instance.
Args:
crawler\_strategy:
(Advanced) Provide a custom crawler strategy if needed.
config:
A BrowserConfig object specifying how the browser is set up.
always\_bypass\_cache:
(Deprecated) Use CrawlerRunConfig.cache\_mode instead.
base\_directory:
Folder for storing caches/logs (if relevant).
thread\_safe:
If True, attempts some concurrency safeguards. Usually False.
\*\*kwargs:
Additional legacy or debugging parameters.
"""
)
### Typical Initialization
```
python
from
crawl4ai
import
AsyncWebCrawler
,
BrowserConfig
browser\_cfg
=
BrowserConfig
(
browser\_type
=
"chromium"
,
headless
=
True
,
verbose
=
True
)
crawler
=
AsyncWebCrawler
(
config
=
browser\_cfg
)
Notes
:
Legacy
parameters like
always\_bypass\_cache
remain for backward compatibility, but prefer to set
caching
in
CrawlerRunConfig
.
2. Lifecycle: Start/Close or Context Manager
2.1 Context Manager (Recommended)
async
with
AsyncWebCrawler
(
config
=
browser\_cfg
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
"https://example.com"
)
# The crawler automatically starts/closes resources
When the
async with
block ends, the crawler cleans up (closes the browser, etc.).
2.2 Manual Start & Close
crawler
=
AsyncWebCrawler
(
config
=
browser\_cfg
)
await
crawler
.
start
()
result1
=
await
crawler
.
arun
(
"https://example.com"
)
result2
=
await
crawler
.
arun
(
"https://another.com"
)
await
crawler
.
close
()
Use this style if you have a
long-running
application or need full control of the crawler’s lifecycle.
3. Primary Method:
arun()
async
def
arun
(
self
,
url
:
str
,
config
:
Optional
[
CrawlerRunConfig
]
=
None
,
# Legacy parameters for backward compatibility...
)
->
CrawlResult
:
...
3.1 New Approach
You pass a
CrawlerRunConfig
object that sets up everything about a crawl—content filtering, caching, session reuse, JS code, screenshots, etc.
import
asyncio
from
crawl4ai
import
CrawlerRunConfig
,
CacheMode
run\_cfg
=
CrawlerRunConfig
(
cache\_mode
=
CacheMode
.
BYPASS
,
css\_selector
=
"main.article"
,
word\_count\_threshold
=
10
,
screenshot
=
True
)
async
with
AsyncWebCrawler
(
config
=
browser\_cfg
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
"https://example.com/news"
,
config
=
run\_cfg
)
print
(
"Crawled HTML length:"
,
len
(
result
.
cleaned\_html
))
if
result
.
screenshot
:
print
(
"Screenshot base64 length:"
,
len
(
result
.
screenshot
))
3.2 Legacy Parameters Still Accepted
For
backward
compatibility,
arun()
can still accept direct arguments like
css\_selector=...
,
word\_count\_threshold=...
, etc., but we strongly advise migrating them into a
CrawlerRunConfig
.
4. Batch Processing:
arun\_many()
async
def
arun\_many
(
self
,
urls
:
List
[
str
],
config
:
Optional
[
CrawlerRunConfig
]
=
None
,
# Legacy parameters maintained for backwards compatibility...
)
->
List
[
CrawlResult
]:
"""
Process multiple URLs with intelligent rate limiting and resource monitoring.
"""
4.1 Resource-Aware Crawling
The
arun\_many()
method now uses an intelligent dispatcher that:
Monitors system memory usage
Implements adaptive rate limiting
Provides detailed progress monitoring
Manages concurrent crawls efficiently
4.2 Example Usage
from
crawl4ai
import
AsyncWebCrawler
,
BrowserConfig
,
CrawlerRunConfig
,
RateLimitConfig
from
crawl4ai.dispatcher
import
DisplayMode
# Configure browser
browser\_cfg
=
BrowserConfig
(
headless
=
True
)
# Configure crawler with rate limiting
run\_cfg
=
CrawlerRunConfig
(
# Enable rate limiting
enable\_rate\_limiting
=
True
,
rate\_limit\_config
=
RateLimitConfig
(
base\_delay
=
(
1.0
,
2.0
),
# Random delay between 1-2 seconds
max\_delay
=
30.0
,
# Maximum delay after rate limit hits
max\_retries
=
2
,
# Number of retries before giving up
rate\_limit\_codes
=
[
429
,
503
]
# Status codes that trigger rate limiting
),
# Resource monitoring
memory\_threshold\_percent
=
70.0
,
# Pause if memory exceeds this
check\_interval
=
0.5
,
# How often to check resources
max\_session\_permit
=
3
,
# Maximum concurrent crawls
display\_mode
=
DisplayMode
.
DETAILED
.
value
# Show detailed progress
)
urls
=
[
"https://example.com/page1"
,
"https://example.com/page2"
,
"https://example.com/page3"
]
async
with
AsyncWebCrawler
(
config
=
browser\_cfg
)
as
crawler
:
results
=
await
crawler
.
arun\_many
(
urls
,
config
=
run\_cfg
)
for
result
in
results
:
print
(
f
"URL:
{
result
.
url
}
, Success:
{
result
.
success
}
"
)
4.3 Key Features
1.
Rate Limiting
Automatic delay between requests
Exponential backoff on rate limit detection
Domain-specific rate limiting
Configurable retry strategy
2.
Resource Monitoring
Memory usage tracking
Adaptive concurrency based on system load
Automatic pausing when resources are constrained
3.
Progress Monitoring
Detailed or aggregated progress display
Real-time status updates
Memory usage statistics
4.
Error Handling
Graceful handling of rate limits
Automatic retries with backoff
Detailed error reporting
5.
CrawlResult
Output
Each
arun()
returns a
CrawlResult
containing:
url
: Final URL (if redirected).
html
: Original HTML.
cleaned\_html
: Sanitized HTML.
markdown\_v2
(or future
markdown
): Markdown outputs (raw, fit, etc.).
extracted\_content
: If an extraction strategy was used (JSON for CSS/LLM strategies).
screenshot
,
pdf
: If screenshots/PDF requested.
media
,
links
: Information about discovered images/links.
success
,
error\_message
: Status info.
For details, see
CrawlResult doc
.
6. Quick Example
Below is an example hooking it all together:
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
,
BrowserConfig
,
CrawlerRunConfig
,
CacheMode
from
crawl4ai.extraction\_strategy
import
JsonCssExtractionStrategy
import
json
async
def
main
():
# 1. Browser config
browser\_cfg
=
BrowserConfig
(
browser\_type
=
"firefox"
,
headless
=
False
,
verbose
=
True
)
# 2. Run config
schema
=
{
"name"
:
"Articles"
,
"baseSelector"
:
"article.post"
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
"url"
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
run\_cfg
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
),
word\_count\_threshold
=
15
,
remove\_overlay\_elements
=
True
,
wait\_for
=
"css:.post"
# Wait for posts to appear
)
async
with
AsyncWebCrawler
(
config
=
browser\_cfg
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
"https://example.com/blog"
,
config
=
run\_cfg
)
if
result
.
success
:
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
result
.
extracted\_content
:
articles
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
"Extracted articles:"
,
articles
[:
2
])
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
asyncio
.
run
(
main
())
Explanation
:
We define a
BrowserConfig
with Firefox, no headless, and
verbose=True
.
We define a
CrawlerRunConfig
that
bypasses cache
, uses a
CSS
extraction schema, has a
word\_count\_threshold=15
, etc.
We pass them to
AsyncWebCrawler(config=...)
and
arun(url=..., config=...)
.
7. Best Practices & Migration Notes
1.
Use
BrowserConfig
for
global
settings about the browser’s environment. 
2.
Use
CrawlerRunConfig
for
per-crawl
logic (caching, content filtering, extraction strategies, wait conditions). 
3.
Avoid
legacy parameters like
css\_selector
or
word\_count\_threshold
directly in
arun()
. Instead:
run\_cfg
=
CrawlerRunConfig
(
css\_selector
=
".main-content"
,
word\_count\_threshold
=
20
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
"..."
,
config
=
run\_cfg
)
4.
Context Manager
usage is simplest unless you want a persistent crawler across many calls.
8. Summary
AsyncWebCrawler
is your entry point to asynchronous crawling:
Constructor
accepts
BrowserConfig
(or defaults).
arun(url, config=CrawlerRunConfig)
is the main method for single-page crawls.
arun\_many(urls, config=CrawlerRunConfig)
handles concurrency across multiple URLs.
For advanced lifecycle control, use
start()
and
close()
explicitly.
Migration
:
If you used
AsyncWebCrawler(browser\_type="chromium", css\_selector="...")
, move browser settings to
BrowserConfig(...)
and content/crawl logic to
CrawlerRunConfig(...)
.
This modular approach ensures your code is
clean
,
scalable
, and
easy to maintain
. For any advanced or rarely used parameters, see the
BrowserConfig docs
.
Search
Type to start searching