Browser & Crawler Config - Crawl4AI Documentation (v0.4.3bx)
Browser & Crawler Configuration (Quick Overview)
Crawl4AI’s flexibility stems from two key classes:
1.
BrowserConfig
– Dictates
how
the browser is launched and behaves (e.g., headless or visible, proxy, user agent).
2.
CrawlerRunConfig
– Dictates
how
each
crawl
operates (e.g., caching, extraction, timeouts, JavaScript code to run, etc.).
In most examples, you create
one
BrowserConfig
for the entire crawler session, then pass a
fresh
or re-used
CrawlerRunConfig
whenever you call
arun()
. This tutorial shows the most commonly used parameters. If you need advanced or rarely used fields, see the
Configuration Parameters
.
1. BrowserConfig Essentials
class
BrowserConfig
:
def
\_\_init\_\_
(
browser\_type
=
"chromium"
,
headless
=
True
,
proxy\_config
=
None
,
viewport\_width
=
1080
,
viewport\_height
=
600
,
verbose
=
True
,
use\_persistent\_context
=
False
,
user\_data\_dir
=
None
,
cookies
=
None
,
headers
=
None
,
user\_agent
=
None
,
text\_mode
=
False
,
light\_mode
=
False
,
extra\_args
=
None
,
# ... other advanced parameters omitted here
):
...
Key Fields to Note
1.
browser\_type
- Options:
"chromium"
,
"firefox"
, or
"webkit"
.
- Defaults to
"chromium"
.
- If you need a different engine, specify it here.
2.
headless
-
True
: Runs the browser in headless mode (invisible browser).
-
False
: Runs the browser in visible mode, which helps with debugging.
3.
proxy\_config
- A dictionary with fields like:
{
"server"
:
"http://proxy.example.com:8080"
,
"username"
:
"..."
,
"password"
:
"..."
}
- Leave as
None
if a proxy is not required.
4.
viewport\_width
&
viewport\_height
:
- The initial window size.
- Some sites behave differently with smaller or bigger viewports.
5.
verbose
:
- If
True
, prints extra logs.
- Handy for debugging.
6.
use\_persistent\_context
:
- If
True
, uses a
persistent
browser profile, storing cookies/local storage across runs.
- Typically also set
user\_data\_dir
to point to a folder.
7.
cookies
&
headers
:
- If you want to start with specific cookies or add universal HTTP headers, set them here.
- E.g.
cookies=[{"name": "session", "value": "abc123", "domain": "example.com"}]
.
8.
user\_agent
:
- Custom User-Agent string. If
None
, a default is used.
- You can also set
user\_agent\_mode="random"
for randomization (if you want to fight bot detection).
9.
text\_mode
&
light\_mode
:
-
text\_mode=True
disables images, possibly speeding up text-only crawls.
-
light\_mode=True
turns off certain background features for performance.
10.
extra\_args
:
- Additional flags for the underlying browser.
- E.g.
["--disable-extensions"]
.
Helper Methods
Both configuration classes provide a
clone()
method to create modified copies:
# Create a base browser config
base\_browser
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
text\_mode
=
True
)
# Create a visible browser config for debugging
debug\_browser
=
base\_browser
.
clone
(
headless
=
False
,
verbose
=
True
)
Minimal Example
:
from
crawl4ai
import
AsyncWebCrawler
,
BrowserConfig
browser\_conf
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
text\_mode
=
True
)
async
with
AsyncWebCrawler
(
config
=
browser\_conf
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
print
(
result
.
markdown
[:
300
])
2. CrawlerRunConfig Essentials
class
CrawlerRunConfig
:
def
\_\_init\_\_
(
word\_count\_threshold
=
200
,
extraction\_strategy
=
None
,
markdown\_generator
=
None
,
cache\_mode
=
None
,
js\_code
=
None
,
wait\_for
=
None
,
screenshot
=
False
,
pdf
=
False
,
enable\_rate\_limiting
=
False
,
rate\_limit\_config
=
None
,
memory\_threshold\_percent
=
70.0
,
check\_interval
=
1.0
,
max\_session\_permit
=
20
,
display\_mode
=
None
,
verbose
=
True
,
stream
=
False
,
# Enable streaming for arun\_many()
# ... other advanced parameters omitted
):
...
Key Fields to Note
1.
word\_count\_threshold
:
- The minimum word count before a block is considered.
- If your site has lots of short paragraphs or items, you can lower it.
2.
extraction\_strategy
:
- Where you plug in JSON-based extraction (CSS, LLM, etc.).
- If
None
, no structured extraction is done (only raw/cleaned HTML + markdown).
3.
markdown\_generator
:
- E.g.,
DefaultMarkdownGenerator(...)
, controlling how HTML→Markdown conversion is done.
- If
None
, a default approach is used.
4.
cache\_mode
:
- Controls caching behavior (
ENABLED
,
BYPASS
,
DISABLED
, etc.).
- If
None
, defaults to some level of caching or you can specify
CacheMode.ENABLED
.
5.
js\_code
:
- A string or list of JS strings to execute.
- Great for “Load More” buttons or user interactions.
6.
wait\_for
:
- A CSS or JS expression to wait for before extracting content.
- Common usage:
wait\_for="css:.main-loaded"
or
wait\_for="js:() => window.loaded === true"
.
7.
screenshot
&
pdf
:
- If
True
, captures a screenshot or PDF after the page is fully loaded.
- The results go to
result.screenshot
(base64) or
result.pdf
(bytes).
8.
verbose
:
- Logs additional runtime details.
- Overlaps with the browser’s verbosity if also set to
True
in
BrowserConfig
.
9.
enable\_rate\_limiting
:
- If
True
, enables rate limiting for batch processing.
- Requires
rate\_limit\_config
to be set.
10.
rate\_limit\_config
:
- A
RateLimitConfig
object controlling rate limiting behavior.
- See below for details.
11.
memory\_threshold\_percent
:
- The memory threshold (as a percentage) to monitor.
- If exceeded, the crawler will pause or slow down.
12.
check\_interval
:
- The interval (in seconds) to check system resources.
- Affects how often memory and CPU usage are monitored.
13.
max\_session\_permit
:
- The maximum number of concurrent crawl sessions.
- Helps prevent overwhelming the system.
14.
display\_mode
:
- The display mode for progress information (
DETAILED
,
BRIEF
, etc.).
- Affects how much information is printed during the crawl.
Helper Methods
The
clone()
method is particularly useful for creating variations of your crawler configuration:
# Create a base configuration
base\_config
=
CrawlerRunConfig
(
cache\_mode
=
CacheMode
.
ENABLED
,
word\_count\_threshold
=
200
,
wait\_until
=
"networkidle"
)
# Create variations for different use cases
stream\_config
=
base\_config
.
clone
(
stream
=
True
,
# Enable streaming mode
cache\_mode
=
CacheMode
.
BYPASS
)
debug\_config
=
base\_config
.
clone
(
page\_timeout
=
120000
,
# Longer timeout for debugging
verbose
=
True
)
The
clone()
method:
- Creates a new instance with all the same settings
- Updates only the specified parameters
- Leaves the original configuration unchanged
- Perfect for creating variations without repeating all parameters
Rate Limiting & Resource Management
For batch processing with
arun\_many()
, you can enable intelligent rate limiting:
from
crawl4ai
import
RateLimitConfig
config
=
CrawlerRunConfig
(
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
3.0
),
# Random delay range
max\_delay
=
60.0
,
# Max delay after rate limits
max\_retries
=
3
,
# Retries before giving up
rate\_limit\_codes
=
[
429
,
503
]
# Status codes to watch
),
memory\_threshold\_percent
=
70.0
,
# Memory threshold
check\_interval
=
1.0
,
# Resource check interval
max\_session\_permit
=
20
,
# Max concurrent crawls
display\_mode
=
"DETAILED"
# Progress display mode
)
This configuration:
- Implements intelligent rate limiting per domain
- Monitors system resources
- Provides detailed progress information
- Manages concurrent crawls efficiently
Minimal Example
:
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
crawl\_conf
=
CrawlerRunConfig
(
js\_code
=
"document.querySelector('button#loadMore')?.click()"
,
wait\_for
=
"css:.loaded-content"
,
screenshot
=
True
,
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
3.0
),
max\_delay
=
60.0
,
max\_retries
=
3
,
rate\_limit\_codes
=
[
429
,
503
]
),
stream
=
True
# Enable streaming
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
crawl\_conf
)
print
(
result
.
screenshot
[:
100
])
# Base64-encoded PNG snippet
3. Putting It All Together
In a typical scenario, you define
one
BrowserConfig
for your crawler session, then create
one or more
CrawlerRunConfig
depending on each call’s needs:
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
async
def
main
():
# 1) Browser config: headless, bigger viewport, no proxy
browser\_conf
=
BrowserConfig
(
headless
=
True
,
viewport\_width
=
1280
,
viewport\_height
=
720
)
# 2) Example extraction strategy
schema
=
{
"name"
:
"Articles"
,
"baseSelector"
:
"div.article"
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
extraction
=
JsonCssExtractionStrategy
(
schema
)
# 3) Crawler run config: skip cache, use extraction
run\_conf
=
CrawlerRunConfig
(
extraction\_strategy
=
extraction
,
cache\_mode
=
CacheMode
.
BYPASS
,
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
3.0
),
max\_delay
=
60.0
,
max\_retries
=
3
,
rate\_limit\_codes
=
[
429
,
503
]
)
)
async
with
AsyncWebCrawler
(
config
=
browser\_conf
)
as
crawler
:
# 4) Execute the crawl
result
=
await
crawler
.
arun
(
url
=
"https://example.com/news"
,
config
=
run\_conf
)
if
result
.
success
:
print
(
"Extracted content:"
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
4. Next Steps
For a
detailed list
of available parameters (including advanced ones), see:
BrowserConfig and CrawlerRunConfig Reference
You can explore topics like:
Custom Hooks & Auth
(Inject JavaScript or handle login forms).
Session Management
(Re-use pages, preserve state across multiple calls).
Magic Mode
or
Identity-based Crawling
(Fight bot detection by simulating user behavior).
Advanced Caching
(Fine-tune read/write cache modes).
5. Conclusion
BrowserConfig
and
CrawlerRunConfig
give you straightforward ways to define:
Which
browser to launch, how it should run, and any proxy or user agent needs.
How
each crawl should behave—caching, timeouts, JavaScript code, extraction strategies, etc.
Use them together for
clear, maintainable
code, and when you need more specialized behavior, check out the advanced parameters in the
reference docs
. Happy crawling!
Search
Type to start searching