# 🔄 Content Creation Flywheel — Architecture & Documentation

> Créé: 2026-03-29 | Statut: Phase 0 déployée, Phase 1 en cours

---

## Vue d'ensemble

Le **Content Creation Flywheel** est un système autonome qui transforme chaque article publié en actifs sociaux distribués sur plusieurs plateformes, puis récupère les données d'engagement pour prioriser les futurs sujets de contenu.

**L'effet composé:** chaque cycle améliore le suivant — plus on publie, plus on apprend ce qui résonne, plus le prochain article est ciblé.

---

## Principe 10:80:10

```
10%  →  Will & Decision (Phil)     : choisir les sujets, approuver les posts
80%  →  AI Execution (Pipeline)    : rédaction, atomisation, distribution
10%  →  Feedback Loop (Analytics)  : GSC + engagement social → priorisation
```

---

## Architecture Globale

```
   ┌─────────────────────────────────────────────────────────┐
   │                    MARQUES × PLATEFORMES                │
   │  REcall (EN)      → LinkedIn + Twitter                  │
   │  Réflexion (FR)   → LinkedIn + Twitter + FB + Instagram │
   │  PatrimonAsia (FR)→ LinkedIn (Phase 3)                  │
   └─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   SEO DATA (GSC)        ARTICLE                ENGAGEMENT
   ← impressions         CREATION               DATA
   ← clicks              WF-001→004             ← impressions
   ← positions           ↓                      ← likes/shares
        │           PUBLICATION WP              ← clicks
        │           + Qdrant + IndexNow              │
        │                │                           │
        └────────────────▼───────────────────────────┘
                         │
                    ┌────▼────┐
                    │ WF-011  │  CONTENT ATOMIZER
                    │         │  1 article → N social posts
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │  SLACK  │  Review: Approve / Reject
                    │ Review  │  (10% human decision)
                    └────┬────┘
                         │ approved
                    ┌────▼────┐
                    │ WF-012  │  SOCIAL DISTRIBUTOR
                    │         │  Every 2h, 08:00-20:00 ICT
                    └────┬────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          LinkedIn    Twitter    Facebook/Instagram
              │          │          │
              └──────────┴──────────┘
                         │
                    ┌────▼────┐
                    │ WF-015  │  PERFORMANCE TRACKER (Phase 2)
                    │ daily   │  fetch metrics → update social_score
                    └────┬────┘
                         │
                 ┌───────▼────────┐
                 │ content_subjects│  social_score updated
                 │ priority boost  │  → next WF-010 run
                 └────────────────┘
```

---

## Composants Techniques

### Infrastructure VPS (`31.97.67.145`)

| Fichier | Rôle |
|---------|------|
| `/home/phil/palanthai/palanthai_api.py` | FastAPI app (port 8765), endpoint `/content/atomize` |
| `/home/phil/palanthai/content/social_atomizer.py` | Moteur d'atomisation (LLM multi-fallback) |
| `/home/phil/palanthai/content/recall/social-voice.md` | Voix de marque REcall pour social |
| `/home/phil/palanthai/content/reflexion/social-voice.md` | Voix de marque Réflexion pour social |

### Endpoint d'atomisation

```http
POST http://172.18.0.1:8765/content/atomize
Content-Type: application/json

{
  "article_title": "...",
  "article_content": "...",
  "article_url": "https://recall-agency.com/...",
  "brand": "recall",
  "language": "en",
  "platforms": ["linkedin", "twitter"],
  "article_id": "uuid",
  "queue_id": "uuid"
}
```

**Retourne:** array de social posts `{ platform, post_type, content, hashtags }`

### Modèle LLM (4-tier fallback via `model_config.py`)

```
1. Groq (rapide, gratuit)
2. NVIDIA API
3. Gemini
4. OpenRouter (backup)
```

---

## Stockage: Airtable Social Flywheel

**Base:** `appDxwFpJXwWM2fgq` (recall-agency workspace)
**Table:** Social Flywheel (`tbletF71ZERgGuZG9`)

### Champs clés

| Champ | Type | Valeurs |
|-------|------|---------|
| `post_status` | Select | `pending_review` → `approved` → `posted` |
| `brand` | Select | recall / reflexion / patrimonasia |
| `platform` | Select | linkedin / twitter / facebook / instagram |
| `post_type` | Select | single / thread / carousel / story |
| `content` | Long text | Le texte du post |
| `scheduled_at` | DateTime | Heure de publication planifiée (Bangkok TZ) |
| `platform_post_id` | Text | ID retourné par l'API plateforme |
| `impressions/likes/shares/clicks` | Number | Métriques d'engagement |
| `engagement_rate` | Percent | Calculé automatiquement |

---

## Workflows n8n

### WF-011 — CONTENT-ATOMIZER
**ID:** `aQE390zbkHQ0gN8K`
**Trigger:** Webhook `POST /wf011-atomize` (appelé par WF-004 après publication)

```
Webhook → Call /content/atomize → Split Posts → Save to Airtable → Slack notify
```

**Slack message:** "5 social assets ready for [article_title]" avec boutons Approve/Review/Reject

### WF-012 — SOCIAL-DISTRIBUTOR
**ID:** `cIIqsEqQqDKHCxHy`
**Trigger:** Toutes les 2h de 08:00 à 20:00 ICT

```
Schedule → Fetch next approved post → Route by platform → POST /social/post → Mark posted → Slack
```

**Routing:** LinkedIn / Twitter / Facebook / Instagram → VPS endpoint `/social/post`

> ⚠️ `/social/post` sur le VPS n'est pas encore créé (Phase 1)

### WF-004 → WF-011 (lien à créer)
Après publication WordPress, WF-004 doit déclencher WF-011:

```json
POST https://n8n.recall-agency.com/webhook/wf011-atomize
{
  "article_title": "{{ $json.title }}",
  "article_content": "{{ $json.content }}",
  "article_url": "{{ $json.url }}",
  "brand": "reflexion",
  "language": "fr",
  "article_id": "{{ $json.article_id }}",
  "queue_id": "{{ $json.queue_id }}"
}
```

---

## Formule d'Atomisation par Article

| Asset | Nombre | Plateforme | Phase |
|-------|--------|------------|-------|
| Post LinkedIn insight | 3-5 | LinkedIn | ✅ 1 |
| Tweet standalone | 5-10 | Twitter/X | ✅ 1 |
| Thread X | 1 | Twitter/X | ✅ 1 |
| Post Facebook | 1-2 | Facebook | 🔜 2 |
| Carousel Instagram | 1-2 | Instagram | 🔜 2 |
| Newsletter block | 1 | Email | 🔜 4 |

---

## Boucle de Feedback

```
WF-015 (daily 23:00 UTC):
  → Fetch posted social_posts des 7 derniers jours
  → API calls: LinkedIn/Twitter/FB metrics
  → UPDATE social_posts: impressions, likes, shares, clicks
  → Aggregate par article → compute social_score
  → UPDATE content_subjects SET social_score
  → Weekly Slack digest (dimanche avec WF-007)

WF-010 (weekly):
  → Priority = gsc_impressions * 0.5 + social_score * 0.5
  → Sujets à fort engagement social remontent dans la queue
```

---

## Phases de Déploiement

| Phase | Quoi | Statut |
|-------|------|--------|
| **0** | Airtable table + API endpoint + WF-011/012 créés | ✅ Complété |
| **1** | Hook WF-004→011, tester atomisation réelle, créer `/social/post` | 🔄 En cours |
| **2** | FB/Instagram, PatrimonAsia launch, WF-015 performance tracker | ⏳ À venir |
| **3** | LINE Official Account, newsletter WF-014, A/B testing | ⏳ À venir |

---

## Coût Mensuel Estimé

| Item | Coût |
|------|------|
| LinkedIn / Twitter / FB / Instagram API | Gratuit |
| OpenRouter (LLM atomisation, ~$5-10/mois) | ~$5-10 |
| **Total incrémental** | **~$5-10/mois** |

---

## Checklist Activation

- [x] `palanthai_api.py` — endpoint `/content/atomize` ajouté (ligne 932)
- [x] `social_atomizer.py` — moteur d'atomisation créé
- [x] `social-voice.md` REcall + Réflexion — voix de marque créées
- [x] Airtable Social Flywheel table — créée avec tous les champs
- [x] WF-011 CONTENT-ATOMIZER — créé dans n8n
- [x] WF-012 SOCIAL-DISTRIBUTOR — créé dans n8n
- [ ] **Redémarrer palanthai_api** (fix endpoint 404 actif mais API pas rechargée)
- [ ] **Hook WF-004 → WF-011** (ajouter node HTTP Request dans WF-004)
- [ ] **Configurer credentials Airtable** dans WF-011 et WF-012
- [ ] **Publier WF-011 et WF-012** (actuellement en draft inactif)
- [ ] **Créer `/social/post`** sur VPS (Phase 1)
- [ ] **Enregistrer comptes dev** LinkedIn + Twitter (action manuelle Phil)
