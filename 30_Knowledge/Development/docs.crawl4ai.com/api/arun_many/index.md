arun\_many() - Crawl4AI Documentation (v0.4.3bx)
arun\_many(...)
Reference
Note
: This function is very similar to
arun()
but focused on
concurrent
or
batch
crawling. If you’re unfamiliar with
arun()
usage, please read that doc first, then review this for differences.
Function Signature
async
def
arun\_many
(
urls
:
Union
[
List
[
str
],
List
[
Any
]],
config
:
Optional
[
CrawlerRunConfig
]
=
None
,
dispatcher
:
Optional
[
BaseDispatcher
]
=
None
,
...
)
->
Union
[
List
[
CrawlResult
],
AsyncGenerator
[
CrawlResult
,
None
]]:
"""
Crawl multiple URLs concurrently or in batches.
:param urls: A list of URLs (or tasks) to crawl.
:param config: (Optional) A default `CrawlerRunConfig` applying to each crawl.
:param dispatcher: (Optional) A concurrency controller (e.g. MemoryAdaptiveDispatcher).
...
:return: Either a list of `CrawlResult` objects, or an async generator if streaming is enabled.
"""
Differences from
arun()
1.
Multiple URLs
:
Instead of crawling a single URL, you pass a list of them (strings or tasks).
The function returns either a
list
of
CrawlResult
or an
async generator
if streaming is enabled.
2.
Concurrency & Dispatchers
:
dispatcher
param allows advanced concurrency control.
If omitted, a default dispatcher (like
MemoryAdaptiveDispatcher
) is used internally.
Dispatchers handle concurrency, rate limiting, and memory-based adaptive throttling (see
Multi-URL Crawling
).
3.
Streaming Support
:
Enable streaming by setting
stream=True
in your
CrawlerRunConfig
.
When streaming, use
async for
to process results as they become available.
Ideal for processing large numbers of URLs without waiting for all to complete.
4.
Parallel
Execution\*\*:
arun\_many()
can run multiple requests concurrently under the hood.
Each
CrawlResult
might also include a
dispatch\_result
with concurrency details (like memory usage, start/end times).
Basic Example (Batch Mode)
# Minimal usage: The default dispatcher will be used
results
=
await
crawler
.
arun\_many
(
urls
=
[
"https://site1.com"
,
"https://site2.com"
],
config
=
CrawlerRunConfig
(
stream
=
False
)
# Default behavior
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
res
.
url
,
"crawled OK!"
)
else
:
print
(
"Failed:"
,
res
.
url
,
"-"
,
res
.
error\_message
)
Streaming Example
config
=
CrawlerRunConfig
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
# Process results as they complete
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
=
[
"https://site1.com"
,
"https://site2.com"
,
"https://site3.com"
],
config
=
config
):
if
result
.
success
:
print
(
f
"Just completed:
{
result
.
url
}
"
)
# Process each result immediately
process\_result
(
result
)
With a Custom Dispatcher
dispatcher
=
MemoryAdaptiveDispatcher
(
memory\_threshold\_percent
=
70.0
,
max\_session\_permit
=
10
)
results
=
await
crawler
.
arun\_many
(
urls
=
[
"https://site1.com"
,
"https://site2.com"
,
"https://site3.com"
],
config
=
my\_run\_config
,
dispatcher
=
dispatcher
)
Key Points
:
- Each URL is processed by the same or separate sessions, depending on the dispatcher’s strategy.
-
dispatch\_result
in each
CrawlResult
(if using concurrency) can hold memory and timing info. 
- If you need to handle authentication or session IDs, pass them in each individual task or within your run config.
Return Value
Either a
list
of
CrawlResult
objects, or an
async generator
if streaming is enabled. You can iterate to check
result.success
or read each item’s
extracted\_content
,
markdown
, or
dispatch\_result
.
Dispatcher Reference
MemoryAdaptiveDispatcher
: Dynamically manages concurrency based on system memory usage.
SemaphoreDispatcher
: Fixed concurrency limit, simpler but less adaptive.
For advanced usage or custom settings, see
Multi-URL Crawling with Dispatchers
.
Common Pitfalls
1.
Large Lists
: If you pass thousands of URLs, be mindful of memory or rate-limits. A dispatcher can help.
2.
Session Reuse
: If you need specialized logins or persistent contexts, ensure your dispatcher or tasks handle sessions accordingly.
3.
Error Handling
: Each
CrawlResult
might fail for different reasons—always check
result.success
or the
error\_message
before proceeding.
Conclusion
Use
arun\_many()
when you want to
crawl multiple URLs
simultaneously or in controlled parallel tasks. If you need advanced concurrency features (like memory-based adaptive throttling or complex rate-limiting), provide a
dispatcher
. Each result is a standard
CrawlResult
, possibly augmented with concurrency stats (
dispatch\_result
) for deeper inspection. For more details on concurrency logic and dispatchers, see the
Advanced Multi-URL Crawling
docs.
Search
Type to start searching