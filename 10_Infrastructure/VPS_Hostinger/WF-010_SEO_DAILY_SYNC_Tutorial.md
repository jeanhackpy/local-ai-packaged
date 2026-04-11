# WF-010 — Cours d'utilisation : SEO Daily Sync

> **Workflow actif** | Déclenchement : tous les jours à 01h00 UTC (08h00 ICT)
> ID n8n : hVpZwgBhZ2Hbxs1s | Lien : https://n8n.recall-agency.com

---

## Vue d'ensemble

WF-010-SEO-DAILY-SYNC est le **pipeline de collecte SEO automatique** pour reflexion.asia.

Son rôle : chaque matin, il interroge l'API locale de performance SEO, agrège les données Google Search Console + Google Analytics 4, envoie un rapport Slack, et alimente automatiquement la file d'attente de contenu (table `content_queue` dans Postgres).

C'est le **déclencheur principal** de toute la chaîne de production de contenu — sans lui, WF-001 et WF-002 n'ont rien à traiter.

---

## Architecture : les 8 noeuds

```
[Schedule 01:00]
    → [Sync GSC Subjects]        → POST /seo/sync-subjects
    → [Fetch GSC Keywords]       → GET  /seo/keywords
    → [Fetch GA4 Pages]          → GET  /seo/pages
    → [Merge Data]               → Agrégation (append mode)
    → [Build Report]             → Construction rapport JS
    → [Slack Report]             → POST webhook Slack #C023FGKE9AP
    → [Auto-Queue Opportunities] → INSERT INTO content_queue (Postgres)
```

### Noeud 1 — Schedule Trigger
- **Type** : scheduleTrigger
- **Heure** : 01:00 UTC = **08:00 heure de Bangkok (ICT)**
- Se déclenche automatiquement sans intervention manuelle
- Déclenchement manuel possible via le bouton "Execute Workflow" dans l'UI n8n

### Noeud 2 — Sync GSC Subjects
- **Type** : httpRequest (POST)
- **URL** : `http://172.18.0.1:8765/seo/sync-subjects?brand=reflexion`
- `172.18.0.1` = IP gateway Docker host (service Python/FastAPI tournant sur le VPS hôte)
- Action : synchronise les sujets/topics depuis Google Search Console vers la BDD locale
- Résultat : met à jour la liste des requêtes de recherche actives pour la journée

### Noeud 3 — Fetch GSC Keywords
- **Type** : httpRequest (GET)
- **URL** : `http://172.18.0.1:8765/seo/keywords?brand=reflexion&limit=100`
- Retourne les 100 meilleurs mots-clés GSC (impressions, clics, position moyenne)
- Format JSON : array de `{keyword, impressions, clicks, position, url}`

### Noeud 4 — Fetch GA4 Pages
- **Type** : httpRequest (GET)
- **URL** : `http://172.18.0.1:8765/seo/pages?brand=reflexion&limit=20`
- Retourne les 20 pages les plus performantes GA4 (sessions, bounce rate, temps)
- Format JSON : array de `{url, sessions, bounce_rate, avg_duration}`

### Noeud 5 — Merge Data
- **Type** : merge (mode append)
- Combine les outputs des noeuds 3 et 4 en un seul flux de données
- Concaténation brute — pas de transformation à ce stade

### Noeud 6 — Build Report
- **Type** : code (JavaScript)
- Construit le message de rapport Slack formaté
- Calcule les métriques clés : top opportunités, pages en baisse, nouveaux mots-clés
- Prépare aussi les entrées candidates pour `content_queue`

### Noeud 7 — Slack Report
- **Type** : httpRequest (POST)
- **Destination** : Canal Slack ID `C023FGKE9AP`
- Envoie le rapport quotidien SEO : keywords en hausse, pages à optimiser, opportunités détectées
- Tu reçois ce message chaque matin à ~08h ICT si tout fonctionne ✅

### Noeud 8 — Auto-Queue Opportunities
- **Type** : postgres
- **Action** : INSERT INTO `content_queue`
- Insère automatiquement les opportunités de contenu identifiées par le rapport
- Ces entrées sont ensuite consommées par **WF-001** (Research Brief) puis **WF-002** (Generate Article)

---

## L'API locale : 172.18.0.1:8765

Cette IP est le **gateway Docker** — c'est ainsi que les containers n8n accèdent aux services tournant directement sur l'hôte VPS (hors Docker).

Le service FastAPI/Python écoute sur le port 8765 et sert d'intermédiaire entre Google APIs et n8n.

**Endpoints utilisés par WF-010 :**

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/seo/sync-subjects` | POST | Sync sujets GSC → BDD locale |
| `/seo/keywords` | GET | Top keywords GSC avec métriques |
| `/seo/pages` | GET | Top pages GA4 avec métriques |

**Pour vérifier que l'API est up (depuis le VPS) :**
```bash
curl http://localhost:8765/health
curl "http://172.18.0.1:8765/seo/keywords?brand=reflexion&limit=5"
```

---

## La table content_queue (Postgres)

WF-010 est le **producteur** de la queue. WF-001 et WF-002 sont les **consommateurs**.

Structure typique d'une entrée insérée :
```sql
INSERT INTO content_queue (
  brand,        -- 'reflexion'
  keyword,      -- mot-clé cible
  priority,     -- score calculé (impressions × gap de position)
  status,       -- 'pending'
  created_at    -- timestamp auto
)
```

**Pour voir la queue en direct (SSH VPS) :**
```bash
docker exec -it supabase-db psql -U postgres -c \
  "SELECT keyword, priority, status FROM content_queue WHERE brand='reflexion' ORDER BY priority DESC LIMIT 20;"
```

---

## Connexion avec le reste du pipeline palanthai

```
WF-010  SEO Daily Sync          → alimente content_queue
    ↓
WF-001  Research Brief          → lit content_queue, génère brief via Ollama
    ↓
WF-003  Human Review            → webhook de validation manuelle (toi)
    ↓
WF-002  Generate Article        → génère article complet via Ollama
    ↓
WF-004  Publish WordPress       → publie sur reflexion.asia
    ↓
WF-007  SEO Performance         → mesure les résultats J+7/J+30
    ↓
WF-010  récupère ces performances le lendemain → boucle fermée ♻️
```

**Workflows en attente d'activation :**
- WF-011 : Content Atomizer (transforme articles en formats courts)
- WF-012 : Social Distributor (distribution multi-canal)

---

## Comment monitorer

### Via l'interface n8n
URL : https://n8n.recall-agency.com

1. Menu gauche → **Executions**
2. Filtrer par workflow "WF-010-SEO-DAILY-SYNC"
3. Statut : ✅ Success | ❌ Error | ⏳ Running
4. Cliquer sur une exécution pour inspecter chaque noeud et son output JSON

### Via le rapport Slack quotidien
- Message reçu chaque matin vers 08h ICT = confirmation que tout tourne
- Absence de message = problème à investiguer immédiatement

### Via SSH (logs Docker)
```bash
ssh phil@31.97.67.145
docker logs n8n --tail=50 | grep -i "WF-010\|SEO\|error"
```

---

## Déclencher manuellement

### Via l'UI n8n (recommandé)
1. Aller sur https://n8n.recall-agency.com
2. Ouvrir le workflow **WF-010-SEO-DAILY-SYNC**
3. Cliquer sur **"Execute Workflow"** (bouton ▶ en haut à droite)
4. Observer les noeuds s'allumer en vert un par un en temps réel

### Via l'API n8n (avancé)
```bash
WORKFLOW_ID="hVpZwgBhZ2Hbxs1s"

curl -X POST "https://n8n.recall-agency.com/api/v1/workflows/${WORKFLOW_ID}/run" \
  -H "X-N8N-API-KEY: <ton-api-key>" \
  -H "Content-Type: application/json"
```

---

## Troubleshooting courant

| Symptôme | Cause probable | Solution |
|----------|---------------|---------|
| Pas de message Slack le matin | Workflow failed ou API down | Vérifier Executions dans n8n + `curl http://localhost:8765/health` sur VPS |
| Noeud "Sync GSC Subjects" échoue | API locale down | `ssh phil@31.97.67.145` → `ps aux \| grep python` |
| Noeud "Fetch Keywords" retourne vide | Credentials Google expirées | Vérifier les credentials Google dans n8n → Settings → Credentials |
| `content_queue` ne se remplit pas | Aucune opportunité trouvée ou noeud Postgres KO | Vérifier l'output du noeud "Build Report" dans l'exécution |
| Workflow silencieux à 08h ICT | Schedule trigger désactivé | Ouvrir WF-010 et vérifier que le toggle "Active" est vert |

---

## Variables d'environnement liées

Fichier `.env` dans `/home/phil/local-ai-packaged/` sur le VPS :
```bash
# Google APIs (pour l'API locale :8765)
GOOGLE_SEARCH_CONSOLE_CREDENTIALS=...
GA4_CREDENTIALS=...
GA4_PROPERTY_ID=...

# Postgres Supabase interne
POSTGRES_HOST=supabase-db
POSTGRES_PASSWORD=...

# Slack
SLACK_WEBHOOK_URL=...
```

---

## Notes

- **Déployé** : actif depuis mars 2026
- **Dernière vérification** : 2026-04-02
- **Statut** : ✅ Actif, tourne quotidiennement sans intervention
- **Prochaine étape** : activer WF-011 + WF-012 pour fermer le pipeline social

---

*Documentation générée par Claude | Session Cowork 2026-04-02*
