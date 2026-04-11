Quick Start - Crawl4AI Documentation (v0.4.3bx)
Getting Started with Crawl4AI
Welcome to
Crawl4AI
, an open-source LLM-friendly Web Crawler & Scraper. In this tutorial, you’ll:
Run your
first crawl
using minimal configuration.
Generate
Markdown
output (and learn how it’s influenced by content filters).
Experiment with a simple
CSS-based extraction
strategy.
See a glimpse of
LLM-based extraction
(including open-source and closed-source model options).
Crawl a
dynamic
page that loads content via JavaScript.
1. Introduction
Crawl4AI provides:
An asynchronous crawler,
AsyncWebCrawler
.
Configurable browser and run settings via
BrowserConfig
and
CrawlerRunConfig
.
Automatic HTML-to-Markdown conversion via
DefaultMarkdownGenerator
(supports optional filters).
Multiple extraction strategies (LLM-based or “traditional” CSS/XPath-based).
By the end of this guide, you’ll have performed a basic crawl, generated Markdown, tried out two extraction strategies, and crawled a dynamic page that uses “Load More” buttons or JavaScript updates.
2. Your First Crawl
Here’s a minimal Python script that creates an
AsyncWebCrawler
, fetches a webpage, and prints the first 300 characters of its Markdown output:
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
async
def
main
():
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
# Print first 300 chars
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
What’s happening?
-
AsyncWebCrawler
launches a headless browser (Chromium by default).
- It fetches
https://example.com
.
- Crawl4AI automatically converts the HTML into Markdown.
You now have a simple, working crawl!
3. Basic Configuration (Light Introduction)
Crawl4AI’s crawler can be heavily customized using two main classes:
1.
BrowserConfig
: Controls browser behavior (headless or full UI, user agent, JavaScript toggles, etc.).
2.
CrawlerRunConfig
: Controls how each crawl runs (caching, extraction, timeouts, hooking, etc.).
Below is an example with minimal usage:
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
async
def
main
():
browser\_conf
=
BrowserConfig
(
headless
=
True
)
# or False to see the browser
run\_conf
=
CrawlerRunConfig
(
cache\_mode
=
CacheMode
.
BYPASS
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
url
=
"https://example.com"
,
config
=
run\_conf
)
print
(
result
.
markdown
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
IMPORTANT: By default cache mode is set to
CacheMode.ENABLED
. So to have fresh content, you need to set it to
CacheMode.BYPASS
We’ll explore more advanced config in later tutorials (like enabling proxies, PDF output, multi-tab sessions, etc.). For now, just note how you pass these objects to manage crawling.
4. Generating Markdown Output
By default, Crawl4AI automatically generates Markdown from each crawled page. However, the exact output depends on whether you specify a
markdown generator
or
content filter
.
result.markdown
:
The direct HTML-to-Markdown conversion.
result.markdown.fit\_markdown
:
The same content after applying any configured
content filter
(e.g.,
PruningContentFilter
).
Example: Using a Filter with
DefaultMarkdownGenerator
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
from
crawl4ai.content\_filter\_strategy
import
PruningContentFilter
from
crawl4ai.markdown\_generation\_strategy
import
DefaultMarkdownGenerator
md\_generator
=
DefaultMarkdownGenerator
(
content\_filter
=
PruningContentFilter
(
threshold
=
0.4
,
threshold\_type
=
"fixed"
)
)
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
markdown\_generator
=
md\_generator
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
"https://news.ycombinator.com"
,
config
=
config
)
print
(
"Raw Markdown length:"
,
len
(
result
.
markdown
.
raw\_markdown
))
print
(
"Fit Markdown length:"
,
len
(
result
.
markdown
.
fit\_markdown
))
Note
: If you do
not
specify a content filter or markdown generator, you’ll typically see only the raw Markdown.
PruningContentFilter
may adds around
50ms
in processing time. We’ll dive deeper into these strategies in a dedicated
Markdown Generation
tutorial.
5. Simple Data Extraction (CSS-based)
Crawl4AI can also extract structured data (JSON) using CSS or XPath selectors. Below is a minimal CSS-based example:
New!
Crawl4AI now provides a powerful utility to automatically generate extraction schemas using LLM. This is a one-time cost that gives you a reusable schema for fast, LLM-free extractions:
from
crawl4ai.extraction\_strategy
import
JsonCssExtractionStrategy
# Generate a schema (one-time cost)
html
=
"

Gaming Laptop
-------------

$999.99"
# Using OpenAI (requires API token)
schema
=
JsonCssExtractionStrategy
.
generate\_schema
(
html
,
llm\_provider
=
"openai/gpt-4o"
,
# Default provider
api\_token
=
"your-openai-token"
# Required for OpenAI
)
# Or using Ollama (open source, no token needed)
schema
=
JsonCssExtractionStrategy
.
generate\_schema
(
html
,
llm\_provider
=
"ollama/llama3.3"
,
# Open source alternative
api\_token
=
None
# Not needed for Ollama
)
# Use the schema for fast, repeated extractions
strategy
=
JsonCssExtractionStrategy
(
schema
)
For a complete guide on schema generation and advanced usage, see
No-LLM Extraction Strategies
.
Here's a basic extraction example:
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
# The JSON output is stored in 'extracted\_content'
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
Why is this helpful?
- Great for repetitive page structures (e.g., item listings, articles).
- No AI usage or costs.
- The crawler returns a JSON string you can parse or store.
Tips: You can pass raw HTML to the crawler instead of a URL. To do so, prefix the HTML with
raw://
.
6. Simple Data Extraction (LLM-based)
For more complex or irregular pages, a language model can parse text intelligently into a structure you define. Crawl4AI supports
open-source
or
closed-source
providers:
Open-Source Models
(e.g.,
ollama/llama3.3
,
no\_token
)
OpenAI Models
(e.g.,
openai/gpt-4
, requires
api\_token
)
Or any provider supported by the underlying library
Below is an example using
open-source
style (no token) and closed-source:
import
os
import
json
import
asyncio
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
OpenAIModelFee
(
BaseModel
):
model\_name
:
str
=
Field
(
...
,
description
=
"Name of the OpenAI model."
)
input\_fee
:
str
=
Field
(
...
,
description
=
"Fee for input token for the OpenAI model."
)
output\_fee
:
str
=
Field
(
...
,
description
=
"Fee for output token for the OpenAI model."
)
async
def
extract\_structured\_data\_using\_llm
(
provider
:
str
,
api\_token
:
str
=
None
,
extra\_headers
:
Dict
[
str
,
str
]
=
None
):
print
(
f
"
\n
--- Extracting Structured Data with
{
provider
}
---"
)
if
api\_token
is
None
and
provider
!=
"ollama"
:
print
(
f
"API token is required for
{
provider
}
. Skipping this example."
)
return
browser\_config
=
BrowserConfig
(
headless
=
True
)
extra\_args
=
{
"temperature"
:
0
,
"top\_p"
:
0.9
,
"max\_tokens"
:
2000
}
if
extra\_headers
:
extra\_args
[
"extra\_headers"
]
=
extra\_headers
crawler\_config
=
CrawlerRunConfig
(
cache\_mode
=
CacheMode
.
BYPASS
,
word\_count\_threshold
=
1
,
page\_timeout
=
80000
,
extraction\_strategy
=
LLMExtractionStrategy
(
provider
=
provider
,
api\_token
=
api\_token
,
schema
=
OpenAIModelFee
.
model\_json\_schema
(),
extraction\_type
=
"schema"
,
instruction
=
"""From the crawled content, extract all mentioned model names along with their fees for input and output tokens.
Do not miss any models in the entire content."""
,
extra\_args
=
extra\_args
,
),
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
"https://openai.com/api/pricing/"
,
config
=
crawler\_config
)
print
(
result
.
extracted\_content
)
if
\_\_name\_\_
==
"\_\_main\_\_"
:
# Use ollama with llama3.3
# asyncio.run(
# extract\_structured\_data\_using\_llm(
# provider="ollama/llama3.3", api\_token="no-token"
# )
# )
asyncio
.
run
(
extract\_structured\_data\_using\_llm
(
provider
=
"openai/gpt-4o"
,
api\_token
=
os
.
getenv
(
"OPENAI\_API\_KEY"
)
)
)
What’s happening?
- We define a Pydantic schema (
PricingInfo
) describing the fields we want.
- The LLM extraction strategy uses that schema and your instructions to transform raw text into structured JSON.
- Depending on the
provider
and
api\_token
, you can use local models or a remote API.
7. Multi-URL Concurrency (Preview)
If you need to crawl multiple URLs in
parallel
, you can use
arun\_many()
. By default, Crawl4AI employs a
MemoryAdaptiveDispatcher
, automatically adjusting concurrency based on system resources. Here’s a quick glimpse:
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
quick\_parallel\_example
():
urls
=
[
"https://example.com/page1"
,
"https://example.com/page2"
,
"https://example.com/page3"
]
run\_conf
=
CrawlerRunConfig
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
# Enable streaming mode
)
async
with
AsyncWebCrawler
()
as
crawler
:
# Stream results as they complete
async
for
result
in
await
crawler
.
arun\_many
(
urls
,
config
=
run\_conf
):
if
result
.
success
:
print
(
f
"[OK]
{
result
.
url
}
, length:
{
len
(
result
.
markdown\_v2
.
raw\_markdown
)
}
"
)
else
:
print
(
f
"[ERROR]
{
result
.
url
}
=>
{
result
.
error\_message
}
"
)
# Or get all results at once (default behavior)
run\_conf
=
run\_conf
.
clone
(
stream
=
False
)
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
run\_conf
)
for
res
in
results
:
if
res
.
success
:
print
(
f
"[OK]
{
res
.
url
}
, length:
{
len
(
res
.
markdown\_v2
.
raw\_markdown
)
}
"
)
else
:
print
(
f
"[ERROR]
{
res
.
url
}
=>
{
res
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
quick\_parallel\_example
())
The example above shows two ways to handle multiple URLs:
1.
Streaming mode
(
stream=True
): Process results as they become available using
async for
2.
Batch mode
(
stream=False
): Wait for all results to complete
For more advanced concurrency (e.g., a
semaphore-based
approach,
adaptive memory usage throttling
, or customized rate limiting), see
Advanced Multi-URL Crawling
.
8. Dynamic Content Example
Some sites require multiple “page clicks” or dynamic JavaScript updates. Below is an example showing how to
click
a “Next Page” button and wait for new commits to load on GitHub, using
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
extract\_structured\_data\_using\_css\_extractor
():
print
(
"
\n
--- Using JsonCssExtractionStrategy for Fast Structured Output ---"
)
schema
=
{
"name"
:
"KidoCode Courses"
,
"baseSelector"
:
"section.charge-methodology .w-tab-content > div"
,
"fields"
:
[
{
"name"
:
"section\_title"
,
"selector"
:
"h3.heading-50"
,
"type"
:
"text"
,
},
{
"name"
:
"section\_description"
,
"selector"
:
".charge-content"
,
"type"
:
"text"
,
},
{
"name"
:
"course\_name"
,
"selector"
:
".text-block-93"
,
"type"
:
"text"
,
},
{
"name"
:
"course\_description"
,
"selector"
:
".course-content-text"
,
"type"
:
"text"
,
},
{
"name"
:
"course\_icon"
,
"selector"
:
".image-92"
,
"type"
:
"attribute"
,
"attribute"
:
"src"
,
},
],
}
browser\_config
=
BrowserConfig
(
headless
=
True
,
java\_script\_enabled
=
True
)
js\_click\_tabs
=
"""
(async () => {
const tabs = document.querySelectorAll("section.charge-methodology .tabs-menu-3 > div");
for(let tab of tabs) {
tab.scrollIntoView();
tab.click();
await new Promise(r => setTimeout(r, 500));
}
})();
"""
crawler\_config
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
js\_code
=
[
js\_click\_tabs
],
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
"https://www.kidocode.com/degrees/technology"
,
config
=
crawler\_config
)
companies
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
f
"Successfully extracted
{
len
(
companies
)
}
companies"
)
print
(
json
.
dumps
(
companies
[
0
],
indent
=
2
))
async
def
main
():
await
extract\_structured\_data\_using\_css\_extractor
()
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
Key Points
:
BrowserConfig(headless=False)
: We want to watch it click “Next Page.”
CrawlerRunConfig(...)
: We specify the extraction strategy, pass
session\_id
to reuse the same page.
js\_code
and
wait\_for
are used for subsequent pages (
page > 0
) to click the “Next” button and wait for new commits to load.
js\_only=True
indicates we’re not re-navigating but continuing the existing session.
Finally, we call
kill\_session()
to clean up the page and browser session.
9. Next Steps
Congratulations! You have:
Performed a basic crawl and printed Markdown.
Used
content filters
with a markdown generator.
Extracted JSON via
CSS
or
LLM
strategies.
Handled
dynamic
pages with JavaScript triggers.
If you’re ready for more, check out:
Installation
: A deeper dive into advanced installs, Docker usage (experimental), or optional dependencies.
Hooks & Auth
: Learn how to run custom JavaScript or handle logins with cookies, local storage, etc.
Deployment
: Explore ephemeral testing in Docker or plan for the upcoming stable Docker release.
Browser Management
: Delve into user simulation, stealth modes, and concurrency best practices.
Crawl4AI is a powerful, flexible tool. Enjoy building out your scrapers, data pipelines, or AI-driven extraction flows. Happy crawling!
Search
Type to start searching