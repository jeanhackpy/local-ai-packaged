# 🤖 AI Image Tagging Pipeline pour Listings

## 🎯 Objectif

Analyser automatiquement vos **44,988 images** avec Claude Vision pour extraire:
- **Standing** (luxury, premium, standard, budget, affordable)
- **Décoration** (modern, minimalist, classic, bohemian, industrial, etc.)
- **Type de pièce** (bedroom, kitchen, bathroom, living, etc.)
- **État** (excellent, good, fair, needs_work)
- **Commodités visibles** (pool, garden, aircon, etc.)
- **Couleurs dominantes**

Résultat: **Recherche affinée** par standing/décoration/type de bien

---

## 📦 Fichiers créés

### 1. `image_tagging_pipeline.py`
Pipeline d'analyse batch avec Claude Vision

**Fonctionnalités:**
- Lit les images depuis la DB (units table)
- Analyse chaque image avec Claude 3.5 Vision
- Stocke les tags dans `unit_image_tags` table
- Rate-limited (respecte les limites API)
- Progress tracking + estimation temps restant

**Usage:**
```bash
# Setup
pip install anthropic psycopg2-binary python-dotenv

# Démarrer le pipeline
python3 image_tagging_pipeline.py

# Exemple: 44,988 images × 0.5s = ~6 heures
```

### 2. `search_api.py`
API REST pour rechercher par tags

**Endpoints:**

#### GET `/search/listings`
Rechercher les listings par critères

```bash
# Luxury apartments avec décoration moderne
curl "http://localhost:5001/search/listings?standing=luxury&decoration=modern"

# Bedrooms en bon état
curl "http://localhost:5001/search/listings?room_type=bedroom&condition=good"

# Listings avec piscine, jardin
curl "http://localhost:5001/search/listings?amenity=pool&amenity=garden"

# Combiner filtres
curl "http://localhost:5001/search/listings?standing=premium&decoration=contemporary&room_type=kitchen&min_confidence=0.7&limit=50"
```

#### GET `/search/filters`
Récupérer les options de filtrage disponibles

```bash
curl "http://localhost:5001/search/filters"
# Response:
# {
#   "standings": ["affordable", "budget", "premium", "standard"],
#   "decorations": ["bohemian", "classic", "minimalist", "modern", "industrial"],
#   "room_types": ["bedroom", "kitchen", "bathroom", "living_room"],
#   "amenities": ["pool", "garden", "aircon", "balcony"],
#   ...
# }
```

#### GET `/stats`
Stats de tagging

```bash
curl "http://localhost:5001/stats"
```

---

## 🚀 Setup complet (5 étapes)

### Étape 1: Installer dépendances

```bash
pip install anthropic psycopg2-binary python-dotenv flask flask-cors
```

### Étape 2: Configurer .env

Ajouter à votre `.env.local` ou créer `.env`:

```dotenv
# Database
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password

# Claude API
ANTHROPIC_API_KEY=sk-ant-...
```

### Étape 3: Créer les tables

```bash
# Via SSH tunnel
ssh -L 5432:127.0.0.1:5432 phil@31.97.67.145 "sleep 600" &

# Le script crée automatiquement la table unit_image_tags
```

### Étape 4: Lancer le pipeline

```bash
python3 image_tagging_pipeline.py
```

**Monitoring:**
- Logs en temps réel
- Progress: `offset: 0 to 10... offset: 10 to 20...`
- Temps estimé restant
- Ctrl+C pour arrêter (peut reprendre)

### Étape 5: Lancer l'API de recherche

```bash
python3 search_api.py
# Listening on http://localhost:5001
```

---

## 📊 Schéma DB

```sql
CREATE TABLE unit_image_tags (
    id UUID PRIMARY KEY,
    unit_id UUID REFERENCES units(id),
    image_url TEXT,
    
    -- Tags analysés
    standing VARCHAR(50),              -- luxury, premium, standard, budget
    decoration_style VARCHAR(100),     -- modern, minimalist, classic, etc.
    room_type VARCHAR(100),            -- bedroom, kitchen, etc.
    colors TEXT[],                     -- ['white', 'blue', 'wood']
    condition VARCHAR(50),             -- excellent, good, fair
    amenities TEXT[],                  -- ['pool', 'garden']
    
    -- Metadata
    confidence FLOAT,                  -- 0.5-1.0 (score de fiabilité Claude)
    tags_json JSONB,                   -- Réponse brute de Claude
    tagged_at TIMESTAMP
);

-- Indexes pour performances
CREATE INDEX idx_unit_tags ON unit_image_tags(unit_id);
CREATE INDEX idx_standing ON unit_image_tags(standing);
CREATE INDEX idx_decoration ON unit_image_tags(decoration_style);
```

---

## 💰 Coûts & Performance

### Analyse 44,988 images

| Métrique | Valeur |
|----------|--------|
| **Coût par image** | $0.01-0.02 |
| **Coût total** | ~$450-900 |
| **Temps** | ~6-8 heures |
| **Rate limit** | 0.5s entre les appels |

### Optimisations si budget limité

**Option 1: Sampling** (20% des images)
- 9,000 images = ~$90-180
- Générer les tags manquants via copie/interpolation

**Option 2: Par catégorie**
- Tagguer seulement les listings "phares" d'abord
- 5,000 images = ~$50-100

**Option 3: Fine-tuning** (rentable à l'échelle)
- Coût initial: $1000-2000
- Ensuite: $0.001-0.005 par image (10x moins cher)

---

## 🔍 Cas d'usage

### 1. Recherche par standing
```bash
# "Je veux du luxury uniquement"
curl "http://localhost:5001/search/listings?standing=luxury&limit=20"
```

### 2. Recherche par décoration
```bash
# "Je veux du moderna minimalist"
curl "http://localhost:5001/search/listings?decoration=minimalist&decoration=modern"
```

### 3. Recherche par pièce + commodités
```bash
# "Je veux une cuisine contemporaine avec tous les équipements"
curl "http://localhost:5001/search/listings?room_type=kitchen&decoration=contemporary&amenity=aircon&amenity=moden_appliances"
```

### 4. Recherche avancée
```bash
# "Je veux du premium en bon état, avec piscine et jardin"
curl "http://localhost:5001/search/listings?standing=premium&condition=good&amenity=pool&amenity=garden&min_confidence=0.8"
```

---

## 🛠️ Troubleshooting

### "ANTHROPIC_API_KEY not found"
```bash
# Ajouter à .env
export ANTHROPIC_API_KEY="sk-ant-..."

# Ou dans .env.local
ANTHROPIC_API_KEY="sk-ant-..."
```

### "Connection to database failed"
```bash
# Vérifier tunnel SSH
ssh -L 5432:127.0.0.1:5432 phil@31.97.67.145 "sleep 600" &

# Ou SSH config
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &
```

### "Rate limit exceeded"
- Claude Vision: limite ~50k tokens/minute
- Script respecte 0.5s par image (configurable)
- Réduire si besoin: `time.sleep(0.2)`

### Pipeline crash - reprendre?
- Stocke `unit_id` dans DB
- Script peut reprendre (ne re-traite pas déjà taggés)
- Relancer: `python3 image_tagging_pipeline.py`

---

## 📈 Monitoring & Stats

**Pendant le pipeline:**
```
🎯 Real Estate Image Tagging Pipeline
==================================================

📊 Processing batch: 0 to 10
  🖼️  Unit abc123 - Image 1/6... ✅ luxury|modern
  🖼️  Unit abc123 - Image 2/6... ✅ premium|contemporary
  
📈 Total processed: 127 images
⏱️  Estimated time remaining: 5.8 hours
```

**Après (via API):**
```bash
curl "http://localhost:5001/stats"
# {
#   "total_tags": 44988,
#   "units_tagged": 44988,
#   "avg_confidence": 0.78,
#   "first_tag": "2026-04-04T12:00:00",
#   "last_tag": "2026-04-04T18:00:00"
# }
```

---

## 🎯 Prochaines étapes

1. ✅ Pipeline d'analyse (ce document)
2. ✅ API de recherche (ce document)
3. 📝 **Web UI** pour recherche interactive
4. 📝 **Dashboard** de stats par standing/décoration
5. 📝 **Recommandations** basées sur "listings similaires"
6. 📝 **Export** listings filtrés → CSV/PDF

---

## ✅ Résumé

Système complet **Vision+AI** pour tagguer et rechercher vos listings:

- **Pipeline**: Analyse 44,988 images avec Claude Vision
- **DB**: Stocke standing, décoration, types de pièces, commodités
- **API**: Recherche filtrée par critères
- **Coût**: ~$450-900 pour tout (ou $50-100 en sampling)
- **Temps**: ~6-8 heures d'exécution
- **ROI**: Recherche affinée = meilleures conversions pour clients

Ready to deploy! 🚀
