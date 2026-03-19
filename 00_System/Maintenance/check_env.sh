#!/bin/bash

# Chemin vers le fichier .env.local à la racine du vault
ENV_FILE="/Users/phil/Documents/Vaults/SystemMac/.env.local"

echo "🔍 Vérification de l'environnement de sécurité..."

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Erreur : Fichier $ENV_FILE introuvable."
    echo "Veuillez le créer en suivant le modèle dans 00_System/Secrets/API_KEYS_MANAGEMENT.md"
    exit 1
fi

REQUIRED_KEYS=(
    "HOSTINGER_API_KEY"
    "ANTHROPIC_API_KEY"
    "GEMINI_API_KEY"
    "SUPABASE_URL"
    "SUPABASE_SERVICE_ROLE_KEY"
)

MISSING=0
for key in "${REQUIRED_KEYS[@]}"; do
    if grep -q "^$key=" "$ENV_FILE"; then
        echo "✅ $key est configuré."
    else
        echo "⚠️  $key est MANQUANT."
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -eq 0 ]; then
    echo "✨ Environnement prêt pour l'orchestration."
else
    echo "❌ Il manque $MISSING clé(s). Veuillez mettre à jour .env.local"
fi
