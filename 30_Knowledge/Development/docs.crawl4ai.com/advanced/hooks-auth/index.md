Hooks & Auth - Crawl4AI Documentation (v0.4.3bx)
Hooks & Auth in AsyncWebCrawler
Crawl4AI’s
hooks
let you customize the crawler at specific points in the pipeline:
1.
on\_browser\_created
– After browser creation.
2.
on\_page\_context\_created
– After a new context & page are created.
3.
before\_goto
– Just before navigating to a page.
4.
after\_goto
– Right after navigation completes.
5.
on\_user\_agent\_updated
– Whenever the user agent changes.
6.
on\_execution\_started
– Once custom JavaScript execution begins.
7.
before\_retrieve\_html
– Just before the crawler retrieves final HTML.
8.
before\_return\_html
– Right before returning the HTML content.
Important
: Avoid heavy tasks in
on\_browser\_created
since you don’t yet have a page context. If you need to
log in
, do so in
on\_page\_context\_created
.
note "Important Hook Usage Warning"
Avoid Misusing Hooks
: Do not manipulate page objects in the wrong hook or at the wrong time, as it can crash the pipeline or produce incorrect results. A common mistake is attempting to handle authentication prematurely—such as creating or closing pages in
on\_browser\_created
.
Use the Right Hook for Auth
: If you need to log in or set tokens, use
on\_page\_context\_created
. This ensures you have a valid page/context to work with, without disrupting the main crawling flow.
Identity-Based Crawling
: For robust auth, consider identity-based crawling (or passing a session ID) to preserve state. Run your initial login steps in a separate, well-defined process, then feed that session to your main crawl—rather than shoehorning complex authentication into early hooks. Check out
Identity-Based Crawling
for more details.
Be Cautious
: Overwriting or removing elements in the wrong hook can compromise the final crawl. Keep hooks focused on smaller tasks (like route filters, custom headers), and let your main logic (crawling, data extraction) proceed normally.
Below is an example demonstration.
Example: Using Hooks in AsyncWebCrawler
import
asyncio
import
json
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
playwright.async\_api
import
Page
,
BrowserContext
async
def
main
():
print
(
"🔗 Hooks Example: Demonstrating recommended usage"
)
# 1) Configure the browser
browser\_config
=
BrowserConfig
(
headless
=
True
,
verbose
=
True
)
# 2) Configure the crawler run
crawler\_run\_config
=
CrawlerRunConfig
(
js\_code
=
"window.scrollTo(0, document.body.scrollHeight);"
,
wait\_for
=
"body"
,
cache\_mode
=
CacheMode
.
BYPASS
)
# 3) Create the crawler instance
crawler
=
AsyncWebCrawler
(
config
=
browser\_config
)
#
# Define Hook Functions
#
async
def
on\_browser\_created
(
browser
,
\*\*
kwargs
):
# Called once the browser instance is created (but no pages or contexts yet)
print
(
"[HOOK] on\_browser\_created - Browser created successfully!"
)
# Typically, do minimal setup here if needed
return
browser
async
def
on\_page\_context\_created
(
page
:
Page
,
context
:
BrowserContext
,
\*\*
kwargs
):
# Called right after a new page + context are created (ideal for auth or route config).
print
(
"[HOOK] on\_page\_context\_created - Setting up page & context."
)
# Example 1: Route filtering (e.g., block images)
async
def
route\_filter
(
route
):
if
route
.
request
.
resource\_type
==
"image"
:
print
(
f
"[HOOK] Blocking image request:
{
route
.
request
.
url
}
"
)
await
route
.
abort
()
else
:
await
route
.
continue\_
()
await
context
.
route
(
"\*\*"
,
route\_filter
)
# Example 2: (Optional) Simulate a login scenario
# (We do NOT create or close pages here, just do quick steps if needed)
# e.g., await page.goto("https://example.com/login")
# e.g., await page.fill("input[name='username']", "testuser")
# e.g., await page.fill("input[name='password']", "password123")
# e.g., await page.click("button[type='submit']")
# e.g., await page.wait\_for\_selector("#welcome")
# e.g., await context.add\_cookies([...])
# Then continue
# Example 3: Adjust the viewport
await
page
.
set\_viewport\_size
({
"width"
:
1080
,
"height"
:
600
})
return
page
async
def
before\_goto
(
page
:
Page
,
context
:
BrowserContext
,
url
:
str
,
\*\*
kwargs
):
# Called before navigating to each URL.
print
(
f
"[HOOK] before\_goto - About to navigate:
{
url
}
"
)
# e.g., inject custom headers
await
page
.
set\_extra\_http\_headers
({
"Custom-Header"
:
"my-value"
})
return
page
async
def
after\_goto
(
page
:
Page
,
context
:
BrowserContext
,
url
:
str
,
response
,
\*\*
kwargs
):
# Called after navigation completes.
print
(
f
"[HOOK] after\_goto - Successfully loaded:
{
url
}
"
)
# e.g., wait for a certain element if we want to verify
try
:
await
page
.
wait\_for\_selector
(
'.content'
,
timeout
=
1000
)
print
(
"[HOOK] Found .content element!"
)
except
:
print
(
"[HOOK] .content not found, continuing anyway."
)
return
page
async
def
on\_user\_agent\_updated
(
page
:
Page
,
context
:
BrowserContext
,
user\_agent
:
str
,
\*\*
kwargs
):
# Called whenever the user agent updates.
print
(
f
"[HOOK] on\_user\_agent\_updated - New user agent:
{
user\_agent
}
"
)
return
page
async
def
on\_execution\_started
(
page
:
Page
,
context
:
BrowserContext
,
\*\*
kwargs
):
# Called after custom JavaScript execution begins.
print
(
"[HOOK] on\_execution\_started - JS code is running!"
)
return
page
async
def
before\_retrieve\_html
(
page
:
Page
,
context
:
BrowserContext
,
\*\*
kwargs
):
# Called before final HTML retrieval.
print
(
"[HOOK] before\_retrieve\_html - We can do final actions"
)
# Example: Scroll again
await
page
.
evaluate
(
"window.scrollTo(0, document.body.scrollHeight);"
)
return
page
async
def
before\_return\_html
(
page
:
Page
,
context
:
BrowserContext
,
html
:
str
,
\*\*
kwargs
):
# Called just before returning the HTML in the result.
print
(
f
"[HOOK] before\_return\_html - HTML length:
{
len
(
html
)
}
"
)
return
page
#
# Attach Hooks
#
crawler
.
crawler\_strategy
.
set\_hook
(
"on\_browser\_created"
,
on\_browser\_created
)
crawler
.
crawler\_strategy
.
set\_hook
(
"on\_page\_context\_created"
,
on\_page\_context\_created
)
crawler
.
crawler\_strategy
.
set\_hook
(
"before\_goto"
,
before\_goto
)
crawler
.
crawler\_strategy
.
set\_hook
(
"after\_goto"
,
after\_goto
)
crawler
.
crawler\_strategy
.
set\_hook
(
"on\_user\_agent\_updated"
,
on\_user\_agent\_updated
)
crawler
.
crawler\_strategy
.
set\_hook
(
"on\_execution\_started"
,
on\_execution\_started
)
crawler
.
crawler\_strategy
.
set\_hook
(
"before\_retrieve\_html"
,
before\_retrieve\_html
)
crawler
.
crawler\_strategy
.
set\_hook
(
"before\_return\_html"
,
before\_return\_html
)
await
crawler
.
start
()
# 4) Run the crawler on an example page
url
=
"https://example.com"
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
crawler\_run\_config
)
if
result
.
success
:
print
(
"
\n
Crawled URL:"
,
result
.
url
)
print
(
"HTML length:"
,
len
(
result
.
html
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
await
crawler
.
close
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
Hook Lifecycle Summary
1.
on\_browser\_created
:
- Browser is up, but
no
pages or contexts yet.
- Light setup only—don’t try to open or close pages here (that belongs in
on\_page\_context\_created
).
2.
on\_page\_context\_created
:
- Perfect for advanced
auth
or route blocking.
- You have a
page
+
context
ready but haven’t navigated to the target URL yet.
3.
before\_goto
:
- Right before navigation. Typically used for setting
custom headers
or logging the target URL.
4.
after\_goto
:
- After page navigation is done. Good place for verifying content or waiting on essential elements.
5.
on\_user\_agent\_updated
:
- Whenever the user agent changes (for stealth or different UA modes).
6.
on\_execution\_started
:
- If you set
js\_code
or run custom scripts, this runs once your JS is about to start.
7.
before\_retrieve\_html
:
- Just before the final HTML snapshot is taken. Often you do a final scroll or lazy-load triggers here.
8.
before\_return\_html
:
- The last hook before returning HTML to the
CrawlResult
. Good for logging HTML length or minor modifications.
When to Handle Authentication
Recommended
: Use
on\_page\_context\_created
if you need to:
Navigate to a login page or fill forms
Set cookies or localStorage tokens
Block resource routes to avoid ads
This ensures the newly created context is under your control
before
arun()
navigates to the main URL.
Additional Considerations
Session Management
: If you want multiple
arun()
calls to reuse a single session, pass
session\_id=
in your
CrawlerRunConfig
. Hooks remain the same.
Performance
: Hooks can slow down crawling if they do heavy tasks. Keep them concise.
Error Handling
: If a hook fails, the overall crawl might fail. Catch exceptions or handle them gracefully.
Concurrency
: If you run
arun\_many()
, each URL triggers these hooks in parallel. Ensure your hooks are thread/async-safe.
Conclusion
Hooks provide
fine-grained
control over:
Browser
creation (light tasks only)
Page
and
context
creation (auth, route blocking)
Navigation
phases
Final HTML
retrieval
Follow the recommended usage:
-
Login
or advanced tasks in
on\_page\_context\_created
-
Custom headers
or logs in
before\_goto
/
after\_goto
-
Scrolling
or final checks in
before\_retrieve\_html
/
before\_return\_html
Search
Type to start searching