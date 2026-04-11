arun() - Crawl4AI Documentation (v0.4.3bx)
arun()
Parameter Guide (New Approach)
In Crawl4AI’s
latest
configuration model, nearly all parameters that once went directly to
arun()
are now part of
CrawlerRunConfig
. When calling
arun()
, you provide:
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
my\_run\_config
)
Below is an organized look at the parameters that can go inside
CrawlerRunConfig
, divided by their functional areas. For
Browser
settings (e.g.,
headless
,
browser\_type
), see
BrowserConfig
.
1. Core Usage
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
run\_config
=
CrawlerRunConfig
(
verbose
=
True
,
# Detailed logging
cache\_mode
=
CacheMode
.
ENABLED
,
# Use normal read/write cache
check\_robots\_txt
=
True
,
# Respect robots.txt rules
# ... other parameters
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
run\_config
)
# Check if blocked by robots.txt
if
not
result
.
success
and
result
.
status\_code
==
403
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
Key Fields
:
-
verbose=True
logs each crawl step. 
-
cache\_mode
decides how to read/write the local crawl cache.
2. Cache Control
cache\_mode
(default:
CacheMode.ENABLED
)
Use a built-in enum from
CacheMode
:
ENABLED
: Normal caching—reads if available, writes if missing.
DISABLED
: No caching—always refetch pages.
READ\_ONLY
: Reads from cache only; no new writes.
WRITE\_ONLY
: Writes to cache but doesn’t read existing data.
BYPASS
: Skips reading cache for this crawl (though it might still write if set up that way).
run\_config
=
CrawlerRunConfig
(
cache\_mode
=
CacheMode
.
BYPASS
)
Additional flags
:
bypass\_cache=True
acts like
CacheMode.BYPASS
.
disable\_cache=True
acts like
CacheMode.DISABLED
.
no\_cache\_read=True
acts like
CacheMode.WRITE\_ONLY
.
no\_cache\_write=True
acts like
CacheMode.READ\_ONLY
.
3. Content Processing & Selection
3.1 Text Processing
run\_config
=
CrawlerRunConfig
(
word\_count\_threshold
=
10
,
# Ignore text blocks <10 words
only\_text
=
False
,
# If True, tries to remove non-text elements
keep\_data\_attributes
=
False
# Keep or discard data-\* attributes
)
3.2 Content Selection
run\_config
=
CrawlerRunConfig
(
css\_selector
=
".main-content"
,
# Focus on .main-content region only
excluded\_tags
=
[
"form"
,
"nav"
],
# Remove entire tag blocks
remove\_forms
=
True
,
# Specifically strip  elements
remove\_overlay\_elements
=
True
,
# Attempt to remove modals/popups
)
3.3 Link Handling
run\_config
=
CrawlerRunConfig
(
exclude\_external\_links
=
True
,
# Remove external links from final content
exclude\_social\_media\_links
=
True
,
# Remove links to known social sites
exclude\_domains
=
[
"ads.example.com"
],
# Exclude links to these domains
exclude\_social\_media\_domains
=
[
"facebook.com"
,
"twitter.com"
],
# Extend the default list
)
3.4 Media Filtering
run\_config
=
CrawlerRunConfig
(
exclude\_external\_images
=
True
# Strip images from other domains
)
4. Page Navigation & Timing
4.1 Basic Browser Flow
run\_config
=
CrawlerRunConfig
(
wait\_for
=
"css:.dynamic-content"
,
# Wait for .dynamic-content
delay\_before\_return\_html
=
2.0
,
# Wait 2s before capturing final HTML
page\_timeout
=
60000
,
# Navigation & script timeout (ms)
)
Key Fields
:
wait\_for
:
"css:selector"
or
"js:() => boolean"
e.g.
js:() => document.querySelectorAll('.item').length > 10
.
mean\_delay
&
max\_range
: define random delays for
arun\_many()
calls.
semaphore\_count
: concurrency limit when crawling multiple URLs.
4.2 JavaScript Execution
run\_config
=
CrawlerRunConfig
(
js\_code
=
[
"window.scrollTo(0, document.body.scrollHeight);"
,
"document.querySelector('.load-more')?.click();"
],
js\_only
=
False
)
js\_code
can be a single string or a list of strings.
js\_only=True
means “I’m continuing in the same session with new JS steps, no new full navigation.”
4.3 Anti-Bot
run\_config
=
CrawlerRunConfig
(
magic
=
True
,
simulate\_user
=
True
,
override\_navigator
=
True
)
-
magic=True
tries multiple stealth features. 
-
simulate\_user=True
mimics mouse movements or random delays. 
-
override\_navigator=True
fakes some navigator properties (like user agent checks).
5. Session Management
session\_id
:
run\_config
=
CrawlerRunConfig
(
session\_id
=
"my\_session123"
)
If re-used in subsequent
arun()
calls, the same tab/page context is continued (helpful for multi-step tasks or stateful browsing).
6. Screenshot, PDF & Media Options
run\_config
=
CrawlerRunConfig
(
screenshot
=
True
,
# Grab a screenshot as base64
screenshot\_wait\_for
=
1.0
,
# Wait 1s before capturing
pdf
=
True
,
# Also produce a PDF
image\_description\_min\_word\_threshold
=
5
,
# If analyzing alt text
image\_score\_threshold
=
3
,
# Filter out low-score images
)
Where they appear
:
-
result.screenshot
→ Base64 screenshot string.
-
result.pdf
→ Byte array with PDF data.
7. Extraction Strategy
For advanced data extraction
(CSS/LLM-based), set
extraction\_strategy
:
run\_config
=
CrawlerRunConfig
(
extraction\_strategy
=
my\_css\_or\_llm\_strategy
)
The extracted data will appear in
result.extracted\_content
.
8. Comprehensive Example
Below is a snippet combining many parameters:
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
from
crawl4ai.extraction\_strategy
import
JsonCssExtractionStrategy
async
def
main
():
# Example schema
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
run\_config
=
CrawlerRunConfig
(
# Core
verbose
=
True
,
cache\_mode
=
CacheMode
.
ENABLED
,
check\_robots\_txt
=
True
,
# Respect robots.txt rules
# Content
word\_count\_threshold
=
10
,
css\_selector
=
"main.content"
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
# Page & JS
js\_code
=
"document.querySelector('.show-more')?.click();"
,
wait\_for
=
"css:.loaded-block"
,
page\_timeout
=
30000
,
# Extraction
extraction\_strategy
=
JsonCssExtractionStrategy
(
schema
),
# Session
session\_id
=
"persistent\_session"
,
# Media
screenshot
=
True
,
pdf
=
True
,
# Anti-bot
simulate\_user
=
True
,
magic
=
True
,
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
"https://example.com/posts"
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
print
(
"HTML length:"
,
len
(
result
.
cleaned\_html
))
print
(
"Extraction JSON:"
,
result
.
extracted\_content
)
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
What we covered
:
1.
Crawling
the main content region, ignoring external links. 
2. Running
JavaScript
to click “.show-more”. 
3.
Waiting
for “.loaded-block” to appear. 
4. Generating a
screenshot
&
PDF
of the final page. 
5. Extracting repeated “article.post” elements with a
CSS-based
extraction strategy.
9. Best Practices
1.
Use
BrowserConfig
for global browser
settings (headless, user agent). 
2.
Use
CrawlerRunConfig
to handle the
specific
crawl needs: content filtering, caching, JS, screenshot, extraction, etc. 
3. Keep your
parameters consistent
in run configs—especially if you’re part of a large codebase with multiple crawls. 
4.
Limit
large concurrency (
semaphore\_count
) if the site or your system can’t handle it. 
5. For dynamic pages, set
js\_code
or
scan\_full\_page
so you load all content.
10. Conclusion
All parameters that used to be direct arguments to
arun()
now belong in
CrawlerRunConfig
. This approach:
Makes code
clearer
and
more maintainable
.
Minimizes confusion about which arguments affect global vs. per-crawl behavior.
Allows you to create
reusable
config objects for different pages or tasks.
For a
full
reference, check out the
CrawlerRunConfig Docs
.
Happy crawling with your
structured, flexible
config approach!
Search
Type to start searching