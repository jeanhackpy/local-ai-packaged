#!/bin/bash

# ==============================================================================
# 🧹 SUPER CLEAN - Script de Maintenance Massive macOS
# ==============================================================================
# Cibles : Caches de dev (npm, pip, brew, composer), Docker, Logs, Xcode.
# ==============================================================================

LOG_FILE="/Users/phil/Documents/Vaults/SystemMac/00_System/Maintenance/clean_history.log"
HEALTH_SCRIPT="/Users/phil/Documents/Vaults/SystemMac/00_System/Maintenance/mac_health_check.sh"

echo "🚀 Démarrage du Grand Nettoyage SystemMac - $(date)" | tee -a "$LOG_FILE"

# 1. Nettoyage des gestionnaires de paquets
echo "📦 Nettoyage des gestionnaires de paquets..."
[ -x "$(command -v brew)" ] && (echo "   - Brew cleanup..."; brew cleanup -s; brew autoremove)
[ -x "$(command -v npm)" ] && (echo "   - npm cache clean..."; npm cache clean --force)
[ -x "$(command -v pip3)" ] && (echo "   - pip cache purge..."; pip3 cache purge)
[ -x "$(command -v composer)" ] && (echo "   - composer clear-cache..."; composer clear-cache)

# 2. Nettoyage Docker (si actif)
if pgrep -x "Docker" > /dev/null; then
    echo "🐳 Nettoyage Docker (Prune)..."
    docker system prune -f --volumes
fi

# 3. Nettoyage Apple / Dev (Xcode & Logs)
echo "🍎 Nettoyage Apple & Logs..."
# DerivedData Xcode (souvent très volumineux)
[ -d ~/Library/Developer/Xcode/DerivedData ] && (echo "   - Xcode DerivedData..."; rm -rf ~/Library/Developer/Xcode/DerivedData/*)
# Logs système (> 7 jours)
find ~/Library/Logs -type f -mtime +7 -delete
find /Users/phil/Library/Caches -type f -atime +7 -delete

# 4. Vidage de la corbeille (optionnel mais utile)
# echo "🗑️ Vidage de la corbeille..."
# rm -rf ~/.Trash/*

# 5. Mise à jour de la note de santé Obsidian
if [ -f "$HEALTH_SCRIPT" ]; then
    echo "📊 Mise à jour du bilan de santé dans Obsidian..."
    bash "$HEALTH_SCRIPT"
fi

echo "✨ Nettoyage terminé avec succès ! - $(date)" | tee -a "$LOG_FILE"
echo "--------------------------------------------------" | tee -a "$LOG_FILE"
