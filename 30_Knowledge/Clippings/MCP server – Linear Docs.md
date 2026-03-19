---
title: "MCP server – Linear Docs"
source: "https://linear.app/docs/mcp"
author:
  - "[[@linear]]"
published:
created: 2026-01-28
description: "This guide is intended to give you an overview of Linear's features, discover their flexibility, and provide tips for how to use Linear to improve the speed, value, and joy of your work."
tags:
  - "clippings"
---
## MCP server

![Abstract image of a drive with Linear's logo and the words "Remote MCP server"](https://webassets.linear.app/images/ornj730p/production/54373418b3cb31208f112cd8137d7dd825d1b7c0-3600x1800.png?w=1440&q=95&auto=format&dpr=2)

Abstract image of a drive with Linear's logo and the words "Remote MCP server"

The Model Context Protocol (MCP) server provides a standardized interface that allows any compatible AI model or agent to access your Linear data in a simple and secure way.

Connect to our MCP server natively in Claude, Cursor, and other clients or use the [`mcp-remote`](https://github.com/geelen/mcp-remote) module for backwards compatibility with clients that do not support remote MCP.

Linear's MCP server follows the authenticated remote [MCP spec](https://modelcontextprotocol.io/specification/2025-03-26), so the server is centrally hosted and managed. The Linear MCP server has tools available for finding, creating, and updating objects in Linear like issues, projects, and comments — with more functionality on the way, and [feedback](https://linear.app/contact/support) on its functionality is welcomed.

Our MCP server supports both Server-Sent Events (SSE) and Streamable HTTP transports. Both transports use OAuth 2.1 with dynamic client registration for authentication at the following addresses:

- HTTP: `https://mcp.linear.app/mcp`
- SSE: `https://mcp.linear.app/sse`

We recommend using the streamable HTTP endpoint where supported for increased reliability. For instructions for specific clients, read on…

**Team, Enterprise (Claude.ai)**

- Navigate to **Settings** in the sidebar on web or desktop
- Scroll to **Integrations** at the bottom and click **Add more**
- In the prompt enter:
	- Integration name: `Linear`
	- Integration URL: `https://mcp.linear.app/mcp`
- Make sure to enable the tools in any new chats

**Free, Pro (Claude desktop)**

1. Open the file `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the following and restart the Claude desktop app:

```json
{

  "mcpServers": {

    "linear": {

      "command": "npx",

      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]

    }

  }

}
```

**Claude Code**

```json
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

Then run `/mcp` once you've opened a Claude Code session to go through the authentication flow.

The setup steps for the MCP server are the same regardless of whether you use the IDE Extension or the CLI since the configuration is shared.

**Configuration via CLI:**

Run the following command in Terminal:

```sh
codex mcp add linear --url https://mcp.linear.app/mcp
```

This will automatically prompt you to log in with your Linear account and connect it to your Codex.

**Note**: If this is the first time you are using an MCP in Codex you will need to enable the `rmcp` feature for this to work. Add the following into your `~/.codex/config.toml`:

```sh
[features]

experimental_use_rmcp_client = true
```

**Configuration through environment variables:**

1. Open the `~/.codex/config.toml` file in your preferred editor
2. Add the following:

```sh
[features]

experimental_use_rmcp_client = true

 

[mcp_servers.linear]

url = "https://mcp.linear.app/mcp"
```

Run `codex mcp login linear` to move through the authentication flow.

To add the MCP to Cursor, you can install by clicking [here](https://anysphere.cursor-deeplink/mcp/install?name=Linear&config=eyJ1cmwiOiJodHRwczovL21jcC5saW5lYXIuYXBwL21jcCJ9), or searching for Linear from Cursor's [MCP tools page](https://cursor.com/docs/context/mcp/directory).  

![C](https://webassets.linear.app/images/ornj730p/production/7ff4a8f3f3f95e1a25a241c49f5d46c66e17b80a-760x343.png?w=1440&q=95&auto=format&dpr=2)

```json
{

  "mcpServers": {

    "linear": {

      "command": "npx",

      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]

    }

  }

}
```

1. CTRL/CMD P and search for **MCP: Add Server**.
2. Select **Command (stdio)**
3. Enter the following configuration, and hit enter.

`npx mcp-remote https://mcp.linear.app/mcp`

1. Enter the name **Linear** and hit enter.
2. Activate the server using **MCP: List Servers** and selecting **Linear**, and selecting **Start Server**.

To add the MCP to v0, you can install from the [connections](https://v0.app/chat/settings/mcp-connections) page.

1. CTRL/CMD , to open Windsurf settings.
2. Under Scroll to Cascade -> MCP servers
3. Select **Add Server -> Add custom server**
4. Add the following:

```json
{

  "mcpServers": {

    "linear": {

      "command": "npx",

      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]

    }

  }

}
```

1. CMD , to open Zed settings.
2. Add the following:

```json
{

  "context_servers": {

    "linear": {

      "source": "custom",

      "command": "npx",

      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"],

      "env": {}

    }

  }

}
```

Hundreds of other tools now support MCP servers, you can configure them to use Linear's MCP server with the following settings:

- **Command**: `npx`
- **Arguments**: `-y mcp-remote https://mcp.linear.app/mcp`
- **Environment**: None