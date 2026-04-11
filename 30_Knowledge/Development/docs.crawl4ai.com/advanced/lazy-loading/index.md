Lazy Loading - Crawl4AI Documentation (v0.4.3bx)
Handling Lazy-Loaded Images
Many websites now load images
lazily
as you scroll. If you need to ensure they appear in your final crawl (and in
result.media
), consider:
1.
wait\_for\_images=True
– Wait for images to fully load.
2.
scan\_full\_page
– Force the crawler to scroll the entire page, triggering lazy loads.
3.
scroll\_delay
– Add small delays between scroll steps.
Note
: If the site requires multiple “Load More” triggers or complex interactions, see the
Page Interaction docs
.
Example: Ensuring Lazy Images Appear
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
,
BrowserConfig
from
crawl4ai.async\_configs
import
CacheMode
async
def
main
():
config
=
CrawlerRunConfig
(
# Force the crawler to wait until images are fully loaded
wait\_for\_images
=
True
,
# Option 1: If you want to automatically scroll the page to load images
scan\_full\_page
=
True
,
# Tells the crawler to try scrolling the entire page
scroll\_delay
=
0.5
,
# Delay (seconds) between scroll steps
# Option 2: If the site uses a 'Load More' or JS triggers for images,
# you can also specify js\_code or wait\_for logic here.
cache\_mode
=
CacheMode
.
BYPASS
,
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
BrowserConfig
(
headless
=
True
))
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
"https://www.example.com/gallery"
,
config
=
config
)
if
result
.
success
:
images
=
result
.
media
.
get
(
"images"
,
[])
print
(
"Images found:"
,
len
(
images
))
for
i
,
img
in
enumerate
(
images
[:
5
]):
print
(
f
"[Image
{
i
}
] URL:
{
img
[
'src'
]
}
, Score:
{
img
.
get
(
'score'
,
'N/A'
)
}
"
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
Explanation
:
wait\_for\_images=True
The crawler tries to ensure images have finished loading before finalizing the HTML.
scan\_full\_page=True
Tells the crawler to attempt scrolling from top to bottom. Each scroll step helps trigger lazy loading.
scroll\_delay=0.5
Pause half a second between each scroll step. Helps the site load images before continuing.
When to Use
:
Lazy-Loading
: If images appear only when the user scrolls into view,
scan\_full\_page
+
scroll\_delay
helps the crawler see them.
Heavier Pages
: If a page is extremely long, be mindful that scanning the entire page can be slow. Adjust
scroll\_delay
or the max scroll steps as needed.
Combining with Other Link & Media Filters
You can still combine
lazy-load
logic with the usual
exclude\_external\_images
,
exclude\_domains
, or link filtration:
config
=
CrawlerRunConfig
(
wait\_for\_images
=
True
,
scan\_full\_page
=
True
,
scroll\_delay
=
0.5
,
# Filter out external images if you only want local ones
exclude\_external\_images
=
True
,
# Exclude certain domains for links
exclude\_domains
=
[
"spammycdn.com"
],
)
This approach ensures you see
all
images from the main domain while ignoring external ones, and the crawler physically scrolls the entire page so that lazy-loading triggers.
Tips & Troubleshooting
1.
Long Pages
- Setting
scan\_full\_page=True
on extremely long or infinite-scroll pages can be resource-intensive.
- Consider using
hooks
or specialized logic to load specific sections or “Load More” triggers repeatedly.
2.
Mixed Image Behavior
- Some sites load images in batches as you scroll. If you’re missing images, increase your
scroll\_delay
or call multiple partial scrolls in a loop with JS code or hooks.
3.
Combining with Dynamic Wait
- If the site has a placeholder that only changes to a real image after a certain event, you might do
wait\_for="css:img.loaded"
or a custom JS
wait\_for
.
4.
Caching
- If
cache\_mode
is enabled, repeated crawls might skip some network fetches. If you suspect caching is missing new images, set
cache\_mode=CacheMode.BYPASS
for fresh fetches.
With
lazy-loading
support,
wait\_for\_images
, and
scan\_full\_page
settings, you can capture the entire gallery or feed of images you expect—even if the site only loads them as the user scrolls. Combine these with the standard media filtering and domain exclusion for a complete link & media handling strategy.
Search
Type to start searching