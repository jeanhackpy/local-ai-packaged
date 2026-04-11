# Sprint 2 — Improvements Roadmap
> Session 2026-04-08 | Status: Coded + Planned

---

## What shipped this session (content_flywheel.py v2.0 + WF-020/021)

| Recommendation | Status | Where |
|---|---|---|
| Dynamic LLM routing per agent role | ✅ Coded | `AGENT_MODELS` dict — Groq for Researcher/Humanizer, Sonnet for QC |
| Critic/Debate Agent | ✅ Coded | `POST /content/critique` endpoint |
| RAG query rewriting (HyDE-lite) | ✅ Coded | `_rewrite_query()` — Groq 8b, 3 expanded queries |
| 9th QC dimension: AI Search Readiness | ✅ Coded | `ai_search_readiness` (weight 0.08) in QC |
| Prompt version hashing + DB storage | ✅ Coded | `prompt_versions` table + background task |
| Brand-aware RAG filtering | ✅ Coded | `frontmatter_brand` filter in `/rag/query` |
| RAG recency boost | ✅ Coded | `last_modified` range filter, configurable days |
| Experience signals in Writer | ✅ Coded | Explicit instruction in Writer prompt for both brands |
| Incremental Obsidian sync | ✅ Coded | WF-020 uses `find -newer` flag for diff-only indexing |
| Slack Approve+Publish single button | ✅ Coded | WF-021 Slack block has direct approve_publish action |

---

## P1 — Still to implement (next sessions)

### 1. Obsidian — Cloudflare Tunnel (1h setup)
**Why**: Syncthing Mac→VPS creates conflicts. Tunnel gives direct HTTP access to Obsidian REST API from n8n, no file sync required.

**Steps**:
```bash
# On Mac (where Obsidian runs)
brew install cloudflare/cloudflare/cloudflared
cloudflared tunnel create obsidian-vault
cloudflared tunnel route dns obsidian-vault obsidian.recall-agency.com
# Start tunnel (port 27124 = obsidian-local-rest-api)
cloudflared tunnel run --url http://localhost:27124 obsidian-vault
```

**n8n change**: Replace `executeCommand` nodes in WF-020 with `httpRequest` to `https://obsidian.recall-agency.com/vault/`.

**Alternative**: Tailscale (zero-config, recommended if Cloudflare setup is complex).

---

### 2. Hybrid Search — Neo4j Graph enrichment (2h)
**Why**: Vector search misses relational context (e.g., "projects near Phuket beach" needs graph traversal, not just embeddings).

**Implementation**:
```python
# In /rag/query — add Neo4j parallel query
async def _neo4j_query(keyword: str, brand: str) -> List[str]:
    """Fetch related entity names from graph for query enrichment."""
    # neo4j.run("MATCH (p:Project)-[:LOCATED_IN]->(l:Location) 
    #            WHERE l.name CONTAINS $keyword RETURN p.name, l.name")
```

**Add to AGENT_MODELS**: `"neo4j_enricher"` tier.

---

### 3. Cross-encoder Reranker (3h)
**Why**: After multi-query RAG returns 15 candidates, a cross-encoder picks the actual top 5.

```bash
pip install sentence-transformers  # already installed
# Model: cross-encoder/ms-marco-MiniLM-L-6-v2 (~80MB, runs on CPU)
```

```python
from sentence_transformers import CrossEncoder
_reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, chunks: List[str], top_k: int = 5):
    pairs = [(query, c) for c in chunks]
    scores = _reranker.predict(pairs)
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    return [c for c, _ in ranked[:top_k]]
```

**Add to `/rag/query`**: Optional `rerank=true` parameter.

---

### 4. Social Performance Feedback Loop (WF-022 update, 4h)
**Why**: Engagement data (LinkedIn likes, X reposts) → insights → next content angles.

**Data flow**:
```
WF-012 (Social Distributor)
  → posts to platforms
  → saves {platform_post_id, article_url, brand, posted_at} to Airtable
  
WF-022 (Performance Tracker, runs J+3/J+7/J+30)
  → fetches engagement via Buffer API (/1/updates/{id}.json)
  → stores to performance_metrics table
  → LLM Analysis: "Which angles got 3x engagement vs baseline?"
  → Writes insight to Obsidian: /30_Knowledge/Content_Performance/
  → Qdrant ingested → future Writer picks it up via RAG
```

**SQL addition**:
```sql
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS
  social_engagement JSONB DEFAULT '{}';
-- {likes: 45, reposts: 12, comments: 3, reach: 890}
```

---

### 5. Prompt Performance View → Monthly Report (WF-023 addition)
**Why**: Anti-fragile loop requires knowing which prompt version produces the best QC scores.

**Already created**: `prompt_performance` VIEW in content_flywheel.py SQL comment.

**Monthly n8n node** (add to WF-022):
```javascript
// Run on 1st of each month
const query = `
  SELECT role, brand, prompt_hash, avg_qc_score, approved_count, articles_evaluated
  FROM prompt_performance
  WHERE created_at > now() - interval '30 days'
  ORDER BY avg_qc_score DESC
`;
// Send to Slack #content-pipeline with trend analysis
```

---

## P2 — Medium priority (Sprint 3)

### 6. WF-011/012 Activation — Platform-specific templates

**Status**: Workflows exist but inactive. Need Airtable credentials + Buffer token.

**Template structure** (add to content_flywheel.py):
```python
SOCIAL_TEMPLATES = {
    "linkedin_post": {
        "recall": "Hook (stat/contrarian) → 3 insights → CTA. Max 200 words. No hashtag spam.",
        "reflexion": "Accroche marché → 3 conseils pratiques → question engagement. Max 200 mots.",
    },
    "x_thread": {
        "recall": "1/ [data hook] → 2-5/ [insights] → 6/ [CTA]. Under 280 chars each.",
        "reflexion": "1/ [stat marché] → 2-4/ [conseils] → 5/ [CTA + lien]. Max 280 chars.",
    },
    "linkedin_carousel": {
        "recall": "Slide 1: Bold claim. Slides 2-7: One insight each. Slide 8: CTA.",
        "reflexion": "Slide 1: Question investisseur. Slides 2-7: Réponses chiffrées. Slide 8: Contact.",
    },
}
```

**Activation checklist**:
```
□ Buffer account created (buffer.com → free plan)
□ LinkedIn Company Page connected to Buffer
□ X account connected to Buffer
□ BUFFER_ACCESS_TOKEN added to /home/phil/local-ai-packaged/.env
□ Airtable credentials added to n8n (base: appDxwFpJXwWM2fgq)
□ WF-011 activated (test with 1 published article)
□ WF-012 activated (set schedule: 2x/day, 09:00 + 15:00 ICT)
```

---

### 7. Chaos Test — Anti-fragile validation

**Scenarios to test** (add to Sprint 3):

| Test | Simulation | Expected behavior |
|---|---|---|
| GSC data empty | Return empty array from /seo/keywords | WF-010 sends Slack warning, no crash |
| Vault partially available | Delete 50% of chunks from Qdrant | Writer proceeds with reduced context, logs warning |
| All LLM tiers fail | Set all API keys to invalid | Returns 503 with clear error message |
| QC max retries hit | Force NEEDS_REVISION 3x | Escalates to Slack after 2nd retry |
| Supabase connection lost | Stop supabase-db container | Pipeline logs fail silently (non-blocking), article still generated |
| Qdrant down | Stop Qdrant container | `/rag/query` returns empty, Writer runs without vault context |

---

## P3 — Lower priority (Sprint 4+)

### 8. Observability Dashboard
- Supabase views: `pipeline_performance_daily`, `qc_trends_weekly`
- Simple HTML dashboard reading from `content_pipeline_log` + `qc_scores_log`
- Key metrics: avg pipeline time, escalation rate, approval rate, cost per article

### 9. REcall WF-001 clone
- Duplicate WF-001, replace `brand='reflexion'` → `brand='recall'`
- Add recall-specific keywords to content_queue
- Target: 2 articles/week for recall-agency.com

### 10. PatrimoinAsia + JP Personal Brand
- Add to BRAND_PROMPTS in content_flywheel.py
- Clone pipeline config, adjust brand voice

---

## One SQL migration still needed

```sql
-- Run on VPS: docker exec -it supabase-db psql -U postgres

-- Prompt versions table (for anti-fragile loop)
CREATE TABLE IF NOT EXISTS prompt_versions (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    role            TEXT NOT NULL,
    brand           TEXT NOT NULL,
    prompt_hash     TEXT NOT NULL,
    prompt_text     TEXT NOT NULL,
    model_used      TEXT,
    created_at      TIMESTAMPTZ DEFAULT now(),
    last_used_at    TIMESTAMPTZ DEFAULT now(),
    avg_qc_score    REAL,
    article_count   INT DEFAULT 0,
    UNIQUE(role, brand, prompt_hash)
);

-- Monthly performance view
CREATE OR REPLACE VIEW prompt_performance AS
SELECT
    pv.role, pv.brand, pv.prompt_hash, pv.created_at,
    COUNT(qs.id)           AS articles_evaluated,
    AVG(qs.weighted_score) AS avg_qc_score,
    AVG(qs.wiki_fidelity)  AS avg_wiki_fidelity,
    AVG(qs.brand_voice)    AS avg_brand_voice,
    SUM(CASE WHEN qs.decision='APPROVED' THEN 1 ELSE 0 END) AS approved_count
FROM prompt_versions pv
LEFT JOIN qc_scores_log qs ON qs.brand = pv.brand
GROUP BY pv.role, pv.brand, pv.prompt_hash, pv.created_at
ORDER BY pv.created_at DESC;
```

---

## Deployment order (critical path)

```
1. SSH VPS → run Sprint 1 SQL (content_pipeline_log, qc_scores_log, etc.)
2. SSH VPS → run NEW SQL above (prompt_versions, prompt_performance view)
3. SSH VPS → scp content_flywheel.py to /home/phil/palanthai/
4. SSH VPS → append to palanthai_api.py:
      from content_flywheel import router as flywheel_router
      app.include_router(flywheel_router, prefix="")
5. SSH VPS → pip install qdrant-client sentence-transformers --break-system-packages
6. SSH VPS → restart FastAPI: systemctl restart palanthai (or kill + relaunch)
7. Test: curl http://localhost:8765/flywheel/health
8. n8n → import WF-021_content_pipeline_v2.json (Settings → Import from file)
9. n8n → import WF-020_obsidian_rag_sync.json
10. n8n → run WF-020 manually (test vault sync)
11. n8n → run WF-021 manually with test payload:
    {"brand":"reflexion","keyword":"investir Phuket 2026","brief":{"target_keyword":"investir Phuket 2026"}}
12. Verify Slack notification arrives in #marketing-content
13. Verify QC scores appear in qc_scores_log
14. Activate WF-020 schedule (every 6h)
15. Activate WF-021 (replaces WF-001 + WF-002 pipeline)
```

---

*Sprint 2 — 2026-04-08 | Claude Architect*
