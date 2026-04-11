File Downloading - Crawl4AI Documentation (v0.4.3bx)
Download Handling in Crawl4AI
This guide explains how to use Crawl4AI to handle file downloads during crawling. You'll learn how to trigger downloads, specify download locations, and access downloaded files.
Enabling Downloads
To enable downloads, set the
accept\_downloads
parameter in the
BrowserConfig
object and pass it to the crawler.
from
crawl4ai.async\_configs
import
BrowserConfig
,
AsyncWebCrawler
async
def
main
():
config
=
BrowserConfig
(
accept\_downloads
=
True
)
# Enable downloads globally
async
with
AsyncWebCrawler
(
config
=
config
)
as
crawler
:
# ... your crawling logic ...
asyncio
.
run
(
main
())
Specifying Download Location
Specify the download directory using the
downloads\_path
attribute in the
BrowserConfig
object. If not provided, Crawl4AI defaults to creating a "downloads" directory inside the
.crawl4ai
folder in your home directory.
from
crawl4ai.async\_configs
import
BrowserConfig
import
os
downloads\_path
=
os
.
path
.
join
(
os
.
getcwd
(),
"my\_downloads"
)
# Custom download path
os
.
makedirs
(
downloads\_path
,
exist\_ok
=
True
)
config
=
BrowserConfig
(
accept\_downloads
=
True
,
downloads\_path
=
downloads\_path
)
async
def
main
():
async
with
AsyncWebCrawler
(
config
=
config
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
)
# ...
Triggering Downloads
Downloads are typically triggered by user interactions on a web page, such as clicking a download button. Use
js\_code
in
CrawlerRunConfig
to simulate these actions and
wait\_for
to allow sufficient time for downloads to start.
from
crawl4ai.async\_configs
import
CrawlerRunConfig
config
=
CrawlerRunConfig
(
js\_code
=
"""
const downloadLink = document.querySelector('a[href$=".exe"]');
if (downloadLink) {
downloadLink.click();
}
"""
,
wait\_for
=
5
# Wait 5 seconds for the download to start
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
"https://www.python.org/downloads/"
,
config
=
config
)
Accessing Downloaded Files
The
downloaded\_files
attribute of the
CrawlResult
object contains paths to downloaded files.
if
result
.
downloaded\_files
:
print
(
"Downloaded files:"
)
for
file\_path
in
result
.
downloaded\_files
:
print
(
f
"-
{
file\_path
}
"
)
file\_size
=
os
.
path
.
getsize
(
file\_path
)
print
(
f
"- File size:
{
file\_size
}
bytes"
)
else
:
print
(
"No files downloaded."
)
Example: Downloading Multiple Files
from
crawl4ai.async\_configs
import
BrowserConfig
,
CrawlerRunConfig
import
os
from
pathlib
import
Path
async
def
download\_multiple\_files
(
url
:
str
,
download\_path
:
str
):
config
=
BrowserConfig
(
accept\_downloads
=
True
,
downloads\_path
=
download\_path
)
async
with
AsyncWebCrawler
(
config
=
config
)
as
crawler
:
run\_config
=
CrawlerRunConfig
(
js\_code
=
"""
const downloadLinks = document.querySelectorAll('a[download]');
for (const link of downloadLinks) {
link.click();
// Delay between clicks
await new Promise(r => setTimeout(r, 2000));
}
"""
,
wait\_for
=
10
# Wait for all downloads to start
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
url
,
config
=
run\_config
)
if
result
.
downloaded\_files
:
print
(
"Downloaded files:"
)
for
file
in
result
.
downloaded\_files
:
print
(
f
"-
{
file
}
"
)
else
:
print
(
"No files downloaded."
)
# Usage
download\_path
=
os
.
path
.
join
(
Path
.
home
(),
".crawl4ai"
,
"downloads"
)
os
.
makedirs
(
download\_path
,
exist\_ok
=
True
)
asyncio
.
run
(
download\_multiple\_files
(
"https://www.python.org/downloads/windows/"
,
download\_path
))
Important Considerations
Browser Context:
Downloads are managed within the browser context. Ensure
js\_code
correctly targets the download triggers on the webpage.
Timing:
Use
wait\_for
in
CrawlerRunConfig
to manage download timing.
Error Handling:
Handle errors to manage failed downloads or incorrect paths gracefully.
Security:
Scan downloaded files for potential security threats before use.
This revised guide ensures consistency with the
Crawl4AI
codebase by using
BrowserConfig
and
CrawlerRunConfig
for all download-related configurations. Let me know if further adjustments are needed!
Search
Type to start searching