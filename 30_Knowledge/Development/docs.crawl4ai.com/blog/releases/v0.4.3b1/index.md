Crawl4AI 0.4.3: Major Performance Boost & LLM Integration - Crawl4AI Documentation (v0.4.3bx)
Crawl4AI 0.4.3: Major Performance Boost & LLM Integration
We're excited to announce Crawl4AI 0.4.3, focusing on three key areas: Speed & Efficiency, LLM Integration, and Core Platform Improvements. This release significantly improves crawling performance while adding powerful new LLM-powered features.
⚡ Speed & Efficiency Improvements
1. Memory-Adaptive Dispatcher System
The new dispatcher system provides intelligent resource management and real-time monitoring:
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
,
DisplayMode
from
crawl4ai.async\_dispatcher
import
MemoryAdaptiveDispatcher
,
CrawlerMonitor
async
def
main
():
urls
=
[
"https://example1.com"
,
"https://example2.com"
]
\*
50
# Configure memory-aware dispatch
dispatcher
=
MemoryAdaptiveDispatcher
(
memory\_threshold\_percent
=
80.0
,
# Auto-throttle at 80% memory
check\_interval
=
0.5
,
# Check every 0.5 seconds
max\_session\_permit
=
20
,
# Max concurrent sessions
monitor
=
CrawlerMonitor
(
# Real-time monitoring
display\_mode
=
DisplayMode
.
DETAILED
)
)
async
with
AsyncWebCrawler
()
as
crawler
:
results
=
await
dispatcher
.
run\_urls
(
urls
=
urls
,
crawler
=
crawler
,
config
=
CrawlerRunConfig
()
)
2. Streaming Support
Process crawled URLs in real-time instead of waiting for all results:
config
=
CrawlerRunConfig
(
stream
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
config
):
print
(
f
"Got result for
{
result
.
url
}
"
)
# Process each result immediately
3. LXML-Based Scraping
New LXML scraping strategy offering up to 20x faster parsing:
config
=
CrawlerRunConfig
(
scraping\_strategy
=
LXMLWebScrapingStrategy
(),
cache\_mode
=
CacheMode
.
ENABLED
)
🤖 LLM Integration
1. LLM-Powered Markdown Generation
Smart content filtering and organization using LLMs:
config
=
CrawlerRunConfig
(
markdown\_generator
=
DefaultMarkdownGenerator
(
content\_filter
=
LLMContentFilter
(
provider
=
"openai/gpt-4o"
,
instruction
=
"Extract technical documentation and code examples"
)
)
)
2. Automatic Schema Generation
Generate extraction schemas instantly using LLMs instead of manual CSS/XPath writing:
schema
=
JsonCssExtractionStrategy
.
generate\_schema
(
html\_content
,
schema\_type
=
"CSS"
,
query
=
"Extract product name, price, and description"
)
🔧 Core Improvements
1. Proxy Support & Rotation
Integrated proxy support with automatic rotation and verification:
config
=
CrawlerRunConfig
(
proxy\_config
=
{
"server"
:
"http://proxy:8080"
,
"username"
:
"user"
,
"password"
:
"pass"
}
)
2. Robots.txt Compliance
Built-in robots.txt support with SQLite caching:
config
=
CrawlerRunConfig
(
check\_robots\_txt
=
True
)
result
=
await
crawler
.
arun
(
url
,
config
=
config
)
if
result
.
status\_code
==
403
:
print
(
"Access blocked by robots.txt"
)
3. URL Redirection Tracking
Track final URLs after redirects:
result
=
await
crawler
.
arun
(
url
)
print
(
f
"Initial URL:
{
url
}
"
)
print
(
f
"Final URL:
{
result
.
redirected\_url
}
"
)
Performance Impact
Memory usage reduced by up to 40% with adaptive dispatcher
Parsing speed increased up to 20x with LXML strategy
Streaming reduces memory footprint for large crawls by ~60%
Getting Started
pip
install
-U
crawl4ai
For complete examples, check our
demo repository
.
Stay Connected
Star us on
GitHub
Follow
@unclecode
Join our
Discord
Happy crawling! 🕷️
Search
Type to start searching