# 📸 Visionneuse d'Images - Listings

## 🎯 Qu'est-ce que c'est?

Un viewer web pour **voir toutes les photos de vos 44,988 listings** (899,760 images au total).

## 📍 Où se trouvent les images?

```
Table: units
├─ primary_image_url (1 image principale)
├─ images (array JSONB avec 20 photos)
└─ source_url (lien vers le listing)
```

**Statistiques:**
- ✅ 44,988 units
- ✅ 100% ont une image principale
- ✅ 100% ont la galerie (20 images)
- ✅ 100% ont la source URL

## 🚀 Comment accéder?

### Étape 1: Démarrer le tunnel SSH
```bash
ssh -L 3000:127.0.0.1:3000 phil@31.97.67.145 "sleep 600" &
```

### Étape 2: Ouvrir le viewer
```bash
open /Users/phil/Documents/Vaults/SystemMac/image_viewer.html
```

Ou double-cliquez sur le fichier `image_viewer.html`

### Étape 3: Charger les images
1. L'URL API doit être: `http://localhost:3000`
2. Choisissez le nombre par page (20-100)
3. Cliquez **"⚡ Charger"**

## 🎨 Fonctionnalités

- ✅ **Galerie interactive** - 20 listings par page (configurable)
- ✅ **Pagination** - Naviguer entre les pages
- ✅ **Clic sur image** - Agrandissement en plein écran
- ✅ **Lien vers source** - 🔗 Accès direct au listing original
- ✅ **Compteur photos** - Voir combien de photos par listing
- ✅ **Responsive** - Fonctionne sur mobile, tablette, desktop

## 📊 Structure des données

Chaque listing affiche:
```
┌─────────────────────┐
│  [Image Principale] │  ← primary_image_url
├─────────────────────┤
│ ID: abc123...       │
│ 📸 20 photos        │  ← Nombre de photos dans la galerie
│ 🔗 Source           │  ← Lien vers livephuket.com
└─────────────────────┘
```

## 🔗 Lien API utilisé

```
GET http://localhost:3000/units?
  select=id,primary_image_url,images,source_url
  &order=created_at.desc
  &limit=20
  &offset=0
```

## 🛠️ Dépannage

### "Connection refused"
- Vérifier le tunnel SSH est actif: `lsof -i :3000`
- Relancer: `ssh -L 3000:127.0.0.1:3000 phil@31.97.67.145 "sleep 600" &`

### Images ne chargeant pas
- Vérifier l'URL API est `http://localhost:3000`
- Attendre quelques secondes
- Recharger la page

### Afficher une galerie complète d'un listing
Pour voir les 20 photos d'un listing particulier:
```bash
curl http://localhost:3000/units?select=id,images&id=eq.UNIT_ID_HERE
```

## 💾 Données stockées

| Colonne | Type | Exemple |
|---------|------|---------|
| `id` | UUID | 2cf45e12-b8ea-51e9-b226-69c4f611722e |
| `primary_image_url` | URL | https://cdn.fazwaz.com/.../belle-rama-94.jpg |
| `images[0]` | URL | https://cdn.fazwaz.com/.../kitchen-photo.png |
| `images[20]` | URL | https://cdn.fazwaz.com/.../view.jpg |
| `source_url` | URL | https://www.livephuket.com/property-sales/... |

## 📌 Variantes d'URL

Les images viennent du CDN FazWaz avec différents formats:

```
Original (haute résolution):
https://cdn.fazwaz.com/nw/-aofMVT74x0kv6TH0EzSZFQi900/0x0/...

Thumbnail (270x146):
https://cdn.fazwaz.com/nw/02q5AZI1OlYrM6pITgRFh3blK9s/270x146/...

Custom (267x175):
https://cdn.fazwaz.com/nw/2O9jS8wMN-9dfPu3_vgj6L2G62k/267x175/...
```

Le viewer utilise les images telle qu'elles sont stockées en base.

## ✅ Prêt!

Lancez le tunnel, ouvrez le fichier HTML, et commencez à explorer! 🎉

