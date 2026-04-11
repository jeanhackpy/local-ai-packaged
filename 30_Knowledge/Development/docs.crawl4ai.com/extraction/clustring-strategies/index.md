Clustering Strategies - Crawl4AI Documentation (v0.4.3bx)
Cosine Strategy
The Cosine Strategy in Crawl4AI uses similarity-based clustering to identify and extract relevant content sections from web pages. This strategy is particularly useful when you need to find and extract content based on semantic similarity rather than structural patterns.
How It Works
The Cosine Strategy:
1. Breaks down page content into meaningful chunks
2. Converts text into vector representations
3. Calculates similarity between chunks
4. Clusters similar content together
5. Ranks and filters content based on relevance
Basic Usage
from
crawl4ai.extraction\_strategy
import
CosineStrategy
strategy
=
CosineStrategy
(
semantic\_filter
=
"product reviews"
,
# Target content type
word\_count\_threshold
=
10
,
# Minimum words per cluster
sim\_threshold
=
0.3
# Similarity threshold
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
"https://example.com/reviews"
,
extraction\_strategy
=
strategy
)
content
=
result
.
extracted\_content
Configuration Options
Core Parameters
CosineStrategy
(
# Content Filtering
semantic\_filter
:
str
=
None
,
# Keywords/topic for content filtering
word\_count\_threshold
:
int
=
10
,
# Minimum words per cluster
sim\_threshold
:
float
=
0.3
,
# Similarity threshold (0.0 to 1.0)
# Clustering Parameters
max\_dist
:
float
=
0.2
,
# Maximum distance for clustering
linkage\_method
:
str
=
'ward'
,
# Clustering linkage method
top\_k
:
int
=
3
,
# Number of top categories to extract
# Model Configuration
model\_name
:
str
=
'sentence-transformers/all-MiniLM-L6-v2'
,
# Embedding model
verbose
:
bool
=
False
# Enable logging
)
Parameter Details
1.
semantic\_filter
- Sets the target topic or content type
- Use keywords relevant to your desired content
- Example: "technical specifications", "user reviews", "pricing information"
2.
sim\_threshold
- Controls how similar content must be to be grouped together
- Higher values (e.g., 0.8) mean stricter matching
- Lower values (e.g., 0.3) allow more variation
# Strict matching
strategy
=
CosineStrategy
(
sim\_threshold
=
0.8
)
# Loose matching
strategy
=
CosineStrategy
(
sim\_threshold
=
0.3
)
3.
word\_count\_threshold
- Filters out short content blocks
- Helps eliminate noise and irrelevant content
# Only consider substantial paragraphs
strategy
=
CosineStrategy
(
word\_count\_threshold
=
50
)
4.
top\_k
- Number of top content clusters to return
- Higher values return more diverse content
# Get top 5 most relevant content clusters
strategy
=
CosineStrategy
(
top\_k
=
5
)
Use Cases
1. Article Content Extraction
strategy
=
CosineStrategy
(
semantic\_filter
=
"main article content"
,
word\_count\_threshold
=
100
,
# Longer blocks for articles
top\_k
=
1
# Usually want single main content
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
"https://example.com/blog/post"
,
extraction\_strategy
=
strategy
)
2. Product Review Analysis
strategy
=
CosineStrategy
(
semantic\_filter
=
"customer reviews and ratings"
,
word\_count\_threshold
=
20
,
# Reviews can be shorter
top\_k
=
10
,
# Get multiple reviews
sim\_threshold
=
0.4
# Allow variety in review content
)
3. Technical Documentation
strategy
=
CosineStrategy
(
semantic\_filter
=
"technical specifications documentation"
,
word\_count\_threshold
=
30
,
sim\_threshold
=
0.6
,
# Stricter matching for technical content
max\_dist
=
0.3
# Allow related technical sections
)
Advanced Features
Custom Clustering
strategy
=
CosineStrategy
(
linkage\_method
=
'complete'
,
# Alternative clustering method
max\_dist
=
0.4
,
# Larger clusters
model\_name
=
'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
# Multilingual support
)
Content Filtering Pipeline
strategy
=
CosineStrategy
(
semantic\_filter
=
"pricing plans features"
,
word\_count\_threshold
=
15
,
sim\_threshold
=
0.5
,
top\_k
=
3
)
async
def
extract\_pricing\_features
(
url
:
str
):
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
url
,
extraction\_strategy
=
strategy
)
if
result
.
success
:
content
=
json
.
loads
(
result
.
extracted\_content
)
return
{
'pricing\_features'
:
content
,
'clusters'
:
len
(
content
),
'similarity\_scores'
:
[
item
[
'score'
]
for
item
in
content
]
}
Best Practices
1.
Adjust Thresholds Iteratively
- Start with default values
- Adjust based on results
- Monitor clustering quality
2.
Choose Appropriate Word Count Thresholds
- Higher for articles (100+)
- Lower for reviews/comments (20+)
- Medium for product descriptions (50+)
3.
Optimize Performance
strategy
=
CosineStrategy
(
word\_count\_threshold
=
10
,
# Filter early
top\_k
=
5
,
# Limit results
verbose
=
True
# Monitor performance
)
4.
Handle Different Content Types
# For mixed content pages
strategy
=
CosineStrategy
(
semantic\_filter
=
"product features"
,
sim\_threshold
=
0.4
,
# More flexible matching
max\_dist
=
0.3
,
# Larger clusters
top\_k
=
3
# Multiple relevant sections
)
Error Handling
try
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
extraction\_strategy
=
strategy
)
if
result
.
success
:
content
=
json
.
loads
(
result
.
extracted\_content
)
if
not
content
:
print
(
"No relevant content found"
)
else
:
print
(
f
"Extraction failed:
{
result
.
error\_message
}
"
)
except
Exception
as
e
:
print
(
f
"Error during extraction:
{
str
(
e
)
}
"
)
The Cosine Strategy is particularly effective when:
- Content structure is inconsistent
- You need semantic understanding
- You want to find similar content blocks
- Structure-based extraction (CSS/XPath) isn't reliable
It works well with other strategies and can be used as a pre-processing step for LLM-based extraction.
Search
Type to start searching