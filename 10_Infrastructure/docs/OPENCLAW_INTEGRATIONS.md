# OpenClaw Service Integrations

This document describes how OpenClaw integrates with the full AI stack.

## 🎯 Services Accessibles

OpenClaw peut maintenant accéder à tous ces services via les variables d'environnement :

### 🗄️ Bases de Données

#### Supabase (PostgreSQL)
```python
# Via l'API Supabase
import os
from supabase import create_client

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

# Exemples d'utilisation
supabase.table('users').select('*').execute()
supabase.table('posts').insert({'title': 'Hello'}).execute()
```

**Variables d'environnement :**
- `SUPABASE_URL=http://kong:8000`
- `SUPABASE_KEY` (Service Role Key)
- `SUPABASE_ANON_KEY` (Anon Key)

#### Qdrant (Vector Database)
```python
from qdrant_client import QdrantClient
import os

qdrant = QdrantClient(url=os.getenv('QDRANT_URL'))

# Recherche vectorielle
qdrant.search(
    collection_name="documents",
    query_vector=[0.1] * 768,
    limit=5
)
```

**Variables d'environnement :**
- `QDRANT_URL=http://qdrant:6333`

#### Neo4j (Graph Database)
```python
from neo4j import GraphDatabase
import os

uri = os.getenv('NEO4J_URL')
auth = os.getenv('NEO4J_AUTH').split('/')
driver = GraphDatabase.driver(uri, auth=(auth[0], auth[1]))

# Requête Cypher
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n LIMIT 5")
```

**Variables d'environnement :**
- `NEO4J_URL=bolt://neo4j:7687`
- `NEO4J_AUTH=neo4j/your_password`

#### PostgreSQL (Direct)
```python
import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    database=os.getenv('POSTGRES_DB')
)
```

### 🤖 Services d'Automatisation

#### n8n (Workflows)
```python
import requests
import os

n8n_url = os.getenv('N8N_URL')
webhook_url = os.getenv('N8N_WEBHOOK_URL')

# Déclencher un workflow
response = requests.post(f"{webhook_url}/webhook/workflow-id", json={
    "data": "your_data"
})
```

**Variables d'environnement :**
- `N8N_URL=http://n8n:5678`
- `N8N_WEBHOOK_URL=https://n8n.yourdomain.com`

#### Crawl4AI (Web Crawling)
```python
import requests
import os

crawl4ai_url = os.getenv('CRAWL4AI_URL')

# Crawler une URL
response = requests.post(f"{crawl4ai_url}/crawl", json={
    "urls": ["https://example.com"],
    "priority": 10
})
```

**Variables d'environnement :**
- `CRAWL4AI_URL=http://crawl4ai:11235`

## 🔄 Configuration

Toutes les configurations sont dans :
- `docker-compose.yml` - URLs des services
- `openclaw/openclaw.json` - Variables d'environnement
- `openclaw/routing-config.json` - Configuration des intégrations

## 🔧 Compétences (Skills) Activées

Les skills suivants sont maintenant activés dans OpenClaw :

- ✅ `crawl4ai` - Web crawling
- ✅ `supabase-client` - Client Supabase
- ✅ `qdrant-client` - Client Qdrant
- ✅ `neo4j-client` - Client Neo4j
- ✅ `n8n-client` - Client n8n

## 📝 Exemples d'Utilisation

### Pipeline RAG Complet
```python
# 1. Crawler du contenu
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://example.com")
    content = result.markdown

# 2. Générer des embeddings avec Ollama
import requests

embeddings = requests.post("http://ollama:11434/api/embeddings", json={
    "model": "nomic-embed-text",
    "prompt": content
}).json()

# 3. Stocker dans Qdrant
qdrant.upsert(
    collection_name="docs",
    points=[{
        "id": "doc_1",
        "vector": embeddings['embedding'],
        "payload": {"content": content, "url": "https://example.com"}
    }]
)

# 4. Sauvegarder les métadonnées dans Supabase
supabase.table('documents').insert({
    'url': 'https://example.com',
    'qdrant_id': 'doc_1',
    'title': 'Example Document'
}).execute()

# 5. Créer des relations dans Neo4j
with driver.session() as session:
    session.run("""
        CREATE (d:Document {url: $url, title: $title})
        MERGE (s:Source {domain: 'example.com'})
        CREATE (d)-[:FROM]->(s)
    """, url='https://example.com', title='Example')
```

### Workflow n8n avec OpenClaw
```python
# Déclencher un workflow n8n depuis OpenClaw
def trigger_n8n_workflow(workflow_id, data):
    response = requests.post(
        f"{os.getenv('N8N_WEBHOOK_URL')}/webhook/{workflow_id}",
        json=data,
        timeout=30
    )
    return response.json()

# Utilisation
trigger_n8n_workflow('process-data', {
    'source': 'openclaw',
    'content': 'Données à traiter'
})
```

## 🔐 Sécurité

- Toutes les connexions utilisent le réseau Docker interne (sécurisé)
- Les clés API sont injectées via les variables d'environnement
- Les mots de passe sont stockés dans le fichier `.env` (non commité)

## 🚀 Prochaines Étapes

Pour créer des skills personnalisés pour ces services :

1. Créer un répertoire dans `/home/phil/local-ai-packaged/openclaw/skills/[nom-skill]/`
2. Ajouter un fichier `SKILL.md` avec la documentation
3. Ajouter des scripts Python dans un dossier `scripts/`
4. Activer le skill dans `openclaw.json`

Exemple de structure :
```
openclaw/skills/my-supabase-queries/
├── SKILL.md
└── scripts/
    ├── query_users.py
    └── insert_data.py
```
