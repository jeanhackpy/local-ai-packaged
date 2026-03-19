#!/bin/bash

# Configuration
VAULT_LINKS_DIR="/Users/phil/Documents/Vaults/SystemMac/00_System/Links"
DOCUMENTS_DIR="/Users/phil/Documents"
APPS_DATA_DIR="/Users/phil/Documents/AppsData"
THE_LAB_DIR="/Users/phil/Documents/The_Lab"

# Fonction pour créer un symlink s'il n'existe pas
create_link() {
    local target="$1"
    local link_name="$2"
    if [ -d "$target" ] || [ -f "$target" ]; then
        if [ ! -L "$VAULT_LINKS_DIR/$link_name" ]; then
            ln -s "$target" "$VAULT_LINKS_DIR/$link_name"
            echo "✅ Lien créé : $link_name -> $target"
        fi
    fi
}

echo "🔄 Synchronisation granulaire des liens Obsidian..."

# 1. AppsData - Tous les sous-dossiers
for folder in "$APPS_DATA_DIR"/*; do
    [ -d "$folder" ] && create_link "$folder" "App_$(basename "$folder")"
done

# 2. The Lab - Pipeline et Hostinger spécifiquement
create_link "$THE_LAB_DIR/Pipeline" "Lab_Pipeline"
create_link "$THE_LAB_DIR/hostinger" "Lab_Hostinger_Codes"

# 3. Cline - Workflows et MCP
create_link "$DOCUMENTS_DIR/Cline/Workflows" "Cline_Workflows"
create_link "$DOCUMENTS_DIR/Cline/MCP" "Cline_MCP_Servers"

# 4. Dotfiles Agents
create_link "/Users/phil/.agents/skills" "Agent_Skills_Global"
create_link "/Users/phil/.gemini/extensions" "Gemini_Extensions"

echo "✨ Synchronisation terminée."
