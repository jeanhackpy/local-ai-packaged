# 📊 Setup - Listings avec Photos

## 🎯 Objectif

Consulter vos 44,988 listings avec 899,760 photos directement dans un tableau web interactif.

## 📋 Prérequis

- Tunnel SSH actif
- Clé API ANON_KEY de Supabase
- Navigateur web

---

## 🚀 Setup (5 minutes)

### Étape 1: Démarrer le tunnel SSH

Remplacez `3000:127.0.0.1:8000` - cela crée un pont entre votre port 3000 local et Kong gateway (port 8000) sur le VPS.

```bash
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &
```

**Vérifier le tunnel:**
```bash
lsof -i :3000
# Vous devez voir: ssh LISTEN
```

---

### Étape 2: Obtenir la clé ANON_KEY

**Option A: Via SSH (recommandé)**
```bash
ssh phil@31.97.67.145 "grep ANON_KEY ./local-ai-packaged/.env"
```

Copier la valeur complète après `ANON_KEY=`

**Option B: Via Docker**
```bash
ssh phil@31.97.67.145 "docker exec supabase-rest env | grep ANON"
```

---

### Étape 3: Ouvrir le viewer HTML

```bash
open /Users/phil/Documents/Vaults/SystemMac/listings_with_photos.html
```

Ou double-cliquez sur le fichier dans Finder.

---

### Étape 4: Configurer et charger

1. **API URL**: `http://localhost:3000` (déjà pré-rempli)
2. **Clé API**: Collez la valeur d'`ANON_KEY` ✅
3. **Lignes par page**: 10 (configurable 1-50)
4. **Décalage**: 0 (pour pagination)
5. Cliquez **"📡 Charger"** 🎯

---

## 📊 Interface

| Colonne | Contenu |
|---------|---------|
| **Photo** | Image principale cliquable (120×90px) |
| **Galerie** | 5 premières photos miniaturisées + compteur |
| **ID** | UUID du listing |
| **Source** | 🔗 Lien vers le listing original |

**Interactions:**
- 🖱️ Cliquez une photo → Agrandissement modal
- ⬅️ ➡️ Boutons de pagination
- ESC → Fermer le modal

---

## 🔑 Clés API expliquées

### ANON_KEY (publique)
- Utilisée pour les requêtes non-authentifiées
- Permet: SELECT sur les données publiques
- ✅ À utiliser pour ce viewer

### SERVICE_ROLE_KEY (admin)
- Accès complet (INSERT, UPDATE, DELETE)
- ❌ Ne pas partager
- À utiliser uniquement côté serveur

---

## ⚠️ Dépannage

### "No API key found in request"
**Problème**: Clé API manquante ou invalide
**Solution**: 
```bash
# 1. Vérifier la clé API
ssh phil@31.97.67.145 "grep ANON_KEY ./local-ai-packaged/.env" | head -c 80

# 2. Copier exactement la valeur (sans ANON_KEY=)
# 3. Coller dans le champ "Clé API" du viewer
```

### "Connection refused" sur port 3000
**Problème**: Tunnel SSH non actif
**Solution**:
```bash
# 1. Vérifier
lsof -i :3000

# 2. Si rien, relancer
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &
```

### Aucune image ne charge
**Problème**: Images CDN indisponibles
**Solution**: C'est normal pour certaines photos. Le CDN FazWaz peut avoir des TTL élevés. Relancer dans 5 min ou changer de listing.

### "Aucun résultat"
**Problème**: Offset hors limites
**Solution**: Réinitialiser le décalage à 0 et recharger

---

## 🔗 API Endpoints

Pour d'autres requêtes directes:

```bash
# Avec la clé API
ANON="eyJhbGciOi..."
curl -H "apikey: $ANON" 'http://localhost:3000/rest/v1/units?limit=5'

# Toutes les colonnes d'un listing
curl -H "apikey: $ANON" 'http://localhost:3000/rest/v1/units?select=*&limit=1'

# Filtrer par ville/région
curl -H "apikey: $ANON" 'http://localhost:3000/rest/v1/units?city=eq.Bangkok&limit=10'
```

---

## 💡 Cas d'usage

### 1. Voir toutes les photos d'un listing complet
Cliquez sur les 5 miniatures → Voir les 20 photos dans le modal → Cliquez "Suivant" pour naviguer parmi les images

### 2. Exporter les métadonnées
```bash
curl -H "apikey: $ANON" \
  'http://localhost:3000/rest/v1/units?select=id,primary_image_url,images,source_url' \
  > listings.json
```

### 3. Compter les photos par ville
```sql
SELECT city, COUNT(*) as listings, AVG(JSONB_ARRAY_LENGTH(images)) as avg_photos
FROM units
GROUP BY city
ORDER BY listings DESC;
```

---

## ✅ Checklists

### Avant de commencer
- [ ] SSH local configuré (`ssh-keygen` si nécessaire)
- [ ] Accès VPS confirmé (`ssh phil@31.97.67.145`)
- [ ] Port 3000 libre localement (`lsof -i :3000`)

### Setup
- [ ] Tunnel SSH actif (`lsof -i :3000` → ssh LISTEN)
- [ ] ANON_KEY copiée correctement
- [ ] HTML file accessible (`listings_with_photos.html`)
- [ ] Navigateur actualisé (F5 ou Cmd+R)

### Troubleshooting
- [ ] Tunnel re-démarré
- [ ] API URL = http://localhost:3000
- [ ] Clé API collée (view-source si doute)
- [ ] Limit = 10-20 (pas trop grand)

---

## 📞 Support rapide

**Tunnel ne démarre pas?**
```bash
# Tuer tous les tunnels existants
killall ssh

# Relancer
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &
```

**Clé API invalide?**
```bash
# Générer une nouvelle (si nécessaire)
ssh phil@31.97.67.145 "docker exec supabase-db psql -U postgres -c 'SELECT ...'"
```

**Tunnel OK mais pas de données?**
```bash
# Tester avec curl
curl -H "apikey: YOUR_KEY_HERE" http://localhost:3000/rest/v1/units?limit=1
```

---

## 🎉 Prêt!

Vous avez maintenant accès complet à vos 44,988 listings avec 899,760 photos dans un tableau interactif!

**Caractéristiques:**
- ✅ Photos en temps réel
- ✅ Pagination rapide
- ✅ Modale agrandie
- ✅ Liens sources
- ✅ Responsive (mobile/desktop)

Bon navire! 🚢
