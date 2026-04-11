Cache Modes - Crawl4AI Documentation (v0.4.3bx)
Crawl4AI Cache System and Migration Guide
Overview
Starting from version 0.5.0, Crawl4AI introduces a new caching system that replaces the old boolean flags with a more intuitive
CacheMode
enum. This change simplifies cache control and makes the behavior more predictable.
Old vs New Approach
Old Way (Deprecated)
The old system used multiple boolean flags:
-
bypass\_cache
: Skip cache entirely
-
disable\_cache
: Disable all caching
-
no\_cache\_read
: Don't read from cache
-
no\_cache\_write
: Don't write to cache
New Way (Recommended)
The new system uses a single
CacheMode
enum:
-
CacheMode.ENABLED
: Normal caching (read/write)
-
CacheMode.DISABLED
: No caching at all
-
CacheMode.READ\_ONLY
: Only read from cache
-
CacheMode.WRITE\_ONLY
: Only write to cache
-
CacheMode.BYPASS
: Skip cache for this operation
Migration Example
Old Code (Deprecated)
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
async
def
use\_proxy
():
async
with
AsyncWebCrawler
(
verbose
=
True
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
"https://www.nbcnews.com/business"
,
bypass\_cache
=
True
# Old way
)
print
(
len
(
result
.
markdown
))
async
def
main
():
await
use\_proxy
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
New Code (Recommended)
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
,
CacheMode
from
crawl4ai.async\_configs
import
CrawlerRunConfig
async
def
use\_proxy
():
# Use CacheMode in CrawlerRunConfig
config
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
verbose
=
True
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
"https://www.nbcnews.com/business"
,
config
=
config
# Pass the configuration object
)
print
(
len
(
result
.
markdown
))
async
def
main
():
await
use\_proxy
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
Common Migration Patterns
Old Flag
New Mode
bypass\_cache=True
cache\_mode=CacheMode.BYPASS
disable\_cache=True
cache\_mode=CacheMode.DISABLED
no\_cache\_read=True
cache\_mode=CacheMode.WRITE\_ONLY
no\_cache\_write=True
cache\_mode=CacheMode.READ\_ONLY
Search
Type to start searching