SSL Certificate - Crawl4AI Documentation (v0.4.3bx)
SSLCertificate
Reference
The
SSLCertificate
class encapsulates an SSL certificate’s data and allows exporting it in various formats (PEM, DER, JSON, or text). It’s used within
Crawl4AI
whenever you set
fetch\_ssl\_certificate=True
in your
CrawlerRunConfig
.
1. Overview
Location
:
crawl4ai/ssl\_certificate.py
class
SSLCertificate
:
"""
Represents an SSL certificate with methods to export in various formats.
Main Methods:
- from\_url(url, timeout=10)
- from\_file(file\_path)
- from\_binary(binary\_data)
- to\_json(filepath=None)
- to\_pem(filepath=None)
- to\_der(filepath=None)
...
Common Properties:
- issuer
- subject
- valid\_from
- valid\_until
- fingerprint
"""
Typical Use Case
You
enable
certificate fetching in your crawl by:
CrawlerRunConfig
(
fetch\_ssl\_certificate
=
True
,
...
)
After
arun()
, if
result.ssl\_certificate
is present, it’s an instance of
SSLCertificate
.
You can
read
basic properties (issuer, subject, validity) or
export
them in multiple formats.
2. Construction & Fetching
2.1
from\_url(url, timeout=10)
Manually load an SSL certificate from a given URL (port 443). Typically used internally, but you can call it directly if you want:
cert
=
SSLCertificate
.
from\_url
(
"https://example.com"
)
if
cert
:
print
(
"Fingerprint:"
,
cert
.
fingerprint
)
2.2
from\_file(file\_path)
Load from a file containing certificate data in ASN.1 or DER. Rarely needed unless you have local cert files:
cert
=
SSLCertificate
.
from\_file
(
"/path/to/cert.der"
)
2.3
from\_binary(binary\_data)
Initialize from raw binary. E.g., if you captured it from a socket or another source:
cert
=
SSLCertificate
.
from\_binary
(
raw\_bytes
)
3. Common Properties
After obtaining a
SSLCertificate
instance (e.g.
result.ssl\_certificate
from a crawl), you can read:
1.
issuer
(dict)
- E.g.
{"CN": "My Root CA", "O": "..."}
2.
subject
(dict)
- E.g.
{"CN": "example.com", "O": "ExampleOrg"}
3.
valid\_from
(str)
- NotBefore date/time. Often in ASN.1/UTC format.
4.
valid\_until
(str)
- NotAfter date/time.
5.
fingerprint
(str)
- The SHA-256 digest (lowercase hex).
- E.g.
"d14d2e..."
4. Export Methods
Once you have a
SSLCertificate
object, you can
export
or
inspect
it:
4.1
to\_json(filepath=None)
→
Optional[str]
Returns a JSON string containing the parsed certificate fields.
If
filepath
is provided, saves it to disk instead, returning
None
.
Usage
:
json\_data
=
cert
.
to\_json
()
# returns JSON string
cert
.
to\_json
(
"certificate.json"
)
# writes file, returns None
4.2
to\_pem(filepath=None)
→
Optional[str]
Returns a PEM-encoded string (common for web servers).
If
filepath
is provided, saves it to disk instead.
pem\_str
=
cert
.
to\_pem
()
# in-memory PEM string
cert
.
to\_pem
(
"/path/to/cert.pem"
)
# saved to file
4.3
to\_der(filepath=None)
→
Optional[bytes]
Returns the original DER (binary ASN.1) bytes.
If
filepath
is specified, writes the bytes there instead.
der\_bytes
=
cert
.
to\_der
()
cert
.
to\_der
(
"certificate.der"
)
4.4 (Optional)
export\_as\_text()
If you see a method like
export\_as\_text()
, it typically returns an OpenSSL-style textual representation.
Not always needed, but can help for debugging or manual inspection.
5. Example Usage in Crawl4AI
Below is a minimal sample showing how the crawler obtains an SSL cert from a site, then reads or exports it. The code snippet:
import
asyncio
import
os
from
crawl4ai
import
AsyncWebCrawler
,
CrawlerRunConfig
,
CacheMode
async
def
main
():
tmp\_dir
=
"tmp"
os
.
makedirs
(
tmp\_dir
,
exist\_ok
=
True
)
config
=
CrawlerRunConfig
(
fetch\_ssl\_certificate
=
True
,
cache\_mode
=
CacheMode
.
BYPASS
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
"https://example.com"
,
config
=
config
)
if
result
.
success
and
result
.
ssl\_certificate
:
cert
=
result
.
ssl\_certificate
# 1. Basic Info
print
(
"Issuer CN:"
,
cert
.
issuer
.
get
(
"CN"
,
""
))
print
(
"Valid until:"
,
cert
.
valid\_until
)
print
(
"Fingerprint:"
,
cert
.
fingerprint
)
# 2. Export
cert
.
to\_json
(
os
.
path
.
join
(
tmp\_dir
,
"certificate.json"
))
cert
.
to\_pem
(
os
.
path
.
join
(
tmp\_dir
,
"certificate.pem"
))
cert
.
to\_der
(
os
.
path
.
join
(
tmp\_dir
,
"certificate.der"
))
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
6. Notes & Best Practices
1.
Timeout
:
SSLCertificate.from\_url
internally uses a default
10s
socket connect and wraps SSL.
2.
Binary Form
: The certificate is loaded in ASN.1 (DER) form, then re-parsed by
OpenSSL.crypto
.
3.
Validation
: This does
not
validate the certificate chain or trust store. It only fetches and parses.
4.
Integration
: Within Crawl4AI, you typically just set
fetch\_ssl\_certificate=True
in
CrawlerRunConfig
; the final result’s
ssl\_certificate
is automatically built.
5.
Export
: If you need to store or analyze a cert, the
to\_json
and
to\_pem
are quite universal.
Summary
SSLCertificate
is a convenience class for capturing and exporting the
TLS certificate
from your crawled site(s).
Common usage is in the
CrawlResult.ssl\_certificate
field, accessible after setting
fetch\_ssl\_certificate=True
.
Offers quick access to essential certificate details (
issuer
,
subject
,
fingerprint
) and is easy to export (PEM, DER, JSON) for further analysis or server usage.
Use it whenever you need
insight
into a site’s certificate or require some form of cryptographic or compliance check.
Search
Type to start searching