---
tags: [utility, amazon, MWS, SP-API, API, python]
---

### 1. Using the Amazon MWS and SP-API
Amazon provides the Marketplace Web Service (MWS) and the Selling Partner API (SP-API) which allow you to access various functionalities related to Seller Central. These APIs provide endpoints for managing orders, inventory, reports, and more, but not specifically for documentation. However, you can leverage these APIs to streamline and automate many Seller Central tasks, which can help you understand the operations better.

#### Getting Started with Amazon SP-API
1. **Register as a Developer**: Create a developer account in Amazon Seller Central.
2. **Create and Configure IAM Policies**: Set up the necessary IAM roles and policies in AWS to allow access to the SP-API.
3. **Generate API Keys**: Generate the necessary API keys and tokens for authentication.

#### Sample API Call using SP-API
Here is an example of how to make a call to the SP-API using Python:

```python
import requests
import datetime
import boto3
from requests.auth import AWS4Auth

# AWS Credentials
access_id = 'YOUR_ACCESS_ID'
secret_key = 'YOUR_SECRET_KEY'
region = 'us-west-2'
service = 'execute-api'

# Generate AWS Signature
session = boto3.Session(aws_access_key_id=access_id, aws_secret_access_key=secret_key, region_name=region)
credentials = session.get_credentials()
auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Endpoint and parameters
endpoint = 'https://sellingpartnerapi-na.amazon.com/orders/v0/orders'
params = {
    'MarketplaceIds': 'ATVPDKIKX0DER',  # Example marketplace ID for Amazon.com
    'CreatedAfter': datetime.datetime.now().isoformat()
}

# Make the API request
response = requests.get(endpoint, params=params, auth=auth)
print(response.json())
```