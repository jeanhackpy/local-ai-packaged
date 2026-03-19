# Agent Report: 2026-01-28 - Vault Optimization & AI Orchestration Strategy

This report summarizes the changes made to the Obsidian vault and the proposed strategy for optimizing AI agent usage, based on user requests.

## I. Vault Structure Improvement: Fixing Redundant/Nested Structures

**Objective:** Eliminate redundancy and improve clarity by consolidating content from the nested `/Users/phil/Documents/Vaults/SystemMac/SystemMac/` directory into the main vault structure.

**Actions Taken:**

1.  **`/Users/phil/Documents/Vaults/SystemMac/SystemMac/Skills Antigravity Awesome.md` vs. `/Users/phil/Documents/Vaults/SystemMac/Development/Skills Antigravity Awesome.md`**
    *   **Decision:** Kept the version in `Development/` (newer by modification date). Deleted the nested version.
    *   **Link Updates:** Updated all links pointing to `[[SystemMac/Skills Antigravity Awesome]]` to `[[Development/Skills Antigravity Awesome]]`.

2.  **`/Users/phil/Documents/Vaults/SystemMac/SystemMac/SystemPolicy.md`**
    *   **Decision:** Content was found to be largely integrated into `SystemPolicy/02_DevEnv.md` (Development Environment Standards, Agentic Workflow Policies) and `SystemPolicy/03_Security.md` (Security Practices). Deleted the redundant nested file.
    *   **Link Updates:** Updated all links pointing to `[[SystemMac/SystemPolicy]]` to `[[SystemPolicy/README]]`.

3.  **`/Users/phil/Documents/Vaults/SystemMac/SystemMac/IDE & Skills.md` vs. `/Users/phil/Documents/Vaults/SystemMac/Development/IDE & Skills.md`**
    *   **Decision:** Kept the version in `Development/` (newer by modification date). Merged the unique `## 📁 Project Structure` section from the nested file into the `Development/` version. Deleted the nested file.
    *   **Link Updates:** No explicit links to `[[SystemMac/IDE & Skills]]` were found.

4.  **`/Users/phil/Documents/Vaults/SystemMac/SystemMac/VPS Management Prompt Template.md` vs. `/Users/phil/Documents/Vaults/SystemMac/Resources/VPS Management Prompt Template.md`**
    *   **Decision:** The nested version was newer by modification date. It was moved to the `Resources/` folder to align with the "Final Clean Structure". The older `Resources/` version was implicitly replaced by the move.
    *   **Link Updates:** Internal links within the moved file were updated (`[[SystemMac/README]]` -> `[[README]]`, etc.). No explicit links to `[[Resources/VPS Management Prompt Template]]` or `[[SystemMac/VPS Management Prompt Template]]` were found in other files.

5.  **`/Users/phil/Documents/Vaults/SystemMac/SystemMac/VPS Hostinger & WordPress.md` vs. `/Users/phil/Documents/Vaults/SystemMac/Development/VPS Hostinger & WordPress.md`**
    *   **Decision:** Kept the version in `Development/` (newer by modification date). Deleted the nested version.
    *   **Link Updates:** No explicit links to `[[SystemMac/VPS Hostinger & WordPress]]` were found.

6.  **`/Users/phil/Documents/Vaults/SystemMac/SystemMac/README.md`**
    *   **Decision:** Deleted, as its purpose was to document the now-removed nested `SystemMac` directory. Its content was either redundant or replaced by the main vault `README.md`.
    *   **Link Updates:** No explicit links to `[[SystemMac/README]]` were found.

7.  **Removal of Empty Directory:** The empty `/Users/phil/Documents/Vaults/SystemMac/SystemMac/` directory was successfully removed.

## II. Improving Vault Cross-Referencing

**Objective:** Enhance discoverability and navigation by adding explicit `[[wiki-links]]` between related notes, focusing initially on the `SystemPolicy/` documents.

**Actions Taken (Examples):**

*   **`SystemPolicy/01_BaseSetup.md`:**
    *   Linked "SSH keys" to `[[Development/VPS Hostinger & WordPress#SSH Config]]`.
    *   Linked "Homebrew", "Node.js and npm" to `[[SystemPolicy/02_DevEnv#Package Management]]`.
    *   Linked "Python managed by pyenv" to `[[Development/IDE & Skills#Python Setup]]`.
    *   Linked "Git" to `[[SystemPolicy/02_DevEnv#Version Control]]`.
    *   Added direct links to agent documentation: `[[Agents/GeminiCLI]]`, `[[Agents/Ollama]]`, `[[Agents/Crawl4AI]]`, `[[Agents/Superwhisper]]`.
*   **`SystemPolicy/02_DevEnv.md`:**
    *   Linked "IDE Configuration Standards" to `[[Development/IDE & Skills]]`.
    *   Linked "Agentic Workflow Policies" to `[[Development/Skills Antigravity Awesome]]`.
    *   Linked specific IDEs (Cursor, VS Code, Antigravity) to `[[Development/IDE & Skills]]`.
    *   Linked "Git" (version control) and "Homebrew" (package management) to `[[Development/IDE & Skills]]`.
    *   Linked "pipx" and "pyenv" to `[[Development/IDE & Skills#Python Setup]]`.
*   **`SystemPolicy/03_Security.md`:**
    *   Linked "SSH keys properly secured" to `[[Development/VPS Hostinger & WordPress#SSH Hardening]]`.
    *   Linked "API keys stored in secure locations" to `[[Infra/VPS_Hostinger/Plan_Action_Monitoring#2-Intégration-Hostinger-MCP]]`.
    *   Linked "Firewall configured with strict rules" to `[[Development/VPS Hostinger & WordPress#Security Management]]`.
    *   Linked "Malware scanning and prevention" to `[[Infra/VPS_Hostinger/VPS_Exploration_2026-01-27#Monarx Malware Scanner]]`.
*   **`SystemPolicy/04_Workflow.md`:**
    *   Linked "AI agents" to `[[Agents]]`.
    *   Linked "Raycast" and "Warp" to `[[01_BaseSetup#Productivity Tools]]`.
*   **`SystemPolicy/05_Maintenance.md`:**
    *   Linked "backup verification" to `[[Development/VPS Hostinger & WordPress#Automated Backups]]` and `[[Infra/VPS_Hostinger/VPS_Exploration_2026-01-27#Snapshots & Backups]]`.
    *   Linked "Daily log review" to `[[Infra/VPS_Hostinger/Plan_Action_Monitoring#1-Script-de-monitoring-Python]]`.
    *   Linked "Weekly performance metrics analysis" to `[[Infra/VPS_Hostinger/VPS_Exploration_2026-01-27#Métriques sur 24h]]`.
    *   Linked "Quarterly security audit" to `[[SystemPolicy/03_Security]]`.

## III. AI Agent Orchestration Strategy

**Objective:** Optimize the usage of main IDEs and AI agents for web development projects on Hostinger, respecting rate limits, leveraging free tiers, and specifically using OpenRouter with *only its free models* and continuous query capping.

### Key Principles:

1.  **Prioritize Local Ollama (Mac M4 / VPS):** First choice for any suitable task. No external cost/rate limits.
2.  **Strict OpenRouter Free Model Use:** OpenRouter is used *only with its free models*, strictly adhering to 1000 req/day and 20 RPM limits, enforced by a custom wrapper.
3.  **Other Free Tiers:** Gemini CLI (60 req/min) and Anthropic (up to $10/month) as additional fallbacks for specific tasks/models.
4.  **OpenRouter Paid Models:** Last resort, only with explicit user override/confirmation.
5.  **Integrated IDE Tools:** Cursor/Antigravity configured to use OpenRouter (via free model wrapper) for premium features.
6.  **Strategic Fallback:** Robust logic to switch between services on rate limit hits or errors.
7.  **Configuration & Monitoring:** Secure API keys and monitor usage.

### Tool & IDE Integration Matrix Summary:

| Task Type                      | Primary Tool(s)                                   | Secondary / Fallback Tool(s)                      | IDE Context           |
| :----------------------------- | :------------------------------------------------ | :------------------------------------------------ | :-------------------- |
| **Code Gen/Completion**          | Local Ollama, Cursor/Antigravity (OpenRouter Free) | GitHub Copilot (VS Code, free), Gemini CLI        | Cursor, VS Code, Antigravity |
| **Code Review/Refactoring**      | Ollama (VPS), Cursor/Antigravity (OpenRouter Free) |                                                   | Cursor, Antigravity   |
| **Complex Problem Solving/Arch** | OpenRouter (Free via wrapper), Ollama (VPS)       | Gemini CLI                                        | Any IDE, Custom Script |
| **Content Generation**         | OpenRouter (Free via wrapper, n8n/script), Ollama (VPS) | Anthropic API (free tier)                         | n8n, Custom Script    |
| **Web Scraping/Data Ext.**       | Crawl4AI Datascraper                              | Ollama/OpenRouter (Free via wrapper) for processing | Script                |
| **Voice Dictation**              | Superwhisper TTS                                  |                                                   | OS-level              |
| **General AI Assistance**        | Ollama (Mac M4)                                   | Gemini CLI, OpenRouter (Free via wrapper)         | CLI, Any IDE          |

### Project-Specific Integration:

*   **`recall-agency.com` & `reflexion.asia` (React Frontend, Hostinger VPS):**
    *   **Code Gen/Review:** IDEs with OpenRouter Free wrapper (BYO key).
    *   **Agentic Features/AI System:** **n8n on VPS** orchestrates workflows integrating **OpenRouter Free Model Wrapper** for LLM calls, **Crawl4AI** for data, and **Local Ollama (VPS)** for processing.
*   **Content/Social Media Automation:** Driven by n8n workflows and custom scripts leveraging the OpenRouter Free Model Wrapper.
*   **Pipeline Extraction:** Crawl4AI to scrape, Ollama (VPS) for initial processing, OpenRouter Free Model Wrapper for complex summarization/enrichment before PostgreSQL.

### Configuration Changes:

*   **OpenRouter Key:** Secure `OPENROUTER_API_KEY` in environment variables.
*   **Custom OpenRouter Free Model Wrapper:** Python module/microservice enforcing free models, rate limits (1000 req/day, 20 RPM), and disabling unwanted OpenRouter features (websearch + two others). Configure all tools/IDEs to use this wrapper.
*   **Ollama:** Install Ollama and models on Mac M4 and Hostinger VPS (consider Docker on VPS).
*   **Fallback Logic:** Implement sequence: Ollama -> OpenRouter Free Wrapper -> Gemini CLI -> Anthropic Free.
*   **Environment Variables:** For all API keys (local & VPS) and n8n credentials.
*   **OpenCode:** Configure to point to the custom OpenRouter Free Model Wrapper.
*   **Gemini/Copilot:** Continue existing free-tier configurations, respecting limits.

### Scripting & Automation:

*   **Core Component:** **OpenRouter Free Model Rate Limiter/Wrapper** (Python).
*   **n8n Workflows:** For LLM orchestration, usage monitoring, and alerts on VPS.
*   **Local Scripting (Mac M4):** **Intelligent AI CLI Wrapper** (Python) for central LLM interface and fallback.
*   **IDE Configuration:** Configure Cursor/Antigravity to use the local OpenRouter wrapper.
*   **Version Control & Documentation:** All custom scripts and n8n workflows in Git (e.g., `Scripts/` folder) with clear documentation.

This comprehensive approach aims to create a highly efficient, cost-optimized, and robust AI-driven development environment for your projects.