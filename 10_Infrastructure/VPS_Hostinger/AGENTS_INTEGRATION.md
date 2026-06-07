# Agents Integration — crawl4ai + Hermes (single fat node Oracle)

> Cible : VM unique A1 (4/24/200), `--environment public`. Les deux services sont en
> `expose:` seul → internes, joignables par Caddy/Tailscale, jamais publiés en public.
> Date : 2026-06-07. (Doc d'infra — vit dans 10_Infrastructure, pas dans le repo public.)

---

## 0. Règle d'or opérationnelle

Sur l'Oracle (machine publique), **toujours** :

```bash
python start_services.py --profile cpu --environment public
```

Le défaut est `private` = tous les ports ouverts (risque H1 de l'audit). crawl4ai et Hermes
ci-dessous sont en `expose:` seul, donc `public` les garde internes par design.

---

## 1. crawl4ai — résolu

Image officielle multi-arch (arm64 natif). Crawl4AI **embarque déjà Playwright/Chromium** :
aucun conteneur Playwright séparé n'est nécessaire pour le scraping. Bloc à ajouter dans
`docker-compose.yml` :

```yaml
  crawl4ai:
    image: unclecode/crawl4ai:0.8.0        # épingle le dernier 0.8.x — pas :latest, pas :all
    container_name: crawl4ai
    restart: unless-stopped
    expose:
      - 11235/tcp                          # interne : n8n appelle http://crawl4ai:11235
    environment:
      - CRAWL4AI_API_TOKEN=${CRAWL4AI_API_TOKEN}   # remplis-le dans .env (défense en profondeur)
    shm_size: "1gb"                        # sinon Chromium OOM sur grosses pages
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11235/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: json-file
      options: { max-size: "10m", max-file: "3" }
    deploy:
      resources:
        limits:       { memory: 1500m }
        reservations: { memory: 512m }
```

Port host (dev uniquement) → dans `docker-compose.override.private.yml` seulement :

```yaml
  crawl4ai:
    ports:
      - 11235:11235
```

---

## 2. Hermes — FRESH START (différé : démarrage stable sans Hermes d'abord)

C'est le `hermes-agent` de Nous Research. Son **Dockerfile de production est déjà excellent**
(multi-stage `uv`, non-root + `gosu`/`tini`, **Chromium installé au build**). Donc Hermes
*pilote* un navigateur : deux Chromium au total (crawl4ai + Hermes), OK ; consolidation
possible plus tard via un browserless partagé si la RAM serre.

### 2.1 Source — cloner l'upstream, PAS la copie de migration

⚠️ La copie `~/migration-2026-06-05/hermes/hermes-agent/` **n'a pas `uv.lock`** (exclu du rsync).
Le Dockerfile fait `uv sync --frozen` → il **échouera** sans ce lock. Pars fresh, clone l'upstream
propre (lock + arbre complet, version épinglée) :

```bash
git clone --depth 1 --branch v0.14.0 https://github.com/NousResearch/hermes-agent ./hermes
```

### 2.2 Build une seule fois (ARM = build lourd ~10-15 min)

```bash
docker build -t palanthai/hermes:0.14.0 ./hermes
# ou buildx arm64 depuis le Mac pour ne pas charger l'A1
```

### 2.3 Service compose (image-based, volume frais)

```yaml
  hermes:
    image: palanthai/hermes:0.14.0
    container_name: hermes
    restart: unless-stopped
    expose:
      - 9119/tcp                           # dashboard interne → via Tailscale, jamais public
    environment:
      - HERMES_UID=10000
    volumes:
      - hermes_data:/opt/data              # /opt/data = HERMES_HOME : config + state bootstrap frais
    shm_size: "1gb"
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://localhost:9119/ || exit 1"]   # confirme port/chemin au 1er run
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    logging:
      driver: json-file
      options: { max-size: "10m", max-file: "3" }
    deploy:
      resources:
        limits:       { memory: 2g }
        reservations: { memory: 512m }
# volumes:
#   hermes_data:
```

### 2.4 Premier démarrage — saisir les clés ROTÉES

```bash
docker exec -it hermes hermes setup        # wizard : entre OpenRouter / NVIDIA rotés
docker exec -it hermes hermes gateway status
```

---

## 3. Vérification Kong + fichiers qui complètent le compose

- **Kong n'est pas dans `docker-compose.yml` racine** — il arrive via `include: ./supabase/docker/docker-compose.yml`. Service `supabase-kong` (`kong:2.8.1`), publie `${KONG_HTTP_PORT}:8000` + `${KONG_HTTPS_PORT}:8443`.
- **`override.public.supabase.yml`** reset `kong`/`supavisor` → ces services existent dans le compose Supabase, le reset **fonctionne** (8000/8443 fermés en public, seul Caddy joint `kong:8000`). ✓
- **`override.public.yml`** (stack IA) reset `kong`/`supavisor` qui **n'existent pas** dans la stack IA → **no-op** (finding M1). Sans danger (services IA en `expose:` seul) mais fichier trompeur.
- 🔴 **`supabase/docker/volumes/api/kong.yml` + scripts d'init Postgres absents du repo** → sur un clone neuf, Kong/Postgres ne bootent pas. **Corrigé** : `ensure_supabase_volumes()` dans `start_services.py` régénère le tout (clone sparse upstream + golden kong.yml) avant le démarrage Supabase.

---

## 4. Budget RAM (24 Go) — après ajout

| Service | Limite | Note |
|---|---|---|
| Supabase (≈10 conteneurs) | ~6 g | Logflare/analytics gourmand |
| Ollama | 2.5 g | capé |
| Neo4j / Qdrant | 2 g | |
| n8n | 700 m | |
| Redis, SearXNG, MinIO, Caddy | ~1 g | cumulé |
| **crawl4ai** | **1.5 g** | Chromium #1 |
| **Hermes** (plus tard) | **2 g** | Chromium #2 |
| **Total** | **~16 g** | OK sur 24 g, surveille Ollama sous charge |
