# 🚀 Sprint 1 — Action Plan & Open Questions Answers
> Session : 2026-04-08 | Statut : Ready to execute

---

## Réponses aux 6 questions ouvertes

---

### Q1 — Obsidian / Syncthing / Chemin VPS ✅ RÉSOLU

**Situation** : Syncthing fonctionne VPS→Mac mais crée des conflits en sens inverse. 
**Décision** : Travailler directement sur le VPS via SSH. L'architecture doc vit sur VPS, Syncthing le rapatrie en lecture sur Mac.

**Structure de dossiers à créer sur VPS** :
```bash
# À exécuter sur VPS (ssh phil@31.97.67.145)
mkdir -p /home/phil/palanthai/content_creation-flywheels
mkdir -p /home/phil/palanthai/SEO
mkdir -p /home/phil/palanthai/content_creation-flywheels/docs
mkdir -p /home/phil/palanthai/content_creation-flywheels/prompts
mkdir -p /home/phil/palanthai/content_creation-flywheels/workflows
```

**Chemin cible du document d'architecture** :
```
/home/phil/palanthai/content_creation-flywheels/docs/FLYWHEEL_ARCHITECTURE_v1.md
```

**Pour WF-020 (RAG Sync)** : Le vault Obsidian Syncthing est probablement à :
```bash
# Vérifier où Syncthing sync le vault sur VPS
find /home/phil -name "00_COMMAND_CENTER.md" 2>/dev/null
# ou
ls /home/phil/SystemMac/ 2>/dev/null
ls /home/phil/sync/ 2>/dev/null
```

---

### Q3 — Notion Free Plan → Stratégie simplifiée ✅ DÉCISION PRISE

**Problème** : Notion free = pas de webhooks natifs.
**Solution adoptée** : **Supprimer Notion du pipeline n8n**. On garde Notion comme interface de lecture/édition humaine, mais le pipeline tourne entièrement sur **Supabase + Slack + Obsidian**.

**Architecture simplifiée (anti-fragile maximal)** :
```
AVANT (complexe) : Notion webhook → n8n → pipeline → Notion update
APRÈS (simple)   : Supabase content_queue → n8n → pipeline → Slack approval → publish
                   Notion = lecture seule (refreshed manuellement ou via n8n write toutes les heures)
```

**Comment tu interagis maintenant** :
- **Ajouter un sujet à traiter** → Insère dans Supabase `content_queue` directement OU via Slack command
- **Approuver un article** → Clic sur bouton Slack (déjà en place, WF-003 ✅)
- **Voir le pipeline** → Obsidian Kanban (`06_Content_Kanban.md`) syncthing-synced en lecture

**n8n polling Notion** (optionnel, pour garder le Content Calendar aligné) :
```
WF-XXX : Schedule toutes les 60 min
→ Fetch Notion Content Calendar (Status = "Brief")
→ INSERT into content_queue si pas déjà présent
→ Update Notion Status = "Queued"
```
Ce polling est sans webhook donc compatible free plan. Mais c'est optionnel — Supabase content_queue reste la source de vérité.

---

### Q4 — Comptes Dev Social Media : Ce qu'il faut faire

#### LinkedIn (priorité 1)
```
1. Va sur : https://www.linkedin.com/developers/apps/new
2. Crée une app "REcall Agency Social"
3. Sous "Products", demande accès à :
   - "Share on LinkedIn" (posts organiques - GRATUIT)
   - "Sign In with LinkedIn using OpenID Connect"
4. Dans "Auth", copie Client ID + Client Secret → mettre dans local-ai-packaged/.env
5. Obtiens un token OAuth2 (expire tous les 60 jours - besoin de refresh)
```

**Alternative si tu veux éviter l'OAuth LinkedIn** : Utilise [Phantombuster](https://phantombuster.com) (plan gratuit : 10 actions/mois) ou [Buffer](https://buffer.com) (free : 3 channels, 10 posts schedulés). Ces outils ont des APIs plus simples.

#### X/Twitter (priorité 2)  
```
1. Va sur : https://developer.x.com/en/portal/dashboard
2. Crée un projet + app "REcall Social"
3. Niveau requis : "Free" tier suffit pour poster (500 posts/mois)
4. Active "Read and Write" permissions
5. Dans "Keys and Tokens", copie :
   - API Key, API Secret
   - Access Token, Access Token Secret
   → Mettre dans local-ai-packaged/.env
```

**Alternative X** : n8n a un node X/Twitter natif qui gère OAuth2 automatiquement — pas besoin de gérer les tokens manuellement.

#### Facebook / Instagram (priorité 3 — Phase 2)
```
1. Va sur : https://developers.facebook.com/apps/
2. Crée une app "Business" type
3. Ajoute le produit "Instagram Graph API"
4. Nécessite : Facebook Page + Instagram Business Account liés
5. Permissions : pages_manage_posts, instagram_basic, instagram_content_publish
```

**Alternative recommandée si tu veux aller vite** :

| Outil | Platforms | Free tier | Intégration n8n |
|-------|-----------|-----------|-----------------|
| **Buffer** | LI + X + FB + IG | 3 channels, 10 posts | API REST simple |
| **Make (ex-Integromat)** | Tout | 1000 ops/mois | Webhook direct |
| **Zapier** | Tout | 100 tâches/mois | Hook |

**Ma recommandation** : Pour démarrer rapidement → commence avec **Buffer API** (1 compte gratuit, 3 channels). n8n envoie le post à Buffer qui gère l'OAuth et la publication. Quand le volume grandit → passe aux API natives.

---

### Q5 — GA4 Property ID ✅ CONFIRMÉ

GA4 est déjà configuré dans `/home/phil/local-ai-packaged/.env`.

**Pour vérifier** :
```bash
ssh phil@31.97.67.145 "grep -i 'GA4\|GOOGLE_ANALYTICS\|MEASUREMENT' /home/phil/local-ai-packaged/.env | sed 's/=.*/=***HIDDEN***/' "
```

**Ce qu'on a besoin pour le pipeline SEO** : Le FastAPI à `:8765` utilise déjà ces credentials via `/seo/pages`. Aucune action requise.

---

### Q6 — Clarification : Découplage `/content/generate` ✅ EXPLIQUÉ

**Ce que je demandais** : Actuellement, le endpoint `/content/generate` sur le FastAPI fait TOUT en un seul appel : brief → rédaction → score de qualité → création du draft WordPress. C'est une "boîte noire" monolithique.

**Pour le nouveau pipeline (WF-021)**, j'ai besoin que chaque agent soit un appel séparé :
```
Actuel (1 call) :
  n8n → POST /content/generate → { title, content, score, wp_post_id }

Cible (4 calls distincts) :
  n8n → POST /content/write     → { draft }        ← Writer seul
  n8n → POST /content/humanize  → { humanized }    ← Humanizer seul  
  n8n → POST /content/qc        → { scores, decision } ← QC seul
  n8n → POST /content/publish   → { wp_post_id }   ← Publish seul
```

**Pourquoi** : Pour que n8n puisse insérer de la logique entre chaque étape (retry QC, notifications Slack, update Notion, logging). Avec un seul call monolithique, on ne peut pas intervenir au milieu.

**Plan d'action** : Je vais créer ces nouveaux endpoints dans le fichier `palanthai_api.py` sur le VPS. Ça sera la tâche principale du Sprint 1, Item 2.

---

## SPRINT 1 — Plan d'exécution complet

### Durée estimée : 3-5 jours

---

### Item 1 — Structure VPS (30 min)
**Qui** : Phil (SSH) ou Claude via terminal

```bash
ssh phil@31.97.67.145 << 'EOF'

# Créer structure de dossiers
mkdir -p /home/phil/palanthai/content_creation-flywheels/{docs,prompts,workflows,agents}
mkdir -p /home/phil/palanthai/SEO

# Vérifier chemin du vault Obsidian syncthing
echo "=== Chercher vault Obsidian ==="
find /home/phil -name "00_COMMAND_CENTER.md" -not -path "*/.git/*" 2>/dev/null | head -3

# Vérifier structure palanthai existante  
echo "=== Structure palanthai actuelle ==="
ls -la /home/phil/palanthai/ 2>/dev/null || echo "Dossier palanthai introuvable, à créer"

# Vérifier les tables content_queue existantes
echo "=== Tables content pipeline ==="
docker exec -it supabase-db psql -U postgres -c "\dt public.*" 2>/dev/null | grep -E "content|pipeline|qc|performance|audit"

EOF
```

---

### Item 2 — Nouveaux endpoints FastAPI (2h)
**Fichier** : `/home/phil/palanthai/palanthai_api.py`

```bash
ssh phil@31.97.67.145 "wc -l /home/phil/palanthai/palanthai_api.py && tail -20 /home/phil/palanthai/palanthai_api.py"
```

**Endpoints à ajouter** (code à écrire dans la prochaine session) :
```python
# POST /content/write      → Writer Agent (LLM call avec brand voice prompt)
# POST /content/humanize   → Humanizer Agent (LLM call post-Writer)  
# POST /content/qc         → Quality Controller (LLM scoring, retourne JSON)
# POST /rag/query          → Qdrant search (obsidian_knowledge + faq_knowledge)
# POST /rag/ingest         → Upsert chunk dans Qdrant
# GET  /content/brand-voice?brand= → Retourne le prompt brand voice depuis env/fichier
```

---

### Item 3 — Nouvelles tables Supabase (30 min)

```bash
ssh phil@31.97.67.145 << 'EOF'
docker exec -it supabase-db psql -U postgres << 'SQL'

-- Pipeline execution log
CREATE TABLE IF NOT EXISTS content_pipeline_log (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    brand           TEXT NOT NULL,
    keyword         TEXT NOT NULL,
    notion_page_id  TEXT,
    n8n_run_id      TEXT,
    status          TEXT DEFAULT 'pending',
    researcher_brief JSONB,
    writer_draft    TEXT,
    humanized_draft TEXT,
    qc_scores       JSONB,
    qc_decision     TEXT,
    final_content   TEXT,
    wp_post_id      INT,
    published_url   TEXT,
    revision_count  INT DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- QC scores history
CREATE TABLE IF NOT EXISTS qc_scores_log (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    pipeline_run_id UUID,
    brand           TEXT,
    keyword         TEXT,
    revision_number INT DEFAULT 0,
    wiki_fidelity   REAL, seo_quality REAL, brand_voice REAL,
    humanness       REAL, originality REAL, readability REAL,
    eeat_signals    REAL, factual_accuracy REAL,
    weighted_score  REAL,
    decision        TEXT,
    issues          JSONB,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Performance tracking post-publication
CREATE TABLE IF NOT EXISTS performance_metrics (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    brand           TEXT NOT NULL,
    keyword         TEXT,
    published_url   TEXT NOT NULL,
    wp_post_id      INT,
    measured_at     DATE NOT NULL,
    days_after_pub  INT,
    gsc_clicks      INT DEFAULT 0,
    gsc_impressions INT DEFAULT 0,
    gsc_position    REAL,
    gsc_ctr         REAL,
    ga4_sessions    INT DEFAULT 0,
    ga4_bounce_rate REAL,
    social_score    REAL DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT now(),
    UNIQUE(published_url, measured_at)
);

-- Site audit snapshots
CREATE TABLE IF NOT EXISTS site_audits (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    brand           TEXT NOT NULL,
    audit_date      DATE NOT NULL,
    quick_wins      JSONB,
    content_gaps    JSONB,
    ctr_issues      JSONB,
    ux_issues       JSONB,
    opportunities   JSONB,
    report_url      TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Brand voice drift tracking
CREATE TABLE IF NOT EXISTS brand_voice_scores (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    brand           TEXT NOT NULL,
    article_url     TEXT,
    tone_match      REAL, vocabulary_compliance REAL,
    structure_pattern REAL, cta_style REAL,
    overall_score   REAL,
    drift_detected  BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE content_pipeline_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE qc_scores_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE site_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE brand_voice_scores ENABLE ROW LEVEL SECURITY;

-- Public select policies (n8n service role bypasses RLS anyway)
CREATE POLICY IF NOT EXISTS "service_all" ON content_pipeline_log FOR ALL USING (true);
CREATE POLICY IF NOT EXISTS "service_all" ON qc_scores_log FOR ALL USING (true);
CREATE POLICY IF NOT EXISTS "service_all" ON performance_metrics FOR ALL USING (true);
CREATE POLICY IF NOT EXISTS "service_all" ON site_audits FOR ALL USING (true);
CREATE POLICY IF NOT EXISTS "service_all" ON brand_voice_scores FOR ALL USING (true);

\echo '✅ Tables créées avec succès'
\dt public.content_pipeline_log
\dt public.qc_scores_log
\dt public.performance_metrics

SQL
EOF
```

---

### Item 4 — Qdrant : Créer collection `obsidian_knowledge` (15 min)

```bash
ssh phil@31.97.67.145 << 'EOF'
curl -X PUT "http://localhost:6333/collections/obsidian_knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": { "size": 384, "distance": "Cosine" },
    "optimizers_config": { "memmap_threshold": 20000 }
  }' && echo "✅ Collection obsidian_knowledge créée"

curl -X PUT "http://localhost:6333/collections/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": { "size": 384, "distance": "Cosine" }
  }' && echo "✅ Collection articles créée"

# Vérifier les collections existantes
curl -s "http://localhost:6333/collections" | python3 -m json.tool | grep name
EOF
```

---

### Item 5 — Copier l'architecture doc sur VPS

```bash
# Depuis Mac (terminal local)
scp ~/SystemMac/20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/FLYWHEEL_ARCHITECTURE_v1.md \
    phil@31.97.67.145:/home/phil/palanthai/content_creation-flywheels/docs/

scp ~/SystemMac/20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/SPRINT1_ACTION_PLAN.md \
    phil@31.97.67.145:/home/phil/palanthai/content_creation-flywheels/docs/
```

---

### Item 6 — Configurer WF-001 pour REcall (10 min dans n8n UI)

WF-001 est hardcodé `brand='reflexion'`. Cloner le workflow pour REcall :

```sql
-- Ajouter des keywords REcall dans la queue pour tester
INSERT INTO content_queue (brand, keyword, content_type, priority, status) VALUES
  ('recall', 'ai real estate automation', 'article', 90, 'pending'),
  ('recall', 'open source proptech stack', 'article', 80, 'pending'),
  ('recall', 'n8n property management workflow', 'article', 75, 'pending');
```

Dans n8n : dupliquer WF-001 → remplacer `brand = 'reflexion'` par `brand = 'recall'` → activer.

---

### Item 7 — Social Media : Actions minimales pour démarrer

**Recommandation : commencer avec Buffer (gratuit, 0 friction)**

```
1. Crée compte Buffer : buffer.com
2. Connecte : 1 LinkedIn Company Page + 1 X/Twitter account
3. Récupère l'API key Buffer dans Settings → API
4. Ajoute dans local-ai-packaged/.env :
   BUFFER_ACCESS_TOKEN=xxx
5. WF-012 appellera Buffer API au lieu des APIs natives
   → Buffer gère OAuth, scheduling, retry
```

**Buffer API endpoint (simple)** :
```bash
# Test post via Buffer
curl -X POST "https://api.bufferapp.com/1/updates/create.json" \
  -d "access_token=YOUR_TOKEN" \
  -d "profile_ids[]=PROFILE_ID" \
  -d "text=Test post from REcall pipeline"
```

**Quand passer aux API natives** : Quand le volume dépasse 10 posts/jour ou quand tu as besoin d'analytics détaillés. Pour l'instant Buffer = 0 setup friction.

---

## CHECKLIST SPRINT 1

```
□ Item 1 : Créer dossiers VPS + vérifier chemin vault Obsidian
□ Item 2 : Ajouter 6 nouveaux endpoints dans palanthai_api.py  
□ Item 3 : Créer 5 nouvelles tables Supabase
□ Item 4 : Créer collections Qdrant (obsidian_knowledge + articles)
□ Item 5 : Copier docs architecture sur VPS
□ Item 6 : Cloner WF-001 pour brand=recall + INSERT test keywords
□ Item 7 : Créer compte Buffer + connecter LI + X + ajouter token .env
```

**Temps total estimé** : 4-6h de travail concentré  
**Prérequis bloquants** : Accès SSH VPS ✅, accès n8n UI ✅, compte Buffer (5 min)

---

## PROCHAINE SESSION — Sprint 2

Une fois Sprint 1 complété, on construira :
1. `palanthai_api.py` — les 6 nouveaux endpoints (code complet)
2. WF-021 — Content Pipeline V2 dans n8n (avec les AI Agent nodes)
3. WF-020 — Obsidian RAG Sync (ingestion vault → Qdrant)
4. Hook WF-004 → WF-011 (activer la boucle sociale)

---

*Session 2026-04-08 — Prêt pour exécution*
