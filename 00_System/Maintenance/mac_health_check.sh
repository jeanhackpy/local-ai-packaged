#!/bin/bash

# Fichier de destination dans Obsidian
HEALTH_NOTE="/Users/phil/Documents/Vaults/SystemMac/00_System/OS_Health_Status.md"

echo "# 🖥️ macOS Health Status" > "$HEALTH_NOTE"
echo "*Dernière mise à jour : $(date '+%Y-%m-%d %H:%M:%S')*" >> "$HEALTH_NOTE"
echo "" >> "$HEALTH_NOTE"

echo "## 📊 Statistiques Système" >> "$HEALTH_NOTE"
echo "- **Uptime** : $(uptime | awk -F', ' '{print $1}')" >> "$HEALTH_NOTE"
echo "- **Charge CPU** : $(sysctl -n vm.loadavg | awk '{print $2}')" >> "$HEALTH_NOTE"
echo "- **Mémoire Vive** : $(top -l 1 | grep PhysMem | awk '{print $2 " utilisées, " $6 " libres"}')" >> "$HEALTH_NOTE"

echo "" >> "$HEALTH_NOTE"
echo "## 💾 Espace Disque" >> "$HEALTH_NOTE"
df -h / | awk 'NR==2 {print "- **Disque Principal** : " $3 "/" $2 " utilisé (" $5 ")"}' >> "$HEALTH_NOTE"

echo "" >> "$HEALTH_NOTE"
echo "## 🧹 Maintenance à prévoir" >> "$HEALTH_NOTE"
if [ $(df / | awk 'NR==2 {print $5}' | sed 's/%//') -gt 85 ]; then
    echo "- ⚠️ **Alerte Disque** : Nettoyage urgent des caches requis." >> "$HEALTH_NOTE"
else
    echo "- ✅ **Disque** : Espace suffisant." >> "$HEALTH_NOTE"
fi

echo "✅ Santé Mac mise à jour dans Obsidian."
