# Real Estate AI os FAktory

The **FAktory** is a module of the **Real Estate AI OS** system, designed to produce high-quality data for the **Palanthai** stack and the Obsidian Knowledge Base Wiki.

## Real Estate AI os FAktory included:
✅ **Self-hosted n8n** - Low-code platform with over 400 integrations and advanced AI components

✅ **Supabase** - Open source database as a service - most widely used database for AI agents

✅ **Ollama** - Cross-platform LLM platform to install and run the latest local LLMs

✅ **Qdrant** - Open source, high performance vector store with an comprehensive API. Even though you can use Supabase for RAG, this was kept since it's faster than Supabase so sometimes is the better option.

✅ **Neo4j** - Knowledge graph engine that powers tools like GraphRAG, LightRAG, and Graphiti

✅ **SearXNG** - Open source, free internet metasearch engine which aggregates results from up to 229 search services. Users are neither tracked nor profiled, hence the fit with the local AI package.

✅ **COOLIFY** - Replaces Caddy for service orchestration. Routing to internal services (Supabase, Qdrant, Neo4j, etc.) is performed through **Tailscale** for secure connections.

---

**Next PHASE:** Langfuse - and Clickhouse Open source LLM engineering platform for agent observability

## Prerequisites
Before you begin, make sure you have the following software installed:

*   **Python** - Required to run the setup script
*   **Git/GitHub Desktop** - For easy repository management
*   **Docker/Docker Desktop** - Required to run all services
*   **Tailscale** - For secure access to internal services

## Installation
Clone the repository and navigate to the project directory:

```bash
git clone -b stable https://github.com/jeanhackpy/local-ai-packaged.git
cd local-ai-packaged
```

Before running the services, you need to set up your environment variables for Supabase following their self-hosting guide.

1.  Make a copy of `.env.example` and rename it to `.env` in the root directory of the project
2.  Set the following required environment variables:

```env
############
# N8N Configuration
############
N8N_ENCRYPTION_KEY=
N8N_USER_MANAGEMENT_JWT_SECRET=

############
# Supabase Secrets
############
POSTGRES_PASSWORD=
JWT_SECRET=
ANON_KEY=
SERVICE_ROLE_KEY=
DASHBOARD_USERNAME=
DASHBOARD_PASSWORD=
POOLER_TENANT_ID=

############
# Neo4j Secrets
############
NEO4J_AUTH=

############
# Langfuse credentials
############
CLICKHOUSE_PASSWORD=
MINIO_ROOT_PASSWORD=
LANGFUSE_SALT=
NEXTAUTH_SECRET=
ENCRYPTION_KEY=
```

### Important
Make sure to generate secure random values for all secrets. Never use the example values in production.

Set the following environment variables if deploying to production, otherwise leave commented:
```env
############
# Coolify / Network Config
############
N8N_HOSTNAME=n8n.yourdomain.com
SUPABASE_HOSTNAME=supabase.yourdomain.com
OLLAMA_HOSTNAME=ollama.yourdomain.com
SEARXNG_HOSTNAME=searxng.yourdomain.com
NEO4J_HOSTNAME=neo4j.yourdomain.com
LETSENCRYPT_EMAIL=your-email-address
```

The project includes a `start_services.py` script that handles starting both the Supabase and local AI services.

### Real Estate AI OS
**Run the starter FAKTORY fully on CPU:**

```bash
python start_services.py --profile cpu
```

**Run Ollama on your Mac for faster inference, and connect to that from the n8n instance:**

```bash
python start_services.py --profile none
```

If you want to run Ollama on your mac, check the Ollama homepage for installation instructions.

#### For Mac users running OLLAMA locally
If you're running OLLAMA locally on your Mac (not in Docker), you need to modify the `OLLAMA_HOST` environment variable in the n8n service configuration. Update the `x-n8n` section in your Docker Compose file as follows:

```yaml
x-n8n: &service-n8n
  # ... other configurations ...
  environment:
    # ... other environment variables ...
    - OLLAMA_HOST=host.docker.internal:11434
```

Additionally, after you see "Editor is now accessible via: http://localhost:5678/":
1.  Head to `http://localhost:5678/home/credentials`
2.  Click on "Local Ollama service"
3.  Change the base URL to `http://host.docker.internal:11434/`

#### For everyone else
```bash
python start_services.py --profile cpu
```

### The environment argument
The `start_services.py` script offers the possibility to pass one of two options for the environment argument, `private` (default environment) and `public`:

*   **private**: you are deploying the stack in a safe environment, hence a lot of ports can be made accessible without having to worry about security
*   **public**: the stack is deployed in a public environment, which means the attack surface should be made as small as possible. All ports except for 80 and 443 are closed.

## Deploying to the Cloud
### Prerequisites for the below steps
*   Linux machine (preferably Ubuntu) with Nano, Git, and Docker installed
*   Tailscale configured for secure access to internal services

### Extra steps
Before running the above commands to pull the repo and install everything:

Run the commands as root to open up the necessary ports:
```bash
ufw enable
ufw allow 80 && ufw allow 443
ufw reload
```

**WARNING:** ufw does not shield ports published by docker. Just make sure that all traffic runs through the proxy service.

Run the `start_services.py` script with the environment argument `public` to indicate you are going to run the package in a public environment.
```bash
python3 start_services.py --profile cpu --environment public
```

Set up A records for your DNS provider to point your subdomains to the IP address of your cloud instance.

## Importing Starter Workflows
This package includes pre-built n8n workflows in the `n8n/backup/workflows/` folder. To import them:

1.  Open n8n at `http://localhost:5678/` (or your custom domain/Tailscale IP)
2.  Go to your workflow list and click the three-dot menu or use **Import from File**
3.  Select the JSON files from the `n8n/backup/workflows/` folder on your local machine (including the Palanthai specific ones in the `palanthai` subfolder)

## ⚡️ Quick start and usage
The main component of the self-hosted AI starter kit is a docker compose file pre-configured with network and disk.

1.  Open `http://localhost:5678/` in your browser to set up n8n. You are NOT creating an account with n8n, it is only a local account for your instance!
2.  Import a workflow from `n8n/backup/workflows/`.
3.  Create credentials for every service:
    *   **Ollama URL:** `http://ollama:11434`
    *   **Postgres (through Supabase):** use DB, username, and password from `.env`. **IMPORTANT: Host is `db`**
    *   **Qdrant URL:** `http://qdrant:6333`
    *   **Google Drive:** Follow the n8n guide.
4.  Select **Test workflow** to start running.
5.  If this is the first time, you may need to wait until Ollama finishes downloading models (check docker console logs).
6.  Make sure to toggle the workflow as active and copy the "Production" webhook URL!

To open n8n at any time, visit `http://localhost:5678/`.

## Upgrading
To update all containers to their latest versions:

```bash
# Stop all services
docker compose -p localai -f docker-compose.yml --profile cpu down

# Pull latest versions
docker compose -p localai -f docker-compose.yml --profile cpu pull

# Start services again
python start_services.py --profile cpu
```

## Troubleshooting
*   **Supabase Pooler:** If the `supabase-pooler` container keeps restarting, check the [GitHub issue](https://github.com/supabase/supabase/issues/22026).
*   **Supabase Analytics:** If startup fails after changing Postgres password, delete `supabase/docker/volumes/db/data`.
*   **Docker Desktop:** Enable "Expose daemon on tcp://localhost:2375 without TLS" in settings.
*   **Postgres Password:** Avoid "@" character in your password.
*   **SearXNG:** If restarting, run `chmod 755 searxng` in the project folder.

## 👓 Recommended reading
*   [AI agents for developers with n8n](https://n8n.io/blog/ai-agents-for-developers-from-theory-to-practice-with-n8n/)
*   [Build an AI workflow in n8n](https://docs.n8n.io/integrations/builtin/nodes/n8n-nodes-langchain.ai-agent/)
*   [What are vector databases?](https://qdrant.tech/articles/what-is-a-vector-database/)

## 🎥 Video walkthrough
[Setting up the Local AI Starter Kit](https://docs.n8n.io/hosting/installation/docker/)

## 🛍️ More AI templates
Visit the [official n8n AI template gallery](https://n8n.io/workflows/).

## Tips & tricks
### Accessing local files
The kit creates a shared folder mounted to the n8n container at `/data/shared`. Use this path in nodes like Read/Write Files from Disk.

**Enabling Local File Trigger and Execute Command nodes:**
In `docker-compose.yml`, find the `x-n8n` section and ensure `NODES_EXCLUDE=[]` is set to enable these nodes.
