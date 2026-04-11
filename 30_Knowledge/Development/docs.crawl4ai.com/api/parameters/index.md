Browser & Crawler Config - Crawl4AI Documentation (v0.4.3bx)
1.
BrowserConfig
– Controlling the Browser
BrowserConfig
focuses on
how
the browser is launched and behaves. This includes headless mode, proxies, user agents, and other environment tweaks.
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
viewport\_width
=
1280
,
viewport\_height
=
720
,
proxy
=
"http://user:pass@proxy:8080"
,
user\_agent
=
"Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36"
,
)
1.1 Parameter Highlights
Parameter
Type / Default
What It Does
browser\_type
"chromium"
,
"firefox"
,
"webkit"
(default:
"chromium"
)
Which browser engine to use.
"chromium"
is typical for many sites,
"firefox"
or
"webkit"
for specialized tests.
headless
bool
(default:
True
)
Headless means no visible UI.
False
is handy for debugging.
viewport\_width
int
(default:
1080
)
Initial page width (in px). Useful for testing responsive layouts.
viewport\_height
int
(default:
600
)
Initial page height (in px).
proxy
str
(default:
None
)
Single-proxy URL if you want all traffic to go through it, e.g.
"http://user:pass@proxy:8080"
.
proxy\_config
dict
(default:
None
)
For advanced or multi-proxy needs, specify details like
{"server": "...", "username": "...", ...}
.
use\_persistent\_context
bool
(default:
False
)
If
True
, uses a
persistent
browser context (keep cookies, sessions across runs). Also sets
use\_managed\_browser=True
.
user\_data\_dir
str or None
(default:
None
)
Directory to store user data (profiles, cookies). Must be set if you want permanent sessions.
ignore\_https\_errors
bool
(default:
True
)
If
True
, continues despite invalid certificates (common in dev/staging).
java\_script\_enabled
bool
(default:
True
)
Disable if you want no JS overhead, or if only static content is needed.
cookies
list
(default:
[]
)
Pre-set cookies, each a dict like
{"name": "session", "value": "...", "url": "..."}
.
headers
dict
(default:
{}
)
Extra HTTP headers for every request, e.g.
{"Accept-Language": "en-US"}
.
user\_agent
str
(default: Chrome-based UA)
Your custom or random user agent.
user\_agent\_mode="random"
can shuffle it.
light\_mode
bool
(default:
False
)
Disables some background features for performance gains.
text\_mode
bool
(default:
False
)
If
True
, tries to disable images/other heavy content for speed.
use\_managed\_browser
bool
(default:
False
)
For advanced “managed” interactions (debugging, CDP usage). Typically set automatically if persistent context is on.
extra\_args
list
(default:
[]
)
Additional flags for the underlying browser process, e.g.
["--disable-extensions"]
.
Tips
:
- Set
headless=False
to visually
debug
how pages load or how interactions proceed.
- If you need
authentication
storage or repeated sessions, consider
use\_persistent\_context=True
and specify
user\_data\_dir
.
- For large pages, you might need a bigger
viewport\_width
and
viewport\_height
to handle dynamic content.
2.
CrawlerRunConfig
– Controlling Each Crawl
While
BrowserConfig
sets up the
environment
,
CrawlerRunConfig
details
how
each
crawl operation
should behave: caching, content filtering, link or domain blocking, timeouts, JavaScript code, etc.
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
run\_cfg
=
CrawlerRunConfig
(
wait\_for
=
"css:.main-content"
,
word\_count\_threshold
=
15
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
stream
=
True
,
# Enable streaming for arun\_many()
)
2.1 Parameter Highlights
We group them by category.
A)
Content Processing
Parameter
Type / Default
What It Does
word\_count\_threshold
int
(default: ~200)
Skips text blocks below X words. Helps ignore trivial sections.
extraction\_strategy
ExtractionStrategy
(default: None)
If set, extracts structured data (CSS-based, LLM-based, etc.).
markdown\_generator
MarkdownGenerationStrategy
(None)
If you want specialized markdown output (citations, filtering, chunking, etc.).
content\_filter
RelevantContentFilter
(None)
Filters out irrelevant text blocks. E.g.,
PruningContentFilter
or
BM25ContentFilter
.
css\_selector
str
(None)
Retains only the part of the page matching this selector.
excluded\_tags
list
(None)
Removes entire tags (e.g.
["script", "style"]
).
excluded\_selector
str
(None)
Like
css\_selector
but to exclude. E.g.
"#ads, .tracker"
.
only\_text
bool
(False)
If
True
, tries to extract text-only content.
prettiify
bool
(False)
If
True
, beautifies final HTML (slower, purely cosmetic).
keep\_data\_attributes
bool
(False)
If
True
, preserve
data-\*
attributes in cleaned HTML.
remove\_forms
bool
(False)
If
True
, remove all
elements.
B)
Caching & Session
Parameter
Type / Default
What It Does
cache\_mode
CacheMode or None
Controls how caching is handled (
ENABLED
,
BYPASS
,
DISABLED
, etc.). If
None
, typically defaults to
ENABLED
.
session\_id
str or None
Assign a unique ID to reuse a single browser session across multiple
arun()
calls.
bypass\_cache
bool
(False)
If
True
, acts like
CacheMode.BYPASS
.
disable\_cache
bool
(False)
If
True
, acts like
CacheMode.DISABLED
.
no\_cache\_read
bool
(False)
If
True
, acts like
CacheMode.WRITE\_ONLY
(writes cache but never reads).
no\_cache\_write
bool
(False)
If
True
, acts like
CacheMode.READ\_ONLY
(reads cache but never writes).
Use these for controlling whether you read or write from a local content cache. Handy for large batch crawls or repeated site visits.
C)
Page Navigation & Timing
Parameter
Type / Default
What It Does
wait\_until
str
(domcontentloaded)
Condition for navigation to “complete”. Often
"networkidle"
or
"domcontentloaded"
.
page\_timeout
int
(60000 ms)
Timeout for page navigation or JS steps. Increase for slow sites.
wait\_for
str or None
Wait for a CSS (
"css:selector"
) or JS (
"js:() => bool"
) condition before content extraction.
wait\_for\_images
bool
(False)
Wait for images to load before finishing. Slows down if you only want text.
delay\_before\_return\_html
float
(0.1)
Additional pause (seconds) before final HTML is captured. Good for last-second updates.
check\_robots\_txt
bool
(False)
Whether to check and respect robots.txt rules before crawling. If True, caches robots.txt for efficiency.
mean\_delay
and
max\_range
float
(0.1, 0.3)
If you call
arun\_many()
, these define random delay intervals between crawls, helping avoid detection or rate limits.
semaphore\_count
int
(5)
Max concurrency for
arun\_many()
. Increase if you have resources for parallel crawls.
D)
Page Interaction
Parameter
Type / Default
What It Does
js\_code
str or list[str]
(None)
JavaScript to run after load. E.g.
"document.querySelector('button')?.click();"
.
js\_only
bool
(False)
If
True
, indicates we’re reusing an existing session and only applying JS. No full reload.
ignore\_body\_visibility
bool
(True)
Skip checking if
is visible. Usually best to keep
True
.
scan\_full\_page
bool
(False)
If
True
, auto-scroll the page to load dynamic content (infinite scroll).
scroll\_delay
float
(0.2)
Delay between scroll steps if
scan\_full\_page=True
.
process\_iframes
bool
(False)
Inlines iframe content for single-page extraction.
remove\_overlay\_elements
bool
(False)
Removes potential modals/popups blocking the main content.
simulate\_user
bool
(False)
Simulate user interactions (mouse movements) to avoid bot detection.
override\_navigator
bool
(False)
Override
navigator
properties in JS for stealth.
magic
bool
(False)
Automatic handling of popups/consent banners. Experimental.
adjust\_viewport\_to\_content
bool
(False)
Resizes viewport to match page content height.
If your page is a single-page app with repeated JS updates, set
js\_only=True
in subsequent calls, plus a
session\_id
for reusing the same tab.
E)
Media Handling
Parameter
Type / Default
What It Does
screenshot
bool
(False)
Capture a screenshot (base64) in
result.screenshot
.
screenshot\_wait\_for
float or None
Extra wait time before the screenshot.
screenshot\_height\_threshold
int
(~20000)
If the page is taller than this, alternate screenshot strategies are used.
pdf
bool
(False)
If
True
, returns a PDF in
result.pdf
.
image\_description\_min\_word\_threshold
int
(~50)
Minimum words for an image’s alt text or description to be considered valid.
image\_score\_threshold
int
(~3)
Filter out low-scoring images. The crawler scores images by relevance (size, context, etc.).
exclude\_external\_images
bool
(False)
Exclude images from other domains.
F)
Link/Domain Handling
Parameter
Type / Default
What It Does
exclude\_social\_media\_domains
list
(e.g. Facebook/Twitter)
A default list can be extended. Any link to these domains is removed from final output.
exclude\_external\_links
bool
(False)
Removes all links pointing outside the current domain.
exclude\_social\_media\_links
bool
(False)
Strips links specifically to social sites (like Facebook or Twitter).
exclude\_domains
list
([])
Provide a custom list of domains to exclude (like
["ads.com", "trackers.io"]
).
Use these for link-level content filtering (often to keep crawls “internal” or to remove spammy domains).
G)
Rate Limiting & Resource Management
Parameter
Type / Default
What It Does
enable\_rate\_limiting
bool
(default:
False
)
Enable intelligent rate limiting for multiple URLs
rate\_limit\_config
RateLimitConfig
(default:
None
)
Configuration for rate limiting behavior
The
RateLimitConfig
class has these fields:
Field
Type / Default
What It Does
base\_delay
Tuple[float, float]
(1.0, 3.0)
Random delay range between requests to the same domain
max\_delay
float
(60.0)
Maximum delay after rate limit detection
max\_retries
int
(3)
Number of retries before giving up on rate-limited requests
rate\_limit\_codes
List[int]
([429, 503])
HTTP status codes that trigger rate limiting behavior
Parameter
Type / Default
What It Does
memory\_threshold\_percent
float
(70.0)
Maximum memory usage before pausing new crawls
check\_interval
float
(1.0)
How often to check system resources (in seconds)
max\_session\_permit
int
(20)
Maximum number of concurrent crawl sessions
display\_mode
str
(
None
, "DETAILED", "AGGREGATED")
How to display progress information
H)
Debug & Logging
Parameter
Type / Default
What It Does
verbose
bool
(True)
Prints logs detailing each step of crawling, interactions, or errors.
log\_console
bool
(False)
Logs the page’s JavaScript console output if you want deeper JS debugging.
2.2 Helper Methods
Both
BrowserConfig
and
CrawlerRunConfig
provide a
clone()
method to create modified copies:
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
)
# Create variations using clone()
stream\_config
=
base\_config
.
clone
(
stream
=
True
)
no\_cache\_config
=
base\_config
.
clone
(
cache\_mode
=
CacheMode
.
BYPASS
,
stream
=
True
)
The
clone()
method is particularly useful when you need slightly different configurations for different use cases, without modifying the original config.
2.3 Example Usage
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
,
RateLimitConfig
async
def
main
():
# Configure the browser
browser\_cfg
=
BrowserConfig
(
headless
=
False
,
viewport\_width
=
1280
,
viewport\_height
=
720
,
proxy
=
"http://user:pass@myproxy:8080"
,
text\_mode
=
True
)
# Configure the run
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
session\_id
=
"my\_session"
,
css\_selector
=
"main.article"
,
excluded\_tags
=
[
"script"
,
"style"
],
exclude\_external\_links
=
True
,
wait\_for
=
"css:.article-loaded"
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
"DETAILED"
,
stream
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
url
=
"https://example.com/news"
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
"Final cleaned\_html length:"
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
"Screenshot captured (base64, length):"
,
len
(
result
.
screenshot
))
else
:
print
(
"Crawl failed:"
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
## 2.4 Compliance & Ethics
|
\*\*
Parameter
\*\*
|
\*\*
Type
/
Default
\*\*
|
\*\*
What
It
Does
\*\*
|
|-----------------------|-------------------------|----------------------------------------------------------------------------------------------------------------------|
|
\*\*
`
check\_robots\_txt
`
\*\*|
`
bool
`
(
False
)
|
When
True
,
checks
and
respects
robots
.
txt
rules
before
crawling
.
Uses
efficient
caching
with
SQLite
backend
.
|
|
\*\*
`
user\_agent
`
\*\*
|
`
str
`
(
None
)
|
User
agent
string
to
identify
your
crawler
.
Used
for
robots
.
txt
checking
when
enabled
.
|
```
python
run\_config
=
CrawlerRunConfig
(
check\_robots\_txt
=
True
,
# Enable robots.txt compliance
user\_agent
=
"MyBot/1.0"
# Identify your crawler
)
3. Putting It All Together
Use
BrowserConfig
for
global
browser settings: engine, headless, proxy, user agent.
Use
CrawlerRunConfig
for each crawl’s
context
: how to filter content, handle caching, wait for dynamic elements, or run JS.
Pass
both configs to
AsyncWebCrawler
(the
BrowserConfig
) and then to
arun()
(the
CrawlerRunConfig
).
# Create a modified copy with the clone() method
stream\_cfg
=
run\_cfg
.
clone
(
stream
=
True
,
cache\_mode
=
CacheMode
.
BYPASS
)
Search
Type to start searching