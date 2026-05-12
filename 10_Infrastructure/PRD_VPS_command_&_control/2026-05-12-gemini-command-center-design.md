# Design Spec: Gemini Command Center

## 1. Overview
The Gemini Command Center is a local web application designed to orchestrate a developer's AI ecosystem. Its primary goals are to optimize RAM usage by managing MCP (Model Context Protocol) servers on-demand, monitor and control a remote VPS (Hostinger), and trigger automation workflows (n8n, local scripts).

## 2. Goals
- **RAM Optimization:** Provide a hybrid control system (manual switches + profiles) to activate/deactivate MCP servers across multiple IDEs (Claude, Cursor, VSCode).
- **Unified Control:** Centralize VPS monitoring and workflow execution in a single visual interface.
- **Interoperability:** Modify local configuration files (`mcp.json`, `.claude.json`) and manage local OS processes.

## 3. Architecture
- **Backend:** Node.js/Fastify server.
    - Responsible for FS operations (config updates), process management (`kill`, `spawn`), and proxying API requests to Hostinger/n8n.
- **Frontend:** React + Tailwind CSS dashboard.
    - Neon/Dark theme.
    - Real-time status updates via WebSockets or polling.
- **Storage:** Local JSON for app settings, reading directly from system paths for MCP configs.

## 4. Key Features
### 4.1 MCP Manager (The "RAM Saver")
- **Dynamic Config Editing:** Adds/Removes server definitions from IDE config files to prevent automatic startup.
- **Process Oversight:** Identifies and terminates orphan `node`/`npm` processes related to MCP.
- **Profiles:** One-click activation for "Web Dev", "Data Science", "Admin" modes.

### 4.2 VPS Control (Hostinger Integration)
- **Monitoring:** Fetch CPU, RAM, and Disk usage via Hostinger API.
- **Operations:** Buttons for "Create Snapshot", "Restart Project (Docker)", and "Service Status".

### 4.3 Workflow & Sync
- **Execution:** Trigger local shell scripts (e.g., `Obsidian -> VPS sync`).
- **Webhooks:** Send triggers to local or remote n8n instances.

## 5. Security & Safety
- **Local Access Only:** Binds to `127.0.0.1` by default.
- **Credential Protection:** Uses an `.env` file (not committed to git) for Hostinger tokens and GitHub PATs.
- **Backup Mechanism:** Creates a backup of any config file before modification.

## 6. Success Criteria
- Reduction of background RAM usage by at least 1GB when MCP servers are toggled off.
- Successful triggering of a VPS snapshot from the UI.
- Unified view of all active MCP servers across different clients.
