# Guide: Voir vos données Supabase dans un tableau

## 🚀 Accès rapide - 3 étapes

### Option 1: Dashboard Web (PLUS SIMPLE) ⭐

**Étape 1**: Ouvrez un tunnel SSH vers PostgREST
```bash
ssh -L 3000:127.0.0.1:3000 phil@31.97.67.145 "sleep 600" &
```

**Étape 2**: Ouvrez le fichier HTML
- Ouvrez `data_viewer.html` dans votre navigateur
- Ou: `open data_viewer.html` (macOS)

**Étape 3**: Sélectionnez une table et cliquez "Load Data"
- projects → 5,387 lignes
- developers → 1,522 lignes
- units → 44,988 lignes
- Et d'autres...

**Résultat**: Tableau interactif avec toutes vos données ✅

---

### Option 2: API JSON directe

Utilisez le tunnel + curl:
```bash
# Tunnel
ssh -L 3000:127.0.0.1:3000 phil@31.97.67.145 "sleep 600" &

# Puis:
curl http://localhost:3000/projects?limit=10
curl http://localhost:3000/developers?limit=5
curl http://localhost:3000/units?limit=20
```

**Résultat**: JSON complet de vos données

---

### Option 3: PostgreSQL Direct (PLUS RAPIDE)

Pas de tunnel nécessaire, juste SSH:
```bash
ssh phil@31.97.67.145
docker exec supabase-db psql -U postgres -d postgres

# Puis dans psql:
SELECT * FROM projects LIMIT 10;
SELECT * FROM developers LIMIT 5;
SELECT * FROM units LIMIT 20;
```

---

## 📊 Données disponibles

| Table | Rows | Via Dashboard | Via API | Via SQL |
|-------|------|---------------|---------|---------|
| **projects** | 5,387 | ✅ | ✅ | ✅ |
| **developers** | 1,522 | ✅ | ✅ | ✅ |
| **units** | 44,988 | ✅ | ✅ | ✅ |
| **alerts** | 0 | ✅ | ✅ | ✅ |
| **execution_data** | 1,276 | ✅ | ✅ | ✅ |
| **districts** | ? | ✅ | ✅ | ✅ |
| **provinces** | ? | ✅ | ✅ | ✅ |

---

## 🔒 Sécurité

Vos données sont protégées par RLS (Row-Level Security):

| Table | Type de données | Accès |
|-------|-----------------|-------|
| **user_api_keys** | 🔒 Credentials | Admin only (postgres) |
| **oauth_access_tokens** | 🔒 OAuth tokens | Admin only (postgres) |
| **projects, developers, units** | 📊 Public | Public read (via API) |
| **execution_data** | ⚙️ Workflows | Public read (via API) |

---

## ⚠️ Dépannage

### "Connection refused" ou timeout

**Problème**: Le tunnel SSH n'est pas actif

**Solution**:
```bash
# Vérifier que le tunnel est actif
lsof -i :3000

# Si rien, relancer:
ssh -L 3000:127.0.0.1:3000 phil@31.97.67.145 "sleep 600" &
```

### "DNS or analytics error" sur Supabase Studio

C'est normal - c'est une erreur non-critique du service "analytics" manquant. Vous pouvez l'ignorer. Les données sont toujours accessibles.

### "No results" ou "empty table"

1. Vérifier la table existe: `SELECT tablename FROM pg_tables WHERE schemaname='public';`
2. Vérifier RLS: `SELECT COUNT(*) FROM projects;`
3. Essayer une autre table

---

## 💡 Cas d'usage

### Voir les derniers projets
```sql
SELECT id, name, city, price FROM projects ORDER BY created_at DESC LIMIT 10;
```

### Chercher un développeur
```sql
SELECT * FROM developers WHERE name ILIKE '%John%' LIMIT 5;
```

### Compter les unités par projet
```sql
SELECT project_id, COUNT(*) as unit_count FROM units GROUP BY project_id ORDER BY unit_count DESC LIMIT 10;
```

---

## 📝 Notes

- Tunnel SSH: `sleep 600` = 10 minutes d'accès. Relancer après si besoin.
- RLS: Seules les données "public read" sont visibles via API
- Admin: Pour voir les tables "admin only", utiliser PostgreSQL direct avec le user postgres

---

## ✅ C'est prêt!

1. Lancez le tunnel
2. Ouvrez `data_viewer.html`
3. Sélectionnez une table
4. Cliquez "Load Data"

Vos données s'affichent dans un tableau interactif! 🎉

