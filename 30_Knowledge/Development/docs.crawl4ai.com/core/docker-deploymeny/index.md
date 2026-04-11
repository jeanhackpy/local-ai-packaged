Docker Deployment - Crawl4AI Documentation (v0.4.3bx)
Docker Deployment
Crawl4AI provides official Docker images for easy deployment and scalability. This guide covers installation, configuration, and usage of Crawl4AI in Docker environments.
Quick Start 🚀
Pull and run the basic version:
# Basic run without security
docker
pull
unclecode/crawl4ai:basic
docker
run
-p
11235
:11235
unclecode/crawl4ai:basic
# Run with API security enabled
docker
run
-p
11235
:11235
-e
CRAWL4AI\_API\_TOKEN
=
your\_secret\_token
unclecode/crawl4ai:basic
Running with Docker Compose 🐳
Use Docker Compose (From Local Dockerfile or Docker Hub)
Crawl4AI provides flexibility to use Docker Compose for managing your containerized services. You can either build the image locally from the provided
Dockerfile
or use the pre-built image from Docker Hub.
Option 1: Using Docker Compose to Build Locally
If you want to build the image locally, use the provided
docker-compose.local.yml
file.
docker-compose
-f
docker-compose.local.yml
up
-d
This will:
1. Build the Docker image from the provided
Dockerfile
.
2. Start the container and expose it on
http://localhost:11235
.
Option 2: Using Docker Compose with Pre-Built Image from Hub
If you prefer using the pre-built image on Docker Hub, use the
docker-compose.hub.yml
file.
docker-compose
-f
docker-compose.hub.yml
up
-d
This will:
1. Pull the pre-built image
unclecode/crawl4ai:basic
(or
all
, depending on your configuration).
2. Start the container and expose it on
http://localhost:11235
.
Stopping the Running Services
To stop the services started via Docker Compose, you can use:
docker-compose
-f
docker-compose.local.yml
down
# OR
docker-compose
-f
docker-compose.hub.yml
down
If the containers don’t stop and the application is still running, check the running containers:
docker
ps
Find the
CONTAINER ID
of the running service and stop it forcefully:
docker
stop
Debugging with Docker Compose
Check Logs
: To view the container logs:
docker-compose
-f
docker-compose.local.yml
logs
-f
Remove Orphaned Containers
: If the service is still running unexpectedly:
docker-compose
-f
docker-compose.local.yml
down
--remove-orphans
Manually Remove Network
: If the network is still in use:
docker
network
ls
docker
network
rm
crawl4ai\_default
Why Use Docker Compose?
Docker Compose is the recommended way to deploy Crawl4AI because:
1. It simplifies multi-container setups.
2. Allows you to define environment variables, resources, and ports in a single file.
3. Makes it easier to switch between local development and production-ready images.
For example, your
docker-compose.yml
could include API keys, token settings, and memory limits, making deployment quick and consistent.
API Security 🔒
Understanding CRAWL4AI\_API\_TOKEN
The
CRAWL4AI\_API\_TOKEN
provides optional security for your Crawl4AI instance:
If
CRAWL4AI\_API\_TOKEN
is set: All API endpoints (except
/health
) require authentication
If
CRAWL4AI\_API\_TOKEN
is not set: The API is publicly accessible
# Secured Instance
docker
run
-p
11235
:11235
-e
CRAWL4AI\_API\_TOKEN
=
your\_secret\_token
unclecode/crawl4ai:all
# Unsecured Instance
docker
run
-p
11235
:11235
unclecode/crawl4ai:all
Making API Calls
For secured instances, include the token in all requests:
import
requests
# Setup headers if token is being used
api\_token
=
"your\_secret\_token"
# Same token set in CRAWL4AI\_API\_TOKEN
headers
=
{
"Authorization"
:
f
"Bearer
{
api\_token
}
"
}
if
api\_token
else
{}
# Making authenticated requests
response
=
requests
.
post
(
"http://localhost:11235/crawl"
,
headers
=
headers
,
json
=
{
"urls"
:
"https://example.com"
,
"priority"
:
10
}
)
# Checking task status
task\_id
=
response
.
json
()[
"task\_id"
]
status
=
requests
.
get
(
f
"http://localhost:11235/task/
{
task\_id
}
"
,
headers
=
headers
)
Using with Docker Compose
In your
docker-compose.yml
:
services
:
crawl4ai
:
image
:
unclecode/crawl4ai:all
environment
:
-
CRAWL4AI\_API\_TOKEN=${CRAWL4AI\_API\_TOKEN:-}
# Optional
# ... other configuration
Then either:
1. Set in
.env
file:
CRAWL4AI\_API\_TOKEN=your\_secret\_token
Or set via command line:
CRAWL4AI\_API\_TOKEN
=
your\_secret\_token
docker-compose
up
Security Note
: If you enable the API token, make sure to keep it secure and never commit it to version control. The token will be required for all API endpoints except the health check endpoint (
/health
).
Configuration Options 🔧
Environment Variables
You can configure the service using environment variables:
# Basic configuration
docker
run
-p
11235
:11235
\
-e
MAX\_CONCURRENT\_TASKS
=
5
\
unclecode/crawl4ai:all
# With security and LLM support
docker
run
-p
11235
:11235
\
-e
CRAWL4AI\_API\_TOKEN
=
your\_secret\_token
\
-e
OPENAI\_API\_KEY
=
sk-...
\
-e
ANTHROPIC\_API\_KEY
=
sk-ant-...
\
unclecode/crawl4ai:all
Using Docker Compose (Recommended) 🐳
Create a
docker-compose.yml
:
version
:
'3.8'
services
:
crawl4ai
:
image
:
unclecode/crawl4ai:all
ports
:
-
"11235:11235"
environment
:
-
CRAWL4AI\_API\_TOKEN=${CRAWL4AI\_API\_TOKEN:-}
# Optional API security
-
MAX\_CONCURRENT\_TASKS=5
# LLM Provider Keys
-
OPENAI\_API\_KEY=${OPENAI\_API\_KEY:-}
-
ANTHROPIC\_API\_KEY=${ANTHROPIC\_API\_KEY:-}
volumes
:
-
/dev/shm:/dev/shm
deploy
:
resources
:
limits
:
memory
:
4G
reservations
:
memory
:
1G
You can run it in two ways:
Using environment variables directly:
CRAWL4AI\_API\_TOKEN
=
secret123
OPENAI\_API\_KEY
=
sk-...
docker-compose
up
Using a
.env
file (recommended):
Create a
.env
file in the same directory:
# API Security (optional)
CRAWL4AI\_API\_TOKEN=your\_secret\_token
# LLM Provider Keys
OPENAI\_API\_KEY=sk-...
ANTHROPIC\_API\_KEY=sk-ant-...
# Other Configuration
MAX\_CONCURRENT\_TASKS=5
Then simply run:
docker-compose
up
Testing the Deployment 🧪
import
requests
# For unsecured instances
def
test\_unsecured
():
# Health check
health
=
requests
.
get
(
"http://localhost:11235/health"
)
print
(
"Health check:"
,
health
.
json
())
# Basic crawl
response
=
requests
.
post
(
"http://localhost:11235/crawl"
,
json
=
{
"urls"
:
"https://www.nbcnews.com/business"
,
"priority"
:
10
}
)
task\_id
=
response
.
json
()[
"task\_id"
]
print
(
"Task ID:"
,
task\_id
)
# For secured instances
def
test\_secured
(
api\_token
):
headers
=
{
"Authorization"
:
f
"Bearer
{
api\_token
}
"
}
# Basic crawl with authentication
response
=
requests
.
post
(
"http://localhost:11235/crawl"
,
headers
=
headers
,
json
=
{
"urls"
:
"https://www.nbcnews.com/business"
,
"priority"
:
10
}
)
task\_id
=
response
.
json
()[
"task\_id"
]
print
(
"Task ID:"
,
task\_id
)
LLM Extraction Example 🤖
When you've configured your LLM provider keys (via environment variables or
.env
), you can use LLM extraction:
request
=
{
"urls"
:
"https://example.com"
,
"extraction\_config"
:
{
"type"
:
"llm"
,
"params"
:
{
"provider"
:
"openai/gpt-4"
,
"instruction"
:
"Extract main topics from the page"
}
}
}
# Make the request (add headers if using API security)
response
=
requests
.
post
(
"http://localhost:11235/crawl"
,
json
=
request
)
Note
: Remember to add
.env
to your
.gitignore
to keep your API keys secure!
Usage Examples 📝
Basic Crawling
request
=
{
"urls"
:
"https://www.nbcnews.com/business"
,
"priority"
:
10
}
response
=
requests
.
post
(
"http://localhost:11235/crawl"
,
json
=
request
)
task\_id
=
response
.
json
()[
"task\_id"
]
# Get results
result
=
requests
.
get
(
f
"http://localhost:11235/task/
{
task\_id
}
"
)
Structured Data Extraction
schema
=
{
"name"
:
"Crypto Prices"
,
"baseSelector"
:
".cds-tableRow-t45thuk"
,
"fields"
:
[
{
"name"
:
"crypto"
,
"selector"
:
"td:nth-child(1) h2"
,
"type"
:
"text"
,
},
{
"name"
:
"price"
,
"selector"
:
"td:nth-child(2)"
,
"type"
:
"text"
,
}
],
}
request
=
{
"urls"
:
"https://www.coinbase.com/explore"
,
"extraction\_config"
:
{
"type"
:
"json\_css"
,
"params"
:
{
"schema"
:
schema
}
}
}
Dynamic Content Handling
request
=
{
"urls"
:
"https://www.nbcnews.com/business"
,
"js\_code"
:
[
"const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More')); loadMoreButton && loadMoreButton.click();"
],
"wait\_for"
:
"article.tease-card:nth-child(10)"
}
AI-Powered Extraction (Full Version)
request
=
{
"urls"
:
"https://www.nbcnews.com/business"
,
"extraction\_config"
:
{
"type"
:
"cosine"
,
"params"
:
{
"semantic\_filter"
:
"business finance economy"
,
"word\_count\_threshold"
:
10
,
"max\_dist"
:
0.2
,
"top\_k"
:
3
}
}
}
Platform-Specific Instructions 💻
macOS
docker
pull
unclecode/crawl4ai:basic
docker
run
-p
11235
:11235
unclecode/crawl4ai:basic
Ubuntu
# Basic version
docker
pull
unclecode/crawl4ai:basic
docker
run
-p
11235
:11235
unclecode/crawl4ai:basic
# With GPU support
docker
pull
unclecode/crawl4ai:gpu
docker
run
--gpus
all
-p
11235
:11235
unclecode/crawl4ai:gpu
Windows (PowerShell)
docker
pull
unclecode
/
crawl4ai
:
basic
docker
run
-p
11235
:
11235
unclecode
/
crawl4ai
:
basic
Testing 🧪
Save this as
test\_docker.py
:
import
requests
import
json
import
time
import
sys
class
Crawl4AiTester
:
def
\_\_init\_\_
(
self
,
base\_url
:
str
=
"http://localhost:11235"
):
self
.
base\_url
=
base\_url
def
submit\_and\_wait
(
self
,
request\_data
:
dict
,
timeout
:
int
=
300
)
->
dict
:
# Submit crawl job
response
=
requests
.
post
(
f
"
{
self
.
base\_url
}
/crawl"
,
json
=
request\_data
)
task\_id
=
response
.
json
()[
"task\_id"
]
print
(
f
"Task ID:
{
task\_id
}
"
)
# Poll for result
start\_time
=
time
.
time
()
while
True
:
if
time
.
time
()
-
start\_time
>
timeout
:
raise
TimeoutError
(
f
"Task
{
task\_id
}
timeout"
)
result
=
requests
.
get
(
f
"
{
self
.
base\_url
}
/task/
{
task\_id
}
"
)
status
=
result
.
json
()
if
status
[
"status"
]
==
"completed"
:
return
status
time
.
sleep
(
2
)
def
test\_deployment
():
tester
=
Crawl4AiTester
()
# Test basic crawl
request
=
{
"urls"
:
"https://www.nbcnews.com/business"
,
"priority"
:
10
}
result
=
tester
.
submit\_and\_wait
(
request
)
print
(
"Basic crawl successful!"
)
print
(
f
"Content length:
{
len
(
result
[
'result'
][
'markdown'
])
}
"
)
if
\_\_name\_\_
==
"\_\_main\_\_"
:
test\_deployment
()
Advanced Configuration ⚙️
Crawler Parameters
The
crawler\_params
field allows you to configure the browser instance and crawling behavior. Here are key parameters you can use:
request
=
{
"urls"
:
"https://example.com"
,
"crawler\_params"
:
{
# Browser Configuration
"headless"
:
True
,
# Run in headless mode
"browser\_type"
:
"chromium"
,
# chromium/firefox/webkit
"user\_agent"
:
"custom-agent"
,
# Custom user agent
"proxy"
:
"http://proxy:8080"
,
# Proxy configuration
# Performance & Behavior
"page\_timeout"
:
30000
,
# Page load timeout (ms)
"verbose"
:
True
,
# Enable detailed logging
"semaphore\_count"
:
5
,
# Concurrent request limit
# Anti-Detection Features
"simulate\_user"
:
True
,
# Simulate human behavior
"magic"
:
True
,
# Advanced anti-detection
"override\_navigator"
:
True
,
# Override navigator properties
# Session Management
"user\_data\_dir"
:
"./browser-data"
,
# Browser profile location
"use\_managed\_browser"
:
True
,
# Use persistent browser
}
}
Extra Parameters
The
extra
field allows passing additional parameters directly to the crawler's
arun
function:
request
=
{
"urls"
:
"https://example.com"
,
"extra"
:
{
"word\_count\_threshold"
:
10
,
# Min words per block
"only\_text"
:
True
,
# Extract only text
"bypass\_cache"
:
True
,
# Force fresh crawl
"process\_iframes"
:
True
,
# Include iframe content
}
}
Complete Examples
1.
Advanced News Crawling
request
=
{
"urls"
:
"https://www.nbcnews.com/business"
,
"crawler\_params"
:
{
"headless"
:
True
,
"page\_timeout"
:
30000
,
"remove\_overlay\_elements"
:
True
# Remove popups
},
"extra"
:
{
"word\_count\_threshold"
:
50
,
# Longer content blocks
"bypass\_cache"
:
True
# Fresh content
},
"css\_selector"
:
".article-body"
}
2.
Anti-Detection Configuration
request
=
{
"urls"
:
"https://example.com"
,
"crawler\_params"
:
{
"simulate\_user"
:
True
,
"magic"
:
True
,
"override\_navigator"
:
True
,
"user\_agent"
:
"Mozilla/5.0 ..."
,
"headers"
:
{
"Accept-Language"
:
"en-US,en;q=0.9"
}
}
}
3.
LLM Extraction with Custom Parameters
request
=
{
"urls"
:
"https://openai.com/pricing"
,
"extraction\_config"
:
{
"type"
:
"llm"
,
"params"
:
{
"provider"
:
"openai/gpt-4"
,
"schema"
:
pricing\_schema
}
},
"crawler\_params"
:
{
"verbose"
:
True
,
"page\_timeout"
:
60000
},
"extra"
:
{
"word\_count\_threshold"
:
1
,
"only\_text"
:
True
}
}
4.
Session-Based Dynamic Content
request
=
{
"urls"
:
"https://example.com"
,
"crawler\_params"
:
{
"session\_id"
:
"dynamic\_session"
,
"headless"
:
False
,
"page\_timeout"
:
60000
},
"js\_code"
:
[
"window.scrollTo(0, document.body.scrollHeight);"
],
"wait\_for"
:
"js:() => document.querySelectorAll('.item').length > 10"
,
"extra"
:
{
"delay\_before\_return\_html"
:
2.0
}
}
5.
Screenshot with Custom Timing
request
=
{
"urls"
:
"https://example.com"
,
"screenshot"
:
True
,
"crawler\_params"
:
{
"headless"
:
True
,
"screenshot\_wait\_for"
:
".main-content"
},
"extra"
:
{
"delay\_before\_return\_html"
:
3.0
}
}
Parameter Reference Table
Category
Parameter
Type
Description
Browser
headless
bool
Run browser in headless mode
Browser
browser\_type
str
Browser engine selection
Browser
user\_agent
str
Custom user agent string
Network
proxy
str
Proxy server URL
Network
headers
dict
Custom HTTP headers
Timing
page\_timeout
int
Page load timeout (ms)
Timing
delay\_before\_return\_html
float
Wait before capture
Anti-Detection
simulate\_user
bool
Human behavior simulation
Anti-Detection
magic
bool
Advanced protection
Session
session\_id
str
Browser session ID
Session
user\_data\_dir
str
Profile directory
Content
word\_count\_threshold
int
Minimum words per block
Content
only\_text
bool
Text-only extraction
Content
process\_iframes
bool
Include iframe content
Debug
verbose
bool
Detailed logging
Debug
log\_console
bool
Browser console logs
Troubleshooting 🔍
Common Issues
1.
Connection Refused
Error: Connection refused at localhost:11235
Solution: Ensure the container is running and ports are properly mapped.
2.
Resource Limits
Error: No available slots
Solution: Increase MAX\_CONCURRENT\_TASKS or container resources.
3.
GPU Access
Error: GPU not found
Solution: Ensure proper NVIDIA drivers and use
--gpus all
flag.
Debug Mode
Access container for debugging:
docker
run
-it
--entrypoint
/bin/bash
unclecode/crawl4ai:all
View container logs:
docker
logs
[
container\_id
]
Best Practices 🌟
1.
Resource Management
- Set appropriate memory and CPU limits
- Monitor resource usage via health endpoint
- Use basic version for simple crawling tasks
2.
Scaling
- Use multiple containers for high load
- Implement proper load balancing
- Monitor performance metrics
3.
Security
- Use environment variables for sensitive data
- Implement proper network isolation
- Regular security updates
API Reference 📚
Health Check
GET /health
Submit Crawl Task
POST /crawl
Content-Type: application/json
{
"urls": "string or array",
"extraction\_config": {
"type": "basic|llm|cosine|json\_css",
"params": {}
},
"priority": 1-10,
"ttl": 3600
}
Get Task Status
GET /task/{task\_id}
For more details, visit the
official documentation
.
Search
Type to start searching