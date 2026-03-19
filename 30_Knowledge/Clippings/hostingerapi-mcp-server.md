---
title: "hostinger/api-mcp-server"
source: "https://github.com/hostinger/api-mcp-server"
author:
  - "[[laurynasgadl]]"
published:
created: 2026-01-27
description: "Contribute to hostinger/api-mcp-server development by creating an account on GitHub."
tags:
  - "clippings"
---
Model Context Protocol (MCP) server for Hostinger API.

## Prerequisites- Node.js version 24 or higher

If you don't have Node.js installed, you can download it from the [official website](https://nodejs.org/en/download/). Alternatively, you can use a package manager like [Homebrew](https://brew.sh/) (for macOS) or [Chocolatey](https://chocolatey.org/) (for Windows) to install Node.js.

We recommend using [NVM (Node Version Manager)](https://github.com/nvm-sh/nvm) to install and manage installed Node.js versions. After installing NVM, you can install Node.js with the following command:

nvm install v24
nvm use v24

## InstallationTo install the MCP server, run one of the following command, depending on your package manager:

# Install globally from npm
npm install -g hostinger-api-mcp

# Or with yarn
yarn global add hostinger-api-mcp

# Or with pnpm
pnpm add -g hostinger-api-mcp

## UpdateTo update the MCP server to the latest version, use one of the following commands, depending on your package manager:

# Update globally from npm
npm update -g hostinger-api-mcp

# Or with yarn
yarn global upgrade hostinger-api-mcp

# Or with pnpm
pnpm update -g hostinger-api-mcp

## ConfigurationThe following environment variables can be configured when running the server:

- `DEBUG`: Enable debug logging (true/false) (default: false)
- `API_TOKEN`: Your API token, which will be sent in the `Authorization` header.

## Usage### JSON configuration for Claude, Cursor, etc.{
    "mcpServers": {
        "hostinger-api": {
            "command": "hostinger-api-mcp",
            "env": {
                "DEBUG": "false",
                "API\_TOKEN": "YOUR API TOKEN"
            }
        }
    }
}

### Transport OptionsThe MCP server supports two transport modes:

#### Standard I/O TransportThe server can use standard input / output (stdio) transport (default). This provides local streaming:

#### Streamable HTTP TransportThe server can use HTTP streaming transport. This provides bidirectional streaming over HTTP:

# Default HTTP transport on localhost:8100
hostinger-api-mcp --http

# Specify custom host and port
hostinger-api-mcp --http --host 0.0.0.0 --port 8150

#### Command Line Options```
Options:
  --http           Use HTTP streaming transport
  --stdio          Use Server-Sent Events transport (default)
  --host {host}    Hostname or IP address to listen on (default: 127.0.0.1)
  --port {port}    Port to bind to (default: 8100)
  --help           Show help message
```

### Using as an MCP Tool ProviderThis server implements the Model Context Protocol (MCP) and can be used with any MCP-compatible consumer.

Example of connecting to this server using HTTP streaming transport:

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

// Create HTTP transport
const transport \= new StreamableHTTPClientTransport({
  url: "http://localhost:8100/",
  headers: {
    "Authorization": \`Bearer ${process.env.API\_TOKEN}\`
  }
});

// Connect to the MCP server
const client \= new Client({
  name: "my-client",
  version: "1.0.0"
}, {
  capabilities: {}
});

await client.connect(transport);

// List available tools
const { tools } \= await client.listTools();
console.log("Available tools:", tools);

// Call a tool
const result \= await client.callTool({
  name: "billing\_getCatalogItemListV1",
  arguments: { category: "DOMAIN" }
});
console.log("Tool result:", result);

## Available ToolsThis MCP server provides the following tools:

### hosting\_importWordpressWebsiteImport a WordPress website from an archive file to a hosting server. This tool uploads a website archive (zip, tar, tar.gz, etc.) and a database dump (.sql file) to deploy a complete WordPress website. The archive will be extracted on the server automatically. Note: This process may take a while for larger sites. After upload completion, files are being extracted and the site will be available in a few minutes. The username will be automatically resolved from the domain.

- **Method**: \`\`
- **Path**: \`\`

**Parameters**:

- `domain`: Domain name associated with the hosting account (e.g., example.com) (required)
- `archivePath`: Absolute or relative path to the website archive file. Supported formats: zip, tar, tar.gz, tgz, 7z, gz, gzip. If user provides directory path, create archive from it before proceeding using EXACTLY this naming pattern: directoryname\_YYYYMMDD\_HHMMSS.zip (e.g., mywebsite\_20250115\_143022.zip) (required)
- `databaseDump`: Absolute or relative path to a database dump file (.sql) (required)

### hosting\_deployWordpressPluginDeploy a WordPress plugin from a directory to a hosting server. This tool uploads all plugin files and triggers plugin deployment.

- **Method**: \`\`
- **Path**: \`\`

**Parameters**:

- `domain`: Domain name associated with the hosting account (e.g., example.com) (required)
- `slug`: WordPress plugin slug (e.g., omnisend) (required)
- `pluginPath`: Absolute or relative path to the plugin directory containing all plugin files (required)

### hosting\_deployWordpressThemeDeploy a WordPress theme from a directory to a hosting server. This tool uploads all theme files and triggers theme deployment. The uploaded theme can optionally be activated after deployment.

- **Method**: \`\`
- **Path**: \`\`

**Parameters**:

- `domain`: Domain name associated with the hosting account (e.g., example.com) (required)
- `slug`: WordPress theme slug (e.g., twentytwentyfive) (required)
- `themePath`: Absolute or relative path to the theme directory containing all theme files (required)
- `activate`: Whether to activate the theme after deployment (default: false)

### hosting\_deployJsApplicationDeploy a JavaScript application from an archive file to a hosting server. IMPORTANT: the archive must ONLY contain application source files, not the build output, skip node\_modules directory; also exclude all files matched by .gitignore if the ignore file exists. The build process will be triggered automatically on the server after the archive is uploaded. After deployment, use the hosting\_listJsDeployments tool to check deployment status and track build progress.

- **Method**: \`\`
- **Path**: \`\`

**Parameters**:

- `domain`: Domain name associated with the hosting account (e.g., example.com) (required)
- `archivePath`: Absolute or relative path to the application archive file. Supported formats: zip, tar, tar.gz, tgz, 7z, gz, gzip. If user provides directory path, create archive from it before proceeding. IMPORTANT: the archive must ONLY contain application source files, not the build output, skip node\_modules directory. (required)
- `removeArchive`: Whether to remove the archive file after successful deployment (default: false)

### hosting\_deployStaticWebsiteDeploy a static website from an archive file to a hosting server. IMPORTANT: This tool only works for static websites with no build process. The archive must contain pre-built static files (HTML, CSS, JavaScript, images, etc.) ready to be served. If the website has a package.json file or requires a build command, use hosting\_deployJsApplication instead. The archive will be extracted and deployed directly without any build steps. The username will be automatically resolved from the domain.

- **Method**: \`\`
- **Path**: \`\`

**Parameters**:

- `domain`: Domain name associated with the hosting account (e.g., example.com) (required)
- `archivePath`: Absolute or relative path to the static website archive file. Supported formats: zip, tar, tar.gz, tgz, 7z, gz, gzip. If user provides directory path, create archive from it before proceeding using EXACTLY this naming pattern: directoryname\_YYYYMMDD\_HHMMSS.zip (e.g., mystaticwebsite\_20250115\_143022.zip) (required)
- `removeArchive`: Whether to remove the archive file after successful deployment (default: false)

### hosting\_listJsDeploymentsList javascript application deployments for checking their status. Use this tool when customer asks for the status of the deployment. This tool retrieves a paginated list of Node.js application deployments for a domain with optional filtering by deployment states.

- **Method**: \`\`
- **Path**: \`\`

**Parameters**:

- `domain`: Domain name associated with the hosting account (e.g., example.com) (required)
- `page`: Page number for pagination (optional)
- `perPage`: Number of items per page (optional)
- `states`: Filter by deployment states (optional). Valid values: pending, completed, running, failed

### hosting\_showJsDeploymentLogsRetrieve logs for a specified JavaScript application deployment for debugging purposes in case of failure.

- **Method**: \`\`
- **Path**: \`\`

**Parameters**:

- `domain`: Domain name associated with the hosting account (e.g., example.com) (required)
- `fromLine`: Line from which to retrieve logs (optional, default 0)
- `buildUuid`: UUID of the JavaScript deployment build (required)

### billing\_getCatalogItemListV1Retrieve catalog items available for order.

Prices in catalog items is displayed as cents (without floating point), e.g: float `17.99` is displayed as integer `1799`.

Use this endpoint to view available services and pricing before placing orders.

- **Method**: `GET`
- **Path**: `/api/billing/v1/catalog`

**Parameters**:

- `category`: Filter catalog items by category
- `name`: Filter catalog items by name. Use `*` for wildcard search, e.g. `.COM*` to find .com domain

### billing\_createServiceOrderV1Create a new service order.

**DEPRECATED**

To purchase a domain, use [`POST /api/domains/v1/portfolio`](https://github.com/hostinger/api-mcp-server/blob/main/#tag/domains-portfolio/POST/api/domains/v1/portfolio) instead.

To purchase a VPS, use [`POST /api/vps/v1/virtual-machines`](https://github.com/hostinger/api-mcp-server/blob/main/#tag/vps-virtual-machine/POST/api/vps/v1/virtual-machines) instead.

To place order, you need to provide payment method ID and list of price items from the catalog endpoint together with quantity. Coupons also can be provided during order creation.

Orders created using this endpoint will be set for automatic renewal.

Some `credit_card` payments might need additional verification, rendering purchase unprocessed. We recommend use other payment methods than `credit_card` if you encounter this issue.

- **Method**: `POST`
- **Path**: `/api/billing/v1/orders`

**Parameters**:

- `payment_method_id`: Payment method ID (required)
- `items`: items parameter (required)
- `coupons`: Discount coupon codes

### billing\_setDefaultPaymentMethodV1Set the default payment method for your account.

Use this endpoint to configure the primary payment method for future orders.

- **Method**: `POST`
- **Path**: `/api/billing/v1/payment-methods/{paymentMethodId}`

**Parameters**:

- `paymentMethodId`: Payment method ID (required)

### billing\_deletePaymentMethodV1Delete a payment method from your account.

Use this endpoint to remove unused payment methods from user accounts.

- **Method**: `DELETE`
- **Path**: `/api/billing/v1/payment-methods/{paymentMethodId}`

**Parameters**:

- `paymentMethodId`: Payment method ID (required)

### billing\_getPaymentMethodListV1Retrieve available payment methods that can be used for placing new orders.

If you want to add new payment method, please use [hPanel](https://hpanel.hostinger.com/billing/payment-methods).

Use this endpoint to view available payment options before creating orders.

- **Method**: `GET`
- **Path**: `/api/billing/v1/payment-methods`

### billing\_cancelSubscriptionV1Cancel a subscription and stop any further billing.

Use this endpoint when users want to terminate active services.

- **Method**: `DELETE`
- **Path**: `/api/billing/v1/subscriptions/{subscriptionId}`

**Parameters**:

- `subscriptionId`: Subscription ID (required)

### billing\_getSubscriptionListV1Retrieve a list of all subscriptions associated with your account.

Use this endpoint to monitor active services and billing status.

- **Method**: `GET`
- **Path**: `/api/billing/v1/subscriptions`

### billing\_disableAutoRenewalV1Disable auto-renewal for a subscription.

Use this endpoint when disable auto-renewal for a subscription.

- **Method**: `DELETE`
- **Path**: `/api/billing/v1/subscriptions/{subscriptionId}/auto-renewal/disable`

**Parameters**:

- `subscriptionId`: Subscription ID (required)

### billing\_enableAutoRenewalV1Enable auto-renewal for a subscription.

Use this endpoint when enable auto-renewal for a subscription.

- **Method**: `PATCH`
- **Path**: `/api/billing/v1/subscriptions/{subscriptionId}/auto-renewal/enable`

**Parameters**:

- `subscriptionId`: Subscription ID (required)

### DNS\_getDNSSnapshotV1Retrieve particular DNS snapshot with contents of DNS zone records.

Use this endpoint to view historical DNS configurations for domains.

- **Method**: `GET`
- **Path**: `/api/dns/v1/snapshots/{domain}/{snapshotId}`

**Parameters**:

- `domain`: Domain name (required)
- `snapshotId`: Snapshot ID (required)

### DNS\_getDNSSnapshotListV1Retrieve DNS snapshots for a domain.

Use this endpoint to view available DNS backup points for restoration.

- **Method**: `GET`
- **Path**: `/api/dns/v1/snapshots/{domain}`

**Parameters**:

- `domain`: Domain name (required)

### DNS\_restoreDNSSnapshotV1Restore DNS zone to the selected snapshot.

Use this endpoint to revert domain DNS to a previous configuration.

- **Method**: `POST`
- **Path**: `/api/dns/v1/snapshots/{domain}/{snapshotId}/restore`

**Parameters**:

- `domain`: Domain name (required)
- `snapshotId`: Snapshot ID (required)

### DNS\_getDNSRecordsV1Retrieve DNS zone records for a specific domain.

Use this endpoint to view current DNS configuration for domain management.

- **Method**: `GET`
- **Path**: `/api/dns/v1/zones/{domain}`

**Parameters**:

- `domain`: Domain name (required)

### DNS\_updateDNSRecordsV1Update DNS records for the selected domain.

Using `overwrite = true` will replace existing records with the provided ones. Otherwise existing records will be updated and new records will be added.

Use this endpoint to modify domain DNS configuration.

- **Method**: `PUT`
- **Path**: `/api/dns/v1/zones/{domain}`

**Parameters**:

- `domain`: Domain name (required)
- `overwrite`: If `true`, resource records (RRs) matching name and type will be deleted and new RRs will be created, otherwise resource records' ttl's are updated and new records are appended. If no matching RRs are found, they are created.
- `zone`: zone parameter (required)

### DNS\_deleteDNSRecordsV1Delete DNS records for the selected domain.

To filter which records to delete, add the `name` of the record and `type` to the filter. Multiple filters can be provided with single request.

If you have multiple records with the same name and type, and you want to delete only part of them, refer to the `Update zone records` endpoint.

Use this endpoint to remove specific DNS records from domains.

- **Method**: `DELETE`
- **Path**: `/api/dns/v1/zones/{domain}`

**Parameters**:

- `domain`: Domain name (required)

### DNS\_resetDNSRecordsV1Reset DNS zone to the default records.

Use this endpoint to restore domain DNS to original configuration.

- **Method**: `POST`
- **Path**: `/api/dns/v1/zones/{domain}/reset`

**Parameters**:

- `domain`: Domain name (required)
- `sync`: Determines if operation should be run synchronously
- `reset_email_records`: Determines if email records should be reset
- `whitelisted_record_types`: Specifies which record types to not reset

### DNS\_validateDNSRecordsV1Validate DNS records prior to update for the selected domain.

If the validation is successful, the response will contain `200 Success` code. If there is validation error, the response will fail with `422 Validation error` code.

Use this endpoint to verify DNS record validity before applying changes.

- **Method**: `POST`
- **Path**: `/api/dns/v1/zones/{domain}/validate`

**Parameters**:

- `domain`: Domain name (required)
- `overwrite`: If `true`, resource records (RRs) matching name and type will be deleted and new RRs will be created, otherwise resource records' ttl's are updated and new records are appended. If no matching RRs are found, they are created.
- `zone`: zone parameter (required)

### v2\_getDomainVerificationsDIRECTRetrieve a list of pending and completed domain verifications.

- **Method**: `GET`
- **Path**: `/api/v2/direct/verifications/active`

### domains\_checkDomainAvailabilityV1Check availability of domain names across multiple TLDs.

Multiple TLDs can be checked at once. If you want alternative domains with response, provide only one TLD and set `with_alternatives` to `true`. TLDs should be provided without leading dot (e.g. `com`, `net`, `org`).

Endpoint has rate limit of 10 requests per minute.

Use this endpoint to verify domain availability before purchase.

- **Method**: `POST`
- **Path**: `/api/domains/v1/availability`

**Parameters**:

- `domain`: Domain name (without TLD) (required)
- `tlds`: TLDs list (required)
- `with_alternatives`: Should response include alternatives

### domains\_getDomainForwardingV1Retrieve domain forwarding data.

Use this endpoint to view current redirect configuration for domains.

- **Method**: `GET`
- **Path**: `/api/domains/v1/forwarding/{domain}`

**Parameters**:

- `domain`: Domain name (required)

### domains\_deleteDomainForwardingV1Delete domain forwarding data.

Use this endpoint to remove redirect configuration from domains.

- **Method**: `DELETE`
- **Path**: `/api/domains/v1/forwarding/{domain}`

**Parameters**:

- `domain`: Domain name (required)

### domains\_createDomainForwardingV1Create domain forwarding configuration.

Use this endpoint to set up domain redirects to other URLs.

- **Method**: `POST`
- **Path**: `/api/domains/v1/forwarding`

**Parameters**:

- `domain`: Domain name (required)
- `redirect_type`: Redirect type (required)
- `redirect_url`: URL to forward domain to (required)

### domains\_enableDomainLockV1Enable domain lock for the domain.

When domain lock is enabled, the domain cannot be transferred to another registrar without first disabling the lock.

Use this endpoint to secure domains against unauthorized transfers.

- **Method**: `PUT`
- **Path**: `/api/domains/v1/portfolio/{domain}/domain-lock`

**Parameters**:

- `domain`: Domain name (required)

### domains\_disableDomainLockV1Disable domain lock for the domain.

Domain lock needs to be disabled before transferring the domain to another registrar.

Use this endpoint to prepare domains for transfer to other registrars.

- **Method**: `DELETE`
- **Path**: `/api/domains/v1/portfolio/{domain}/domain-lock`

**Parameters**:

- `domain`: Domain name (required)

### domains\_getDomainDetailsV1Retrieve detailed information for specified domain.

Use this endpoint to view comprehensive domain configuration and status.

- **Method**: `GET`
- **Path**: `/api/domains/v1/portfolio/{domain}`

**Parameters**:

- `domain`: Domain name (required)

### domains\_getDomainListV1Retrieve all domains associated with your account.

Use this endpoint to view user's domain portfolio.

- **Method**: `GET`
- **Path**: `/api/domains/v1/portfolio`

### domains\_purchaseNewDomainV1Purchase and register a new domain name.

If registration fails, login to [hPanel](https://hpanel.hostinger.com/) and check domain registration status.

If no payment method is provided, your default payment method will be used automatically.

If no WHOIS information is provided, default contact information for that TLD will be used. Before making request, ensure WHOIS information for desired TLD exists in your account.

Some TLDs require `additional_details` to be provided and these will be validated before completing purchase.

Use this endpoint to register new domains for users.

- **Method**: `POST`
- **Path**: `/api/domains/v1/portfolio`

**Parameters**:

- `domain`: Domain name (required)
- `item_id`: Catalog price item ID (required)
- `payment_method_id`: Payment method ID, default will be used if not provided
- `domain_contacts`: Domain contact information
- `additional_details`: Additional registration data, possible values depends on TLD
- `coupons`: Discount coupon codes

### domains\_enablePrivacyProtectionV1Enable privacy protection for the domain.

When privacy protection is enabled, domain owner's personal information is hidden from public WHOIS database.

Use this endpoint to protect domain owner's personal information from public view.

- **Method**: `PUT`
- **Path**: `/api/domains/v1/portfolio/{domain}/privacy-protection`

**Parameters**:

- `domain`: Domain name (required)

### domains\_disablePrivacyProtectionV1Disable privacy protection for the domain.

When privacy protection is disabled, domain owner's personal information is visible in public WHOIS database.

Use this endpoint to make domain owner's information publicly visible.

- **Method**: `DELETE`
- **Path**: `/api/domains/v1/portfolio/{domain}/privacy-protection`

**Parameters**:

- `domain`: Domain name (required)

### domains\_updateDomainNameserversV1Set nameservers for a specified domain.

Be aware, that improper nameserver configuration can lead to the domain being unresolvable or unavailable.

Use this endpoint to configure custom DNS hosting for domains.

- **Method**: `PUT`
- **Path**: `/api/domains/v1/portfolio/{domain}/nameservers`

**Parameters**:

- `domain`: Domain name (required)
- `ns1`: First name server (required)
- `ns2`: Second name server (required)
- `ns3`: Third name server
- `ns4`: Fourth name server

### domains\_getWHOISProfileV1Retrieve a WHOIS contact profile.

Use this endpoint to view domain registration contact information.

- **Method**: `GET`
- **Path**: `/api/domains/v1/whois/{whoisId}`

**Parameters**:

- `whoisId`: WHOIS ID (required)

### domains\_deleteWHOISProfileV1Delete WHOIS contact profile.

Use this endpoint to remove unused contact profiles from account.

- **Method**: `DELETE`
- **Path**: `/api/domains/v1/whois/{whoisId}`

**Parameters**:

- `whoisId`: WHOIS ID (required)

### domains\_getWHOISProfileListV1Retrieve WHOIS contact profiles.

Use this endpoint to view available contact profiles for domain registration.

- **Method**: `GET`
- **Path**: `/api/domains/v1/whois`

**Parameters**:

- `tld`: Filter by TLD (without leading dot)

### domains\_createWHOISProfileV1Create WHOIS contact profile.

Use this endpoint to add new contact information for domain registration.

- **Method**: `POST`
- **Path**: `/api/domains/v1/whois`

**Parameters**:

- `tld`: TLD of the domain (without leading dot) (required)
- `country`: ISO 3166 2-letter country code (required)
- `entity_type`: Legal entity type (required)
- `tld_details`: TLD details
- `whois_details`: WHOIS details (required)

### domains\_getWHOISProfileUsageV1Retrieve domain list where provided WHOIS contact profile is used.

Use this endpoint to view which domains use specific contact profiles.

- **Method**: `GET`
- **Path**: `/api/domains/v1/whois/{whoisId}/usage`

**Parameters**:

- `whoisId`: WHOIS ID (required)

### hosting\_listAvailableDatacentersV1Retrieve a list of datacenters available for setting up hosting plans based on available datacenter capacity and hosting plan of your order. The first item in the list is the best match for your specific order requirements.

- **Method**: `GET`
- **Path**: `/api/hosting/v1/datacenters`

**Parameters**:

- `order_id`: Order ID (required)

### hosting\_generateAFreeSubdomainV1Generate a unique free subdomain that can be used for hosting services without purchasing custom domains. Free subdomains allow you to start using hosting services immediately and you can always connect a custom domain to your site later.

- **Method**: `POST`
- **Path**: `/api/hosting/v1/domains/free-subdomains`

### hosting\_verifyDomainOwnershipV1Verify ownership of a single domain and return the verification status.

Use this endpoint to check if a domain is accessible for you before using it for new websites. If the domain is accessible, the response will have `is_accessible: true`. If not, add the given TXT record to your domain's DNS records and try verifying again. Keep in mind that it may take up to 10 minutes for new TXT DNS records to propagate.

Skip this verification when using Hostinger's free subdomains (\*.hostingersite.com).

- **Method**: `POST`
- **Path**: `/api/hosting/v1/domains/verify-ownership`

**Parameters**:

- `domain`: Domain to verify ownership for (required)

### hosting\_listOrdersV1Retrieve a paginated list of orders accessible to the authenticated client.

This endpoint returns orders of your hosting accounts as well as orders of other client hosting accounts that have shared access with you.

Use the available query parameters to filter results by order statuses or specific order IDs for more targeted results.

- **Method**: `GET`
- **Path**: `/api/hosting/v1/orders`

**Parameters**:

- `page`: Page number
- `per_page`: Number of items per page
- `statuses`: Filter by order statuses
- `order_ids`: Filter by specific order IDs

### hosting\_listWebsitesV1Retrieve a paginated list of websites (main and addon types) accessible to the authenticated client.

This endpoint returns websites from your hosting accounts as well as websites from other client hosting accounts that have shared access with you.

Use the available query parameters to filter results by username, order ID, enabled status, or domain name for more targeted results.

- **Method**: `GET`
- **Path**: `/api/hosting/v1/websites`

**Parameters**:

- `page`: Page number
- `per_page`: Number of items per page
- `username`: Filter by specific username
- `order_id`: Order ID
- `is_enabled`: Filter by enabled status
- `domain`: Filter by domain name (exact match)

### hosting\_createWebsiteV1Create a new website for the authenticated client.

Provide the domain name and associated order ID to create a new website. The datacenter\_code parameter is required when creating the first website on a new hosting plan - this will set up and configure new hosting account in the selected datacenter.

Subsequent websites will be hosted on the same datacenter automatically.

Website creation takes up to a few minutes to complete. Check the websites list endpoint to see when your new website becomes available.

- **Method**: `POST`
- **Path**: `/api/hosting/v1/websites`

**Parameters**:

- `domain`: Domain name for the website. Cannot start with "[www](http://www/)." (required)
- `order_id`: ID of the associated order (required)
- `datacenter_code`: Datacenter code. This parameter is required when creating the first website on a new hosting plan.

### reach\_deleteAContactV1Delete a contact with the specified UUID.

This endpoint permanently removes a contact from the email marketing system.

- **Method**: `DELETE`
- **Path**: `/api/reach/v1/contacts/{uuid}`

**Parameters**:

- `uuid`: UUID of the contact to delete (required)

### reach\_listContactGroupsV1Get a list of all contact groups.

This endpoint returns a list of contact groups that can be used to organize contacts.

- **Method**: `GET`
- **Path**: `/api/reach/v1/contacts/groups`

### reach\_listContactsV1Get a list of contacts, optionally filtered by group and subscription status.

This endpoint returns a paginated list of contacts with their basic information. You can filter contacts by group UUID and subscription status.

- **Method**: `GET`
- **Path**: `/api/reach/v1/contacts`

**Parameters**:

- `group_uuid`: Filter contacts by group UUID
- `subscription_status`: Filter contacts by subscription status
- `page`: Page number

### reach\_createANewContactV1Create a new contact in the email marketing system.

This endpoint allows you to create a new contact with basic information like name, email, and surname. You can optionally assign the contact to specific groups and add notes.

The contact will be automatically subscribed to email communications.

- **Method**: `POST`
- **Path**: `/api/reach/v1/contacts`

**Parameters**:

- `email`: email parameter (required)
- `name`: name parameter
- `surname`: surname parameter
- `note`: note parameter

### reach\_listSegmentsV1Get a list of all contact segments.

This endpoint returns a list of contact segments that can be used to organize contacts.

- **Method**: `GET`
- **Path**: `/api/reach/v1/segmentation/segments`

### reach\_createANewContactSegmentV1Create a new contact segment.

This endpoint allows creating a new contact segment that can be used to organize contacts. The segment can be configured with specific criteria like email, name, subscription status, etc.

- **Method**: `POST`
- **Path**: `/api/reach/v1/segmentation/segments`

**Parameters**:

- `name`: name parameter (required)
- `conditions`: conditions parameter (required)
- `logic`: logic parameter (required)

### reach\_listSegmentContactsV1Retrieve contacts associated with a specific segment.

This endpoint allows you to fetch and filter contacts that belong to a particular segment, identified by its UUID.

- **Method**: `GET`
- **Path**: `/api/reach/v1/segmentation/segments/{segmentUuid}/contacts`

**Parameters**:

- `segmentUuid`: Segment uuid parameter (required)
- `page`: Page number
- `per_page`: Number of items per page

### reach\_getSegmentDetailsV1Get details of a specific segment.

This endpoint retrieves information about a single segment identified by UUID. Segments are used to organize and group contacts based on specific criteria.

- **Method**: `GET`
- **Path**: `/api/reach/v1/segmentation/segments/{segmentUuid}`

**Parameters**:

- `segmentUuid`: Segment uuid parameter (required)

### VPS\_getDataCenterListV1Retrieve all available data centers.

Use this endpoint to view location options before deploying VPS instances.

- **Method**: `GET`
- **Path**: `/api/vps/v1/data-centers`

### VPS\_getProjectContainersV1Retrieves a list of all containers belonging to a specific Docker Compose project on the virtual machine.

This endpoint returns detailed information about each container including their current status, port mappings, and runtime configuration.

Use this to monitor the health and state of all services within your Docker Compose project.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}/containers`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_getProjectContentsV1Retrieves the complete project information including the docker-compose.yml file contents, project metadata, and current deployment status.

This endpoint provides the full configuration and state details of a specific Docker Compose project.

Use this to inspect project settings, review the compose file, or check the overall project health.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_deleteProjectV1Completely removes a Docker Compose project from the virtual machine, stopping all containers and cleaning up associated resources including networks, volumes, and images.

This operation is irreversible and will delete all project data.

Use this when you want to permanently remove a project and free up system resources.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}/down`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_getProjectListV1Retrieves a list of all Docker Compose projects currently deployed on the virtual machine.

This endpoint returns basic information about each project including name, status, file path and list of containers with details about their names, image, status, health and ports. Container stats are omitted in this endpoint. If you need to get detailed information about container with stats included, use the `Get project containers` endpoint.

Use this to get an overview of all Docker projects on your VPS instance.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_createNewProjectV1Deploy new project from docker-compose.yaml contents or download contents from URL.

URL can be Github repository url in format [https://github.com/\[user\]/\[repo\]](https://github.com/%5Buser%5D/%5Brepo%5D) and it will be automatically resolved to docker-compose.yaml file in master branch. Any other URL provided must return docker-compose.yaml file contents.

If project with the same name already exists, existing project will be replaced.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `project_name`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)
- `content`: URL pointing to docker-compose.yaml file, Github repository or raw YAML content of the compose file (required)
- `environment`: Project environment variables

### VPS\_getProjectLogsV1Retrieves aggregated log entries from all services within a Docker Compose project.

This endpoint returns recent log output from each container, organized by service name with timestamps. The response contains the last 300 log entries across all services.

Use this for debugging, monitoring application behavior, and troubleshooting issues across your entire project stack.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}/logs`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_restartProjectV1Restarts all services in a Docker Compose project by stopping and starting containers in the correct dependency order.

This operation preserves data volumes and network configurations while refreshing the running containers.

Use this to apply configuration changes or recover from service failures.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}/restart`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_startProjectV1Starts all services in a Docker Compose project that are currently stopped.

This operation brings up containers in the correct dependency order as defined in the compose file.

Use this to resume a project that was previously stopped or to start services after a system reboot.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}/start`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_stopProjectV1Stops all running services in a Docker Compose project while preserving container configurations and data volumes.

This operation gracefully shuts down containers in reverse dependency order.

Use this to temporarily halt a project without removing data or configurations.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}/stop`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_updateProjectV1Updates a Docker Compose project by pulling the latest image versions and recreating containers with new configurations.

This operation preserves data volumes while applying changes from the compose file.

Use this to deploy application updates, apply configuration changes, or refresh container images to their latest versions.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/docker/{projectName}/update`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `projectName`: Docker Compose project name using alphanumeric characters, dashes, and underscores only (required)

### VPS\_activateFirewallV1Activate a firewall for a specified virtual machine.

Only one firewall can be active for a virtual machine at a time.

Use this endpoint to apply firewall rules to VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/firewall/{firewallId}/activate/{virtualMachineId}`

**Parameters**:

- `firewallId`: Firewall ID (required)
- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_deactivateFirewallV1Deactivate a firewall for a specified virtual machine.

Use this endpoint to remove firewall protection from VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/firewall/{firewallId}/deactivate/{virtualMachineId}`

**Parameters**:

- `firewallId`: Firewall ID (required)
- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_getFirewallDetailsV1Retrieve firewall by its ID and rules associated with it.

Use this endpoint to view specific firewall configuration and rules.

- **Method**: `GET`
- **Path**: `/api/vps/v1/firewall/{firewallId}`

**Parameters**:

- `firewallId`: Firewall ID (required)

### VPS\_deleteFirewallV1Delete a specified firewall.

Any virtual machine that has this firewall activated will automatically have it deactivated.

Use this endpoint to remove unused firewall configurations.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/firewall/{firewallId}`

**Parameters**:

- `firewallId`: Firewall ID (required)

### VPS\_getFirewallListV1Retrieve all available firewalls.

Use this endpoint to view existing firewall configurations.

- **Method**: `GET`
- **Path**: `/api/vps/v1/firewall`

**Parameters**:

- `page`: Page number

### VPS\_createNewFirewallV1Create a new firewall.

Use this endpoint to set up new firewall configurations for VPS security.

- **Method**: `POST`
- **Path**: `/api/vps/v1/firewall`

**Parameters**:

- `name`: name parameter (required)

### VPS\_updateFirewallRuleV1Update a specific firewall rule from a specified firewall.

Any virtual machine that has this firewall activated will lose sync with the firewall and will have to be synced again manually.

Use this endpoint to modify existing firewall rules.

- **Method**: `PUT`
- **Path**: `/api/vps/v1/firewall/{firewallId}/rules/{ruleId}`

**Parameters**:

- `firewallId`: Firewall ID (required)
- `ruleId`: Firewall Rule ID (required)
- `protocol`: protocol parameter (required)
- `port`: Port or port range, ex: 1024:2048 (required)
- `source`: source parameter (required)
- `source_detail`: IP range, CIDR, single IP or `any` (required)

### VPS\_deleteFirewallRuleV1Delete a specific firewall rule from a specified firewall.

Any virtual machine that has this firewall activated will lose sync with the firewall and will have to be synced again manually.

Use this endpoint to remove specific firewall rules.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/firewall/{firewallId}/rules/{ruleId}`

**Parameters**:

- `firewallId`: Firewall ID (required)
- `ruleId`: Firewall Rule ID (required)

### VPS\_createFirewallRuleV1Create new firewall rule for a specified firewall.

By default, the firewall drops all incoming traffic, which means you must add accept rules for all ports you want to use.

Any virtual machine that has this firewall activated will lose sync with the firewall and will have to be synced again manually.

Use this endpoint to add new security rules to firewalls.

- **Method**: `POST`
- **Path**: `/api/vps/v1/firewall/{firewallId}/rules`

**Parameters**:

- `firewallId`: Firewall ID (required)
- `protocol`: protocol parameter (required)
- `port`: Port or port range, ex: 1024:2048 (required)
- `source`: source parameter (required)
- `source_detail`: IP range, CIDR, single IP or `any` (required)

### VPS\_syncFirewallV1Sync a firewall for a specified virtual machine.

Firewall can lose sync with virtual machine if the firewall has new rules added, removed or updated.

Use this endpoint to apply updated firewall rules to VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/firewall/{firewallId}/sync/{virtualMachineId}`

**Parameters**:

- `firewallId`: Firewall ID (required)
- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_getPostInstallScriptV1Retrieve post-install script by its ID.

Use this endpoint to view specific automation script details.

- **Method**: `GET`
- **Path**: `/api/vps/v1/post-install-scripts/{postInstallScriptId}`

**Parameters**:

- `postInstallScriptId`: Post-install script ID (required)

### VPS\_updatePostInstallScriptV1Update a specific post-install script.

Use this endpoint to modify existing automation scripts.

- **Method**: `PUT`
- **Path**: `/api/vps/v1/post-install-scripts/{postInstallScriptId}`

**Parameters**:

- `postInstallScriptId`: Post-install script ID (required)
- `name`: Name of the script (required)
- `content`: Content of the script (required)

### VPS\_deletePostInstallScriptV1Delete a post-install script from your account.

Use this endpoint to remove unused automation scripts.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/post-install-scripts/{postInstallScriptId}`

**Parameters**:

- `postInstallScriptId`: Post-install script ID (required)

### VPS\_getPostInstallScriptsV1Retrieve post-install scripts associated with your account.

Use this endpoint to view available automation scripts for VPS deployment.

- **Method**: `GET`
- **Path**: `/api/vps/v1/post-install-scripts`

**Parameters**:

- `page`: Page number

### VPS\_createPostInstallScriptV1Add a new post-install script to your account, which can then be used after virtual machine installation.

The script contents will be saved to the file `/post_install` with executable attribute set and will be executed once virtual machine is installed. The output of the script will be redirected to `/post_install.log`. Maximum script size is 48KB.

Use this endpoint to create automation scripts for VPS setup tasks.

- **Method**: `POST`
- **Path**: `/api/vps/v1/post-install-scripts`

**Parameters**:

- `name`: Name of the script (required)
- `content`: Content of the script (required)

### VPS\_attachPublicKeyV1Attach existing public keys from your account to a specified virtual machine.

Multiple keys can be attached to a single virtual machine.

Use this endpoint to enable SSH key authentication for VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/public-keys/attach/{virtualMachineId}`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `ids`: Public Key IDs to attach (required)

### VPS\_deletePublicKeyV1Delete a public key from your account.

**Deleting public key from account does not remove it from virtual machine**

Use this endpoint to remove unused SSH keys from account.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/public-keys/{publicKeyId}`

**Parameters**:

- `publicKeyId`: Public Key ID (required)

### VPS\_getPublicKeysV1Retrieve public keys associated with your account.

Use this endpoint to view available SSH keys for VPS authentication.

- **Method**: `GET`
- **Path**: `/api/vps/v1/public-keys`

**Parameters**:

- `page`: Page number

### VPS\_createPublicKeyV1Add a new public key to your account.

Use this endpoint to register SSH keys for VPS authentication.

- **Method**: `POST`
- **Path**: `/api/vps/v1/public-keys`

**Parameters**:

- `name`: name parameter (required)
- `key`: key parameter (required)

### VPS\_getTemplateDetailsV1Retrieve detailed information about a specific OS template for virtual machines.

Use this endpoint to view specific template specifications before deployment.

- **Method**: `GET`
- **Path**: `/api/vps/v1/templates/{templateId}`

**Parameters**:

- `templateId`: Template ID (required)

### VPS\_getTemplatesV1Retrieve available OS templates for virtual machines.

Use this endpoint to view operating system options before creating or recreating VPS instances.

- **Method**: `GET`
- **Path**: `/api/vps/v1/templates`

### VPS\_getActionDetailsV1Retrieve detailed information about a specific action performed on a specified virtual machine.

Use this endpoint to monitor specific VPS operation status and details.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/actions/{actionId}`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `actionId`: Action ID (required)

### VPS\_getActionsV1Retrieve actions performed on a specified virtual machine.

Actions are operations or events that have been executed on the virtual machine, such as starting, stopping, or modifying the machine. This endpoint allows you to view the history of these actions, providing details about each action, such as the action name, timestamp, and status.

Use this endpoint to view VPS operation history and troubleshoot issues.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/actions`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `page`: Page number

### VPS\_getAttachedPublicKeysV1Retrieve public keys attached to a specified virtual machine.

Use this endpoint to view SSH keys configured for specific VPS instances.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/public-keys`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `page`: Page number

### VPS\_getBackupsV1Retrieve backups for a specified virtual machine.

Use this endpoint to view available backup points for VPS data recovery.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/backups`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `page`: Page number

### VPS\_restoreBackupV1Restore a backup for a specified virtual machine.

The system will then initiate the restore process, which may take some time depending on the size of the backup.

**All data on the virtual machine will be overwritten with the data from the backup.**

Use this endpoint to recover VPS data from backup points.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/backups/{backupId}/restore`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `backupId`: Backup ID (required)

### VPS\_setHostnameV1Set hostname for a specified virtual machine.

Changing hostname does not update PTR record automatically. If you want your virtual machine to be reachable by a hostname, you need to point your domain A/AAAA records to virtual machine IP as well.

Use this endpoint to configure custom hostnames for VPS instances.

- **Method**: `PUT`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/hostname`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `hostname`: hostname parameter (required)

### VPS\_resetHostnameV1Reset hostname and PTR record of a specified virtual machine to default value.

Use this endpoint to restore default hostname configuration for VPS instances.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/hostname`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_getVirtualMachineDetailsV1Retrieve detailed information about a specified virtual machine.

Use this endpoint to view comprehensive VPS configuration and status.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_getVirtualMachinesV1Retrieve all available virtual machines.

Use this endpoint to view available VPS instances.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines`

### VPS\_purchaseNewVirtualMachineV1Purchase and setup a new virtual machine.

If virtual machine setup fails for any reason, login to [hPanel](https://hpanel.hostinger.com/) and complete the setup manually.

If no payment method is provided, your default payment method will be used automatically.

Use this endpoint to create new VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines`

**Parameters**:

- `item_id`: Catalog price item ID (required)
- `payment_method_id`: Payment method ID, default will be used if not provided
- `setup`: setup parameter (required)
- `coupons`: Discount coupon codes

### VPS\_getScanMetricsV1Retrieve scan metrics for the [Monarx](https://www.monarx.com/) malware scanner installed on a specified virtual machine.

The scan metrics provide detailed information about malware scans performed by Monarx, including number of scans, detected threats, and other relevant statistics. This information is useful for monitoring security status of the virtual machine and assessing effectiveness of the malware scanner.

Use this endpoint to monitor VPS security scan results and threat detection.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/monarx`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_installMonarxV1Install the Monarx malware scanner on a specified virtual machine.

[Monarx](https://www.monarx.com/) is a security tool designed to detect and prevent malware infections on virtual machines. By installing Monarx, users can enhance the security of their virtual machines, ensuring that they are protected against malicious software.

Use this endpoint to enable malware protection on VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/monarx`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_uninstallMonarxV1Uninstall the Monarx malware scanner on a specified virtual machine.

If Monarx is not installed, the request will still be processed without any effect.

Use this endpoint to remove malware scanner from VPS instances.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/monarx`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_getMetricsV1Retrieve historical metrics for a specified virtual machine.

It includes the following metrics:

- CPU usage
- Memory usage
- Disk usage
- Network usage
- Uptime

Use this endpoint to monitor VPS performance and resource utilization over time.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/metrics`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `date_from`: date\_from parameter (required)
- `date_to`: date\_to parameter (required)

### VPS\_setNameserversV1Set nameservers for a specified virtual machine.

Be aware, that improper nameserver configuration can lead to the virtual machine being unable to resolve domain names.

Use this endpoint to configure custom DNS resolvers for VPS instances.

- **Method**: `PUT`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/nameservers`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `ns1`: ns1 parameter (required)
- `ns2`: ns2 parameter
- `ns3`: ns3 parameter

### VPS\_createPTRRecordV1Create or update a PTR (Pointer) record for a specified virtual machine.

Use this endpoint to configure reverse DNS lookup for VPS IP addresses.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/ptr/{ipAddressId}`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `ipAddressId`: IP Address ID (required)
- `domain`: Pointer record domain (required)

### VPS\_deletePTRRecordV1Delete a PTR (Pointer) record for a specified virtual machine.

Once deleted, reverse DNS lookups to the virtual machine's IP address will no longer return the previously configured hostname.

Use this endpoint to remove reverse DNS configuration from VPS instances.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/ptr/{ipAddressId}`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `ipAddressId`: IP Address ID (required)

### VPS\_setPanelPasswordV1Set panel password for a specified virtual machine.

If virtual machine does not use panel OS, the request will still be processed without any effect. Requirements for password are same as in the [recreate virtual machine endpoint](https://github.com/hostinger/api-mcp-server/blob/main/#tag/vps-virtual-machine/POST/api/vps/v1/virtual-machines/%7BvirtualMachineId%7D/recreate).

Use this endpoint to configure control panel access credentials for VPS instances.

- **Method**: `PUT`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/panel-password`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `password`: Panel password for the virtual machine (required)

### VPS\_startRecoveryModeV1Initiate recovery mode for a specified virtual machine.

Recovery mode is a special state that allows users to perform system rescue operations, such as repairing file systems, recovering data, or troubleshooting issues that prevent the virtual machine from booting normally.

Virtual machine will boot recovery disk image and original disk image will be mounted in `/mnt` directory.

Use this endpoint to enable system rescue operations on VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/recovery`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `root_password`: Temporary root password for recovery mode (required)

### VPS\_stopRecoveryModeV1Stop recovery mode for a specified virtual machine.

If virtual machine is not in recovery mode, this operation will fail.

Use this endpoint to exit system rescue mode and return VPS to normal operation.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/recovery`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_recreateVirtualMachineV1Recreate a virtual machine from scratch.

The recreation process involves reinstalling the operating system and resetting the virtual machine to its initial state. Snapshots, if there are any, will be deleted.

## Password RequirementsPassword will be checked against leaked password databases. Requirements for the password are:

- At least 12 characters long
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- Is not leaked publicly

**This operation is irreversible and will result in the loss of all data stored on the virtual machine!**

Use this endpoint to completely rebuild VPS instances with fresh OS installation.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/recreate`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `template_id`: Template ID (required)
- `password`: Root password for the virtual machine. If not provided, random password will be generated. Password will not be shown in the response.
- `panel_password`: Panel password for the panel-based OS template. If not provided, random password will be generated. If OS does not support panel\_password this field will be ignored. Password will not be shown in the response.
- `post_install_script_id`: Post-install script to execute after virtual machine was recreated

### VPS\_restartVirtualMachineV1Restart a specified virtual machine by fully stopping and starting it.

If the virtual machine was stopped, it will be started.

Use this endpoint to reboot VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/restart`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_setRootPasswordV1Set root password for a specified virtual machine.

Requirements for password are same as in the [recreate virtual machine endpoint](https://github.com/hostinger/api-mcp-server/blob/main/#tag/vps-virtual-machine/POST/api/vps/v1/virtual-machines/%7BvirtualMachineId%7D/recreate).

Use this endpoint to update administrator credentials for VPS instances.

- **Method**: `PUT`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/root-password`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `password`: Root password for the virtual machine (required)

### VPS\_setupPurchasedVirtualMachineV1Setup newly purchased virtual machine with `initial` state.

Use this endpoint to configure and initialize purchased VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/setup`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)
- `template_id`: Template ID (required)
- `data_center_id`: Data center ID (required)
- `post_install_script_id`: Post-install script ID
- `password`: Password for the virtual machine. If not provided, random password will be generated. Password will not be shown in the response.
- `hostname`: Override default hostname of the virtual machine
- `install_monarx`: Install Monarx malware scanner (if supported)
- `enable_backups`: Enable weekly backup schedule
- `ns1`: Name server 1
- `ns2`: Name server 2
- `public_key`: Use SSH key

### VPS\_getSnapshotV1Retrieve snapshot for a specified virtual machine.

Use this endpoint to view current VPS snapshot information.

- **Method**: `GET`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/snapshot`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_createSnapshotV1Create a snapshot of a specified virtual machine.

A snapshot captures the state and data of the virtual machine at a specific point in time, allowing users to restore the virtual machine to that state if needed. This operation is useful for backup purposes, system recovery, and testing changes without affecting the current state of the virtual machine.

**Creating new snapshot will overwrite the existing snapshot!**

Use this endpoint to capture VPS state for backup and recovery purposes.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/snapshot`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_deleteSnapshotV1Delete a snapshot of a specified virtual machine.

Use this endpoint to remove VPS snapshots.

- **Method**: `DELETE`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/snapshot`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_restoreSnapshotV1Restore a specified virtual machine to a previous state using a snapshot.

Restoring from a snapshot allows users to revert the virtual machine to that state, which is useful for system recovery, undoing changes, or testing.

Use this endpoint to revert VPS instances to previous saved states.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/snapshot/restore`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_startVirtualMachineV1Start a specified virtual machine.

If the virtual machine is already running, the request will still be processed without any effect.

Use this endpoint to power on stopped VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/start`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

### VPS\_stopVirtualMachineV1Stop a specified virtual machine.

If the virtual machine is already stopped, the request will still be processed without any effect.

Use this endpoint to power off running VPS instances.

- **Method**: `POST`
- **Path**: `/api/vps/v1/virtual-machines/{virtualMachineId}/stop`

**Parameters**:

- `virtualMachineId`: Virtual Machine ID (required)

## About

[developers.hostinger.com](https://developers.hostinger.com/ "https://developers.hostinger.com")

### Topics

[api](https://github.com/topics/api "Topic: api") [ai](https://github.com/topics/ai "Topic: ai") [mcp](https://github.com/topics/mcp "Topic: mcp") [cursor](https://github.com/topics/cursor "Topic: cursor") [claude](https://github.com/topics/claude "Topic: claude") [hostinger](https://github.com/topics/hostinger "Topic: hostinger")

### Resources

[Readme](https://github.com/hostinger/#readme-ov-file)

### License

[MIT license](https://github.com/hostinger/#MIT-1-ov-file)

### Uh oh!

There was an error while loading. Please reload this page.

[Activity](https://github.com/hostinger/api-mcp-server/activity)

[Custom properties](https://github.com/hostinger/api-mcp-server/custom-properties)

### Stars

[**53** stars](https://github.com/hostinger/api-mcp-server/stargazers)

### Watchers

[**6** watching](https://github.com/hostinger/api-mcp-server/watchers)

### Forks

[**34** forks](https://github.com/hostinger/api-mcp-server/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fhostinger%2Fapi-mcp-server&report=hostinger+%28user%29)

## [Releases 53](https://github.com/hostinger/api-mcp-server/releases)

[

v0.1.24 Latest

Dec 19, 2025

](https://github.com/hostinger/api-mcp-server/releases/tag/v0.1.24)

[\+ 52 releases](https://github.com/hostinger/api-mcp-server/releases)

## [Packages 1](https://github.com/orgs/hostinger/packages?repo_name=api-mcp-server)

- [api-mcp-server](https://github.com/orgs/hostinger/packages/npm/package/api-mcp-server)

### Uh oh!

There was an error while loading. Please reload this page.

## [Contributors 7](https://github.com/hostinger/api-mcp-server/graphs/contributors)

- [![@algirdasci](https://avatars.githubusercontent.com/u/172274299?s=64&v=4)](https://github.com/algirdasci)
- [![@ginplonis](https://avatars.githubusercontent.com/u/164881800?s=64&v=4)](https://github.com/ginplonis)
- [![@dependabot[bot]](https://avatars.githubusercontent.com/in/29110?s=64&v=4)](https://github.com/apps/dependabot)
- [![@LaurynasMinelga](https://avatars.githubusercontent.com/u/66416800?s=64&v=4)](https://github.com/LaurynasMinelga)
- [![@zygintas](https://avatars.githubusercontent.com/u/3470788?s=64&v=4)](https://github.com/zygintas)
- [![@aurimasbutkus](https://avatars.githubusercontent.com/u/20791214?s=64&v=4)](https://github.com/aurimasbutkus)
- [![@laurynasgadl](https://avatars.githubusercontent.com/u/30233941?s=64&v=4)](https://github.com/laurynasgadl)

## Languages

- [JavaScript 99.9%](https://github.com/hostinger/api-mcp-server/search?l=javascript)
- [Dockerfile 0.1%](https://github.com/hostinger/api-mcp-server/search?l=dockerfile)

## Footer© 2026 GitHub, Inc.

### Footer navigation

- [Terms](https://docs.github.com/site-policy/github-terms/github-terms-of-service)
- [Privacy](https://docs.github.com/site-policy/privacy-policies/github-privacy-statement)