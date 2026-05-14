# Gemini Context: Obsidian Vault for Project REcall

This document provides a comprehensive overview of the "Gemini-obsidian" directory, which serves as a shared knowledge base and operational memory for our collaboration on "Project REcall".

## Directory Overview

This directory is an Obsidian vault used to manage the strategy, architecture, and daily interactions related to the development of the **REcall** real estate intelligence platform. It is a non-code project, meaning it contains documentation, plans, and logs rather than application source code.

## Key Files

*   **`Project_Blueprint.md`**: This is the most important file. It is the master document outlining the vision, business strategy, technical architecture, and execution plan for the entire REcall ecosystem.
*   **`README.md`**: This file explains the structure of this Obsidian vault, providing a visual map of the directories and guidelines on how to log our daily interactions, manage project notes, and organize data. It also contains details about the configured services like Qdrant and Supabase.
*   **`000_Blackboard.md`**: A general-purpose file for quick notes, brainstorming, or temporary information.
*   **`gemini-reboot-obsidian.md`**: Contains notes and context related to the setup and purpose of this shared vault for our interactions.

## Usage Guidelines

As outlined in the `README.md`, we should follow these conventions:

*   **Daily Logs:** Record our interactions (discussions, tasks, file changes) in the `logs/daily_interactions/` directory, with one file per day (e.g., `YYYY-MM-DD.md`).
*   **Project Notes:** All notes, goals, and task breakdowns for a specific sub-project should be centralized in the `projects/` directory.
*   **Data & Documents:** Raw data files (like CSVs) belong in `data/`, while processed outputs (like reports) go into `documents/`.
*   **Configuration & Scripts:** Infrastructure and tool configurations are stored in `config/`, and utility scripts are in `scripts/`.

## Project REcall Summary

The following is a high-level summary derived from the `Project_Blueprint.md`:

*   **Vision:** To build **REcall OS**, an AI-powered "Palantir for Real Estate" in Southeast Asia, starting with Thailand. The goal is to bring clarity and efficiency to the market through data unification, AI agents, and immersive 3D environments.
*   **Core Brands:**
    1.  **REcall Agency:** The core technology and cybersecurity builder.
    2.  **Reflexion.asia:** The flagship B2C/B2B real estate marketplace for Thailand.
    3.  **Patrimonasia.com:** A B2B platform connecting European investors to the Thai market.
*   **Core Technology Stack:**
    *   **Frontend:** Next.js, TailwindCSS
    *   **Backend & Data:** Supabase (PostgreSQL), Qdrant (Vector DB), Neo4j (Graph DB), Redis
    *   **Orchestration & AI:** n8n, LangGraph/Flowise, OpenRouter, and locally-hosted LLMs via Ollama.
    *   **Data Pipeline:** Crawl4AI, Pydantic
    *   **3D Environment:** Unreal Engine 5, Cesium
    *   **Deployment:** Hostinger, Vercel, and dedicated VPS.
