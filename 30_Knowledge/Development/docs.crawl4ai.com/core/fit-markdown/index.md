Fit Markdown - Crawl4AI Documentation (v0.4.3bx)
Fit Markdown with Pruning & BM25
Fit Markdown
is a specialized
filtered
version of your page’s markdown, focusing on the most relevant content. By default, Crawl4AI converts the entire HTML into a broad
raw\_markdown
. With fit markdown, we apply a
content filter
algorithm (e.g.,
Pruning
or
BM25
) to remove or rank low-value sections—such as repetitive sidebars, shallow text blocks, or irrelevancies—leaving a concise textual “core.”
1. How “Fit Markdown” Works
1.1 The
content\_filter
In
CrawlerRunConfig
, you can specify a
content\_filter
to shape how content is pruned or ranked before final markdown generation. A filter’s logic is applied
before
or
during
the HTML→Markdown process, producing:
result.markdown\_v2.raw\_markdown
(unfiltered)
result.markdown\_v2.fit\_markdown
(filtered or “fit” version)
result.markdown\_v2.fit\_html
(the corresponding HTML snippet that produced
fit\_markdown
)
Note
: We’re currently storing the result in
markdown\_v2
, but eventually we’ll unify it as
result.markdown
.
1.2 Common Filters
1.
PruningContentFilter
– Scores each node by text density, link density, and tag importance, discarding those below a threshold.
2.
BM25ContentFilter
– Focuses on textual relevance using BM25 ranking, especially useful if you have a specific user query (e.g., “machine learning” or “food nutrition”).
2. PruningContentFilter
Pruning
discards less relevant nodes based on
text density, link density, and tag importance
. It’s a heuristic-based approach—if certain sections appear too “thin” or too “spammy,” they’re pruned.
2.1 Usage Example
import
asyncio
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
async
def
main
():
# Step 1: Create a pruning filter
prune\_filter
=
PruningContentFilter
(
# Lower → more content retained, higher → more content pruned
threshold
=
0.45
,
# "fixed" or "dynamic"
threshold\_type
=
"dynamic"
,
# Ignore nodes with <5 words
min\_word\_threshold
=
5
)
# Step 2: Insert it into a Markdown Generator
md\_generator
=
DefaultMarkdownGenerator
(
content\_filter
=
prune\_filter
)
# Step 3: Pass it to CrawlerRunConfig
config
=
CrawlerRunConfig
(
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
url
=
"https://news.ycombinator.com"
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
# 'fit\_markdown' is your pruned content, focusing on "denser" text
print
(
"Raw Markdown length:"
,
len
(
result
.
markdown\_v2
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
markdown\_v2
.
fit\_markdown
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
2.2 Key Parameters
min\_word\_threshold
(int): If a block has fewer words than this, it’s pruned.
threshold\_type
(str):
"fixed"
→ each node must exceed
threshold
(0–1).
"dynamic"
→ node scoring adjusts according to tag type, text/link density, etc.
threshold
(float, default ~0.48): The base or “anchor” cutoff.
Algorithmic Factors
:
Text density
– Encourages blocks that have a higher ratio of text to overall content.
Link density
– Penalizes sections that are mostly links.
Tag importance
– e.g., an
or

might be more important than a
.
Structural context
– If a node is deeply nested or in a suspected sidebar, it might be deprioritized.
3. BM25ContentFilter
BM25
is a classical text ranking algorithm often used in search engines. If you have a
user query
or rely on page metadata to derive a query, BM25 can identify which text chunks best match that query.
3.1 Usage Example
import
asyncio
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
from
crawl4ai.content\_filter\_strategy
import
BM25ContentFilter
from
crawl4ai.markdown\_generation\_strategy
import
DefaultMarkdownGenerator
async
def
main
():
# 1) A BM25 filter with a user query
bm25\_filter
=
BM25ContentFilter
(
user\_query
=
"startup fundraising tips"
,
# Adjust for stricter or looser results
bm25\_threshold
=
1.2
)
# 2) Insert into a Markdown Generator
md\_generator
=
DefaultMarkdownGenerator
(
content\_filter
=
bm25\_filter
)
# 3) Pass to crawler config
config
=
CrawlerRunConfig
(
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
url
=
"https://news.ycombinator.com"
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
print
(
"Fit Markdown (BM25 query-based):"
)
print
(
result
.
markdown\_v2
.
fit\_markdown
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
3.2 Parameters
user\_query
(str, optional): E.g.
"machine learning"
. If blank, the filter tries to glean a query from page metadata.
bm25\_threshold
(float, default 1.0):
Higher → fewer chunks but more relevant.
Lower → more inclusive.
In more advanced scenarios, you might see parameters like
use\_stemming
,
case\_sensitive
, or
priority\_tags
to refine how text is tokenized or weighted.
4. Accessing the “Fit” Output
After the crawl, your “fit” content is found in
result.markdown\_v2.fit\_markdown
. In future versions, it will be
result.markdown.fit\_markdown
. Meanwhile:
fit\_md
=
result
.
markdown\_v2
.
fit\_markdown
fit\_html
=
result
.
markdown\_v2
.
fit\_html
If the content filter is
BM25
, you might see additional logic or references in
fit\_markdown
that highlight relevant segments. If it’s
Pruning
, the text is typically well-cleaned but not necessarily matched to a query.
5. Code Patterns Recap
5.1 Pruning
prune\_filter
=
PruningContentFilter
(
threshold
=
0.5
,
threshold\_type
=
"fixed"
,
min\_word\_threshold
=
10
)
md\_generator
=
DefaultMarkdownGenerator
(
content\_filter
=
prune\_filter
)
config
=
CrawlerRunConfig
(
markdown\_generator
=
md\_generator
)
# => result.markdown\_v2.fit\_markdown
5.2 BM25
bm25\_filter
=
BM25ContentFilter
(
user\_query
=
"health benefits fruit"
,
bm25\_threshold
=
1.2
)
md\_generator
=
DefaultMarkdownGenerator
(
content\_filter
=
bm25\_filter
)
config
=
CrawlerRunConfig
(
markdown\_generator
=
md\_generator
)
# => result.markdown\_v2.fit\_markdown
6. Combining with “word\_count\_threshold” & Exclusions
Remember you can also specify:
config
=
CrawlerRunConfig
(
word\_count\_threshold
=
10
,
excluded\_tags
=
[
"nav"
,
"footer"
,
"header"
],
exclude\_external\_links
=
True
,
markdown\_generator
=
DefaultMarkdownGenerator
(
content\_filter
=
PruningContentFilter
(
threshold
=
0.5
)
)
)
Thus,
multi-level
filtering occurs:
The crawler’s
excluded\_tags
are removed from the HTML first.
The content filter (Pruning, BM25, or custom) prunes or ranks the remaining text blocks.
The final “fit” content is generated in
result.markdown\_v2.fit\_markdown
.
7. Custom Filters
If you need a different approach (like a specialized ML model or site-specific heuristics), you can create a new class inheriting from
RelevantContentFilter
and implement
filter\_content(html)
. Then inject it into your
markdown generator
:
from
crawl4ai.content\_filter\_strategy
import
RelevantContentFilter
class
MyCustomFilter
(
RelevantContentFilter
):
def
filter\_content
(
self
,
html
,
min\_word\_threshold
=
None
):
# parse HTML, implement custom logic
return
[
block
for
block
in
...
if
...
some
condition
...
]
Steps
:
Subclass
RelevantContentFilter
.
Implement
filter\_content(...)
.
Use it in your
DefaultMarkdownGenerator(content\_filter=MyCustomFilter(...))
.
8. Final Thoughts
Fit Markdown
is a crucial feature for:
Summaries
: Quickly get the important text from a cluttered page.
Search
: Combine with
BM25
to produce content relevant to a query.
AI Pipelines
: Filter out boilerplate so LLM-based extraction or summarization runs on denser text.
Key Points
:
-
PruningContentFilter
: Great if you just want the “meatiest” text without a user query.
-
BM25ContentFilter
: Perfect for query-based extraction or searching.
- Combine with
excluded\_tags
,
exclude\_external\_links
,
word\_count\_threshold
to refine your final “fit” text.
- Fit markdown ends up in
result.markdown\_v2.fit\_markdown
; eventually
result.markdown.fit\_markdown
in future versions.
With these tools, you can
zero in
on the text that truly matters, ignoring spammy or boilerplate content, and produce a concise, relevant “fit markdown” for your AI or data pipelines. Happy pruning and searching!
Last Updated: 2025-01-01
Search
Type to start searching

