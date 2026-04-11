Strategies - Crawl4AI Documentation (v0.4.3bx)
Extraction & Chunking Strategies API
This documentation covers the API reference for extraction and chunking strategies in Crawl4AI.
Extraction Strategies
All extraction strategies inherit from the base
ExtractionStrategy
class and implement two key methods:
-
extract(url: str, html: str) -> List[Dict[str, Any]]
-
run(url: str, sections: List[str]) -> List[Dict[str, Any]]
LLMExtractionStrategy
Used for extracting structured data using Language Models.
LLMExtractionStrategy
(
# Required Parameters
provider
:
str
=
DEFAULT\_PROVIDER
,
# LLM provider (e.g., "ollama/llama2")
api\_token
:
Optional
[
str
]
=
None
,
# API token
# Extraction Configuration
instruction
:
str
=
None
,
# Custom extraction instruction
schema
:
Dict
=
None
,
# Pydantic model schema for structured data
extraction\_type
:
str
=
"block"
,
# "block" or "schema"
# Chunking Parameters
chunk\_token\_threshold
:
int
=
4000
,
# Maximum tokens per chunk
overlap\_rate
:
float
=
0.1
,
# Overlap between chunks
word\_token\_rate
:
float
=
0.75
,
# Word to token conversion rate
apply\_chunking
:
bool
=
True
,
# Enable/disable chunking
# API Configuration
base\_url
:
str
=
None
,
# Base URL for API
extra\_args
:
Dict
=
{},
# Additional provider arguments
verbose
:
bool
=
False
# Enable verbose logging
)
CosineStrategy
Used for content similarity-based extraction and clustering.
CosineStrategy
(
# Content Filtering
semantic\_filter
:
str
=
None
,
# Topic/keyword filter
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
# Similarity threshold
# Clustering Parameters
max\_dist
:
float
=
0.2
,
# Maximum cluster distance
linkage\_method
:
str
=
'ward'
,
# Clustering method
top\_k
:
int
=
3
,
# Top clusters to return
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
# Enable verbose logging
)
JsonCssExtractionStrategy
Used for CSS selector-based structured data extraction.
JsonCssExtractionStrategy
(
schema
:
Dict
[
str
,
Any
],
# Extraction schema
verbose
:
bool
=
False
# Enable verbose logging
)
# Schema Structure
schema
=
{
"name"
:
str
,
# Schema name
"baseSelector"
:
str
,
# Base CSS selector
"fields"
:
[
# List of fields to extract
{
"name"
:
str
,
# Field name
"selector"
:
str
,
# CSS selector
"type"
:
str
,
# Field type: "text", "attribute", "html", "regex"
"attribute"
:
str
,
# For type="attribute"
"pattern"
:
str
,
# For type="regex"
"transform"
:
str
,
# Optional: "lowercase", "uppercase", "strip"
"default"
:
Any
# Default value if extraction fails
}
]
}
Chunking Strategies
All chunking strategies inherit from
ChunkingStrategy
and implement the
chunk(text: str) -> list
method.
RegexChunking
Splits text based on regex patterns.
RegexChunking
(
patterns
:
List
[
str
]
=
None
# Regex patterns for splitting
# Default: [r'\n\n']
)
SlidingWindowChunking
Creates overlapping chunks with a sliding window approach.
SlidingWindowChunking
(
window\_size
:
int
=
100
,
# Window size in words
step
:
int
=
50
# Step size between windows
)
OverlappingWindowChunking
Creates chunks with specified overlap.
OverlappingWindowChunking
(
window\_size
:
int
=
1000
,
# Chunk size in words
overlap
:
int
=
100
# Overlap size in words
)
Usage Examples
LLM Extraction
from
pydantic
import
BaseModel
from
crawl4ai.extraction\_strategy
import
LLMExtractionStrategy
# Define schema
class
Article
(
BaseModel
):
title
:
str
content
:
str
author
:
str
# Create strategy
strategy
=
LLMExtractionStrategy
(
provider
=
"ollama/llama2"
,
schema
=
Article
.
schema
(),
instruction
=
"Extract article details"
)
# Use with crawler
result
=
await
crawler
.
arun
(
url
=
"https://example.com/article"
,
extraction\_strategy
=
strategy
)
# Access extracted data
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
CSS Extraction
from
crawl4ai.extraction\_strategy
import
JsonCssExtractionStrategy
# Define schema
schema
=
{
"name"
:
"Product List"
,
"baseSelector"
:
".product-card"
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
"h2.title"
,
"type"
:
"text"
},
{
"name"
:
"price"
,
"selector"
:
".price"
,
"type"
:
"text"
,
"transform"
:
"strip"
},
{
"name"
:
"image"
,
"selector"
:
"img"
,
"type"
:
"attribute"
,
"attribute"
:
"src"
}
]
}
# Create and use strategy
strategy
=
JsonCssExtractionStrategy
(
schema
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
"https://example.com/products"
,
extraction\_strategy
=
strategy
)
Content Chunking
from
crawl4ai.chunking\_strategy
import
OverlappingWindowChunking
# Create chunking strategy
chunker
=
OverlappingWindowChunking
(
window\_size
=
500
,
# 500 words per chunk
overlap
=
50
# 50 words overlap
)
# Use with extraction strategy
strategy
=
LLMExtractionStrategy
(
provider
=
"ollama/llama2"
,
chunking\_strategy
=
chunker
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
"https://example.com/long-article"
,
extraction\_strategy
=
strategy
)
Best Practices
1.
Choose the Right Strategy
- Use
LLMExtractionStrategy
for complex, unstructured content
- Use
JsonCssExtractionStrategy
for well-structured HTML
- Use
CosineStrategy
for content similarity and clustering
2.
Optimize Chunking
# For long documents
strategy
=
LLMExtractionStrategy
(
chunk\_token\_threshold
=
2000
,
# Smaller chunks
overlap\_rate
=
0.1
# 10% overlap
)
3.
Handle Errors
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
except
Exception
as
e
:
print
(
f
"Extraction failed:
{
e
}
"
)
4.
Monitor Performance
strategy
=
CosineStrategy
(
verbose
=
True
,
# Enable logging
word\_count\_threshold
=
20
,
# Filter short content
top\_k
=
5
# Limit results
)
Search
Type to start searching