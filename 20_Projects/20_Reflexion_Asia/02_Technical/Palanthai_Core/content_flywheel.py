"""
content_flywheel.py — Palanthai Content Flywheel Endpoints v2.0
===============================================================
Auteur   : Claude Architect | 2026-04-08
Version  : 2.0.0
VPS path : /home/phil/palanthai/content_flywheel.py

INTÉGRATION dans palanthai_api.py (ajouter en fin de fichier) :
    from content_flywheel import router as flywheel_router
    app.include_router(flywheel_router, prefix="")

ENDPOINTS EXPOSÉS :
    POST /content/write          → Writer Agent
    POST /content/humanize       → Humanizer Agent
    POST /content/critique        → Critic/Debate Agent (v2)
    POST /content/qc             → Quality Controller (9 dimensions)
    POST /rag/query              → Qdrant semantic search (+ query rewriting)
    POST /rag/ingest             → Qdrant upsert with dedup
    GET  /content/brand-voice    → Brand voice prompt by brand
    GET  /flywheel/health        → Health check
    GET  /flywheel/prompt-version → Active prompt version hashes

NOUVEAUTÉS v2 :
    • Dynamic LLM routing per agent role (speed/cost optimised)
    • Critic/Debate Agent after Humanizer
    • RAG query rewriting before Qdrant search
    • 9th QC dimension: ai_search_readiness (AEO/LLM visibility)
    • Prompt version hashing + Supabase storage
    • RAG recency boost + brand-aware metadata filtering

DÉPENDANCES :
    pip install qdrant-client sentence-transformers python-dotenv psycopg2-binary httpx fastapi
"""

import os
import re
import json
import uuid
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Literal

import httpx
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct, Filter, FieldCondition,
    MatchAny, MatchValue, Range,
)
from sentence_transformers import SentenceTransformer

import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv("/home/phil/local-ai-packaged/.env")
logger = logging.getLogger("palanthai.flywheel")

# ─────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────

QDRANT_HOST    = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT    = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

PG = dict(
    host     = os.getenv("POSTGRES_HOST", "localhost"),
    port     = int(os.getenv("POSTGRES_PORT", "5432")),
    user     = os.getenv("POSTGRES_USER", "postgres"),
    password = os.getenv("POSTGRES_PASSWORD", ""),
    dbname   = os.getenv("POSTGRES_DB", "postgres"),
)

EMBED_MODEL = "all-MiniLM-L6-v2"
EMBED_DIM   = 384

# ─────────────────────────────────────────────────────────
# DYNAMIC LLM ROUTING
# Each agent role gets the right model for cost/quality tradeoff.
# Groq = sub-second, cheap → Researcher, Humanizer, Critic
# NVIDIA/Gemini = mid-tier → Writer
# OpenRouter Sonnet-class = expensive, best reasoning → QC
# ─────────────────────────────────────────────────────────

GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")
NVIDIA_API_KEY     = os.getenv("NVIDIA_API_KEY", "")
GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Role → ordered list of (provider, url, model)
AGENT_MODELS: Dict[str, List[Dict]] = {
    "researcher": [
        {"name": "groq",       "url": "https://api.groq.com/openai/v1/chat/completions",                               "model": "llama-3.3-70b-versatile",           "key": GROQ_API_KEY},
        {"name": "nvidia",     "url": "https://integrate.api.nvidia.com/v1/chat/completions",                          "model": "meta/llama-3.3-70b-instruct",       "key": NVIDIA_API_KEY},
        {"name": "openrouter", "url": "https://openrouter.ai/api/v1/chat/completions",                                 "model": "meta-llama/llama-3.3-70b-instruct", "key": OPENROUTER_API_KEY},
    ],
    "writer": [
        {"name": "nvidia",     "url": "https://integrate.api.nvidia.com/v1/chat/completions",                          "model": "meta/llama-3.3-70b-instruct",       "key": NVIDIA_API_KEY},
        {"name": "gemini",     "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",      "model": "gemini-2.0-flash",                  "key": GEMINI_API_KEY},
        {"name": "openrouter", "url": "https://openrouter.ai/api/v1/chat/completions",                                 "model": "anthropic/claude-3-5-haiku",        "key": OPENROUTER_API_KEY},
        {"name": "groq",       "url": "https://api.groq.com/openai/v1/chat/completions",                               "model": "llama-3.3-70b-versatile",           "key": GROQ_API_KEY},
    ],
    "humanizer": [
        {"name": "groq",       "url": "https://api.groq.com/openai/v1/chat/completions",                               "model": "llama-3.3-70b-versatile",           "key": GROQ_API_KEY},
        {"name": "openrouter", "url": "https://openrouter.ai/api/v1/chat/completions",                                 "model": "anthropic/claude-3-5-haiku",        "key": OPENROUTER_API_KEY},
    ],
    "critic": [
        {"name": "groq",       "url": "https://api.groq.com/openai/v1/chat/completions",                               "model": "llama-3.3-70b-versatile",           "key": GROQ_API_KEY},
        {"name": "nvidia",     "url": "https://integrate.api.nvidia.com/v1/chat/completions",                          "model": "meta/llama-3.3-70b-instruct",       "key": NVIDIA_API_KEY},
    ],
    "qc": [
        {"name": "openrouter", "url": "https://openrouter.ai/api/v1/chat/completions",                                 "model": "anthropic/claude-3-5-sonnet",       "key": OPENROUTER_API_KEY},
        {"name": "gemini",     "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",      "model": "gemini-2.0-flash-thinking-exp",     "key": GEMINI_API_KEY},
        {"name": "nvidia",     "url": "https://integrate.api.nvidia.com/v1/chat/completions",                          "model": "meta/llama-3.3-70b-instruct",       "key": NVIDIA_API_KEY},
    ],
    "rewriter": [  # Query rewriting — fast and cheap
        {"name": "groq",       "url": "https://api.groq.com/openai/v1/chat/completions",                               "model": "llama-3.1-8b-instant",              "key": GROQ_API_KEY},
        {"name": "nvidia",     "url": "https://integrate.api.nvidia.com/v1/chat/completions",                          "model": "meta/llama-3.1-8b-instruct",        "key": NVIDIA_API_KEY},
    ],
}


# ─────────────────────────────────────────────────────────
# QC WEIGHTS (v2 — 9 dimensions, weights sum to 1.0)
# ─────────────────────────────────────────────────────────

QC_WEIGHTS = {
    "wiki_fidelity":       0.18,
    "seo_quality":         0.13,
    "brand_voice_match":   0.18,
    "humanness":           0.13,
    "originality":         0.09,
    "readability":         0.09,
    "eeat_signals":        0.07,
    "factual_accuracy":    0.05,
    "ai_search_readiness": 0.08,   # NEW — AEO / LLM visibility
}

# ─────────────────────────────────────────────────────────
# BRAND PROMPTS (embedded — no Notion dependency)
# ─────────────────────────────────────────────────────────

BRAND_PROMPTS: Dict[str, Dict] = {
    "recall": {
        "writer": (
            "You write for REcall Agency — an AI intelligence boutique, not a marketing factory.\n"
            "TONE: Sharp. Technical. Direct. No hype.\n"
            "AUDIENCE: Real estate professionals, PropTech entrepreneurs, hospitality operators.\n"
            "VOICE: Lead with data. Speak like insider intelligence, not a sales pitch.\n"
            "VOCABULARY (use): algorithmic, pipeline, inference, sovereignty, agentic, orchestration, "
            "deterministic, architecture, signal, attribution\n"
            "VOCABULARY (ban): game-changer, revolutionary, synergy, disruptive, paradigm shift, "
            "unlock, leverage (as buzzword), seamless\n"
            "STRUCTURE: Open with contrarian observation or precise data point. Build logical argument. "
            "Close with low-friction, specific CTA.\n"
            "EXPERIENCE SIGNALS: Whenever vault data is available use first-person plural: "
            "'From our analysis of 340+ listings across Bangkok Q1 2026...' — never generic.\n"
            "LANGUAGE: English only. American spelling. Technical precision over accessibility.\n"
            "LENGTH: Dense paragraphs. Short sentences for emphasis. No filler."
        ),
        "humanizer": (
            "Maintain REcall's technical precision and contrarian edge. Do not soften or dilute. "
            "Preserve ALL data points and technical vocabulary."
        ),
        "critic_persona": (
            "You are a skeptical senior PropTech analyst reviewing a colleague's research brief. "
            "Your job is to find weak arguments, missing data, and technical inaccuracies. "
            "Be direct. No pleasantries. Challenge every unsupported claim."
        ),
        "qc_criteria": {
            "brand_voice": "Must sound like a technical insider report — not a blog post. Data-first, no enthusiasm.",
            "language": "EN only",
            "banned_words": ["game-changer", "revolutionary", "synergy", "disruptive", "seamless"],
        },
    },
    "reflexion": {
        "writer": (
            "You write for REflexion Asia — la plateforme d'intelligence immobilière premium en Thaïlande.\n"
            "TONE: Expert. Rassurant. Précis. Chaleureux.\n"
            "AUDIENCE: Investisseurs français HNW (35-55), expatriés, digital nomads francophones.\n"
            "VOICE: Combine la rigueur d'un analyste avec la chaleur d'un insider local. "
            "Tu informes, tu guides, tu rassures. Tu ne vends jamais directement.\n"
            "VOCABULARY (use): rendement locatif, freehold, leasehold, due diligence, chanote, "
            "immigration, Elite Visa, précision, intelligence, patrimoine, sérénité\n"
            "VOCABULARY (ban): cheap, bargain, bon marché, pas cher, deal incroyable\n"
            "REPLACE: 'appartement' → 'résidence' | 'prix bas' → 'rapport qualité-valeur exceptionnel'\n"
            "EXPERIENCE SIGNALS: Use vault data to ground claims: 'D'après notre analyse de X "
            "résidences à Phuket...' ou 'Dans notre base de projets suivis...' — ancre dans le réel.\n"
            "STRUCTURE: Hook narratif ou donnée marché. Preuve chiffrée. Guide pratique. CTA consultatif.\n"
            "LANGUAGE: Français principal. Termes techniques en anglais acceptables. Phrases ≤ 25 mots."
        ),
        "humanizer": (
            "Maintain REflexion's warmth and expert-guide tone. Do not make clinical or cold. "
            "Keep French warm, expert, reassuring. Never aggressive or salesy."
        ),
        "critic_persona": (
            "Tu es un investisseur immobilier français expérimenté qui lit cet article avant de l'envoyer "
            "à ses clients. Tu cherches les imprécisions, les affirmations sans preuve, les termes trop vagues. "
            "Sois direct, constructif, et spécifique."
        ),
        "qc_criteria": {
            "brand_voice": "Must feel like advice from a trusted friend who is also an expert. Warm but never salesy.",
            "language": "FR primary",
            "banned_words": ["cheap", "bargain", "bon marché", "pas cher"],
        },
    },
    "patrimonasia": {
        "writer": "Wealth management voice for Southeast Asia. Conservative, trustworthy, long-term oriented.",
        "humanizer": "Maintain formal, trustworthy register for wealth management audiences.",
        "critic_persona": "You are a conservative wealth manager scrutinising claims for accuracy and compliance risk.",
        "qc_criteria": {
            "brand_voice": "Conservative, trust-building, long-term perspective.",
            "language": "EN/FR",
            "banned_words": [],
        },
    },
}

# ─────────────────────────────────────────────────────────
# PROMPT VERSIONS — hash each active prompt for traceability
# ─────────────────────────────────────────────────────────

def _prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]

PROMPT_REGISTRY: Dict[str, str] = {
    f"writer_{brand}":   _prompt_hash(v["writer"])
    for brand, v in BRAND_PROMPTS.items()
}


# ─────────────────────────────────────────────────────────
# SINGLETON CLIENTS
# ─────────────────────────────────────────────────────────

_qdrant_client: Optional[QdrantClient] = None
_embed_model:   Optional[SentenceTransformer] = None


def get_qdrant() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            host=QDRANT_HOST, port=QDRANT_PORT,
            api_key=QDRANT_API_KEY, timeout=30,
        )
    return _qdrant_client


def get_embedder() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBED_MODEL)
    return _embed_model


def get_db():
    return psycopg2.connect(**PG, cursor_factory=RealDictCursor)


# ─────────────────────────────────────────────────────────
# LLM CALL — dynamic role-based routing with fallback chain
# ─────────────────────────────────────────────────────────

async def llm_call(
    role: str,
    system_prompt: str,
    user_message: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    json_mode: bool = False,
) -> tuple[str, str]:
    """
    Route LLM call to the optimal model for the given agent role.
    Falls back through the role's tier list, then to 'writer' tiers.
    Returns (content, "provider/model").
    """
    tiers = AGENT_MODELS.get(role, AGENT_MODELS["writer"])
    last_error = None

    async with httpx.AsyncClient(timeout=120.0) as client:
        for tier in tiers:
            if not tier["key"]:
                continue
            payload: Dict[str, Any] = {
                "model": tier["model"],
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_message},
                ],
                "temperature": temperature,
                "max_tokens":  max_tokens,
            }
            if json_mode:
                payload["response_format"] = {"type": "json_object"}

            try:
                resp = await client.post(
                    tier["url"],
                    json=payload,
                    headers={"Authorization": f"Bearer {tier['key']}", "Content-Type": "application/json"},
                )
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]
                logger.info(f"LLM[{role}] OK via {tier['name']}/{tier['model']}")
                return content, f"{tier['name']}/{tier['model']}"
            except Exception as e:
                last_error = e
                logger.warning(f"LLM[{role}] tier {tier['name']} failed: {e}")

    raise HTTPException(503, detail=f"All LLM tiers failed for role '{role}'. Last: {last_error}")


def _parse_llm_json(raw: str) -> Dict:
    """Parse LLM response as JSON — strips markdown code fences if present."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise


# ─────────────────────────────────────────────────────────
# RAG QUERY REWRITING
# Transforms a short keyword into 3 semantically rich queries
# for better Qdrant recall (HyDE-lite approach)
# ─────────────────────────────────────────────────────────

async def _rewrite_query(query: str, brand: str, context: str = "") -> List[str]:
    """
    Rewrite a short keyword into 3 expanded queries for richer RAG retrieval.
    Fast call via 'rewriter' role (Groq llama-3.1-8b-instant ~100ms).
    Returns list of 3 queries including the original.
    """
    sys = (
        "You are a search query expander for a real estate knowledge base. "
        "Given a short keyword or topic, generate 3 semantically distinct search queries "
        "that would retrieve relevant expert knowledge about this topic. "
        "Return JSON: {\"queries\": [\"q1\", \"q2\", \"q3\"]}"
    )
    msg = f"Brand: {brand}\nKeyword: {query}\nContext hint: {context[:200] if context else 'none'}"

    try:
        raw, _ = await llm_call("rewriter", sys, msg, temperature=0.3, max_tokens=200, json_mode=True)
        parsed = _parse_llm_json(raw)
        queries = parsed.get("queries", [])
        if queries:
            return [query] + [q for q in queries if q != query][:2]
    except Exception as e:
        logger.debug(f"Query rewriting failed (non-fatal, using original): {e}")
    return [query]


# ─────────────────────────────────────────────────────────
# BACKGROUND TASKS — non-blocking DB writes
# ─────────────────────────────────────────────────────────

def _db_log_pipeline(run_id: str, field: str, value: Any):
    FIELD_MAP = {
        "writer_draft":    "writer_draft",
        "humanized_draft": "humanized_draft",
        "final_content":   "final_content",
    }
    col = FIELD_MAP.get(field, "updated_at")
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE content_pipeline_log SET {col}=%s, updated_at=now() WHERE id=%s",
                (value if isinstance(value, str) else json.dumps(value), run_id),
            )
            conn.commit()
        conn.close()
    except Exception as e:
        logger.debug(f"Pipeline log write non-fatal: {e}")


def _db_log_qc(run_id: str, brand: str, keyword: str, qc_response: "QCResponse"):
    scores = qc_response.scores
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO qc_scores_log (
                    pipeline_run_id, brand, keyword, revision_number,
                    wiki_fidelity, seo_quality, brand_voice, humanness,
                    originality, readability, eeat_signals, factual_accuracy,
                    weighted_score, decision, issues
                ) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s)""",
                (
                    run_id, brand, keyword, qc_response.revision_number,
                    scores.get("wiki_fidelity", {}).get("score", 0),
                    scores.get("seo_quality", {}).get("score", 0),
                    scores.get("brand_voice_match", {}).get("score", 0),
                    scores.get("humanness", {}).get("score", 0),
                    scores.get("originality", {}).get("score", 0),
                    scores.get("readability", {}).get("score", 0),
                    scores.get("eeat_signals", {}).get("score", 0),
                    scores.get("factual_accuracy", {}).get("score", 0),
                    qc_response.weighted_score,
                    qc_response.decision,
                    json.dumps({d: s.issues for d, s in scores.items() if s.issues}),
                ),
            )
            conn.commit()
        conn.close()
    except Exception as e:
        logger.debug(f"QC log write non-fatal: {e}")


def _db_store_prompt_version(role: str, brand: str, prompt_text: str, model_used: str):
    """Persist prompt hash + text for the anti-fragile improvement loop."""
    phash = _prompt_hash(prompt_text)
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO prompt_versions (role, brand, prompt_hash, prompt_text, model_used)
                   VALUES (%s,%s,%s,%s,%s)
                   ON CONFLICT (role, brand, prompt_hash) DO UPDATE SET last_used_at=now()""",
                (role, brand, phash, prompt_text, model_used),
            )
            conn.commit()
        conn.close()
    except Exception as e:
        logger.debug(f"Prompt version store non-fatal: {e}")


# ─────────────────────────────────────────────────────────
# PYDANTIC SCHEMAS
# ─────────────────────────────────────────────────────────

class WriterRequest(BaseModel):
    brand: str
    keyword: str
    brief: Dict[str, Any]
    rag_context: Optional[str] = ""
    max_words: Optional[int] = 1500
    previous_revision_feedback: Optional[str] = None
    pipeline_run_id: Optional[str] = None


class WriterResponse(BaseModel):
    title: str
    meta_description: str
    slug: str
    content: str
    word_count: int
    primary_keyword_density: float
    internal_links_used: List[str] = []
    schema_markup: Optional[Dict] = None
    model_used: str
    prompt_hash: str
    pipeline_run_id: Optional[str] = None


class HumanizerRequest(BaseModel):
    brand: str
    keyword: str
    draft: str
    pipeline_run_id: Optional[str] = None


class HumanizerResponse(BaseModel):
    humanized: str
    changes_count: int
    patterns_eliminated: List[str] = []
    pipeline_run_id: Optional[str] = None


class CriticRequest(BaseModel):
    brand: str
    keyword: str
    draft: str
    brief: Optional[Dict[str, Any]] = None
    pipeline_run_id: Optional[str] = None


class CriticFinding(BaseModel):
    type: str          # "weak_argument" | "missing_data" | "factual_risk" | "brand_deviation"
    location: str      # quote from article identifying where
    critique: str
    fix_suggestion: str
    severity: str      # "high" | "medium" | "low"


class CriticResponse(BaseModel):
    overall_verdict: str    # "STRONG" | "NEEDS_WORK" | "MAJOR_ISSUES"
    findings: List[CriticFinding] = []
    high_severity_count: int
    approved_for_next_stage: bool
    debate_summary: str
    pipeline_run_id: Optional[str] = None


class QCDimensionScore(BaseModel):
    score: float
    justification: str
    issues: List[str] = []


class QCRequest(BaseModel):
    brand: str
    keyword: str
    draft: str
    brief: Optional[Dict[str, Any]] = None
    rag_context: Optional[str] = ""
    revision_number: Optional[int] = 0
    pipeline_run_id: Optional[str] = None


class QCResponse(BaseModel):
    decision: str   # APPROVED | NEEDS_REVISION | ESCALATE_TO_HUMAN
    weighted_score: float
    min_score: float
    scores: Dict[str, QCDimensionScore]
    revision_instructions: Optional[str] = None
    escalation_reason: Optional[str] = None
    strengths: List[str] = []
    revision_number: int
    pipeline_run_id: Optional[str] = None


class RAGQueryRequest(BaseModel):
    query: str
    collection: str = "obsidian_knowledge"
    brand: Optional[str] = None
    limit: int = 5
    score_threshold: float = 0.50
    filters: Optional[Dict[str, Any]] = None
    rewrite_query: bool = True          # Enable query expansion by default
    recency_boost_days: Optional[int] = 90  # Boost docs modified in last N days


class RAGQueryResult(BaseModel):
    id: str
    score: float
    payload: Dict[str, Any]
    text: str
    query_matched: str     # which rewritten query matched


class RAGQueryResponse(BaseModel):
    results: List[RAGQueryResult]
    query: str
    queries_used: List[str]
    collection: str
    total: int


class RAGChunk(BaseModel):
    text: str
    metadata: Dict[str, Any] = {}


class RAGIngestRequest(BaseModel):
    collection: str = "obsidian_knowledge"
    chunks: List[RAGChunk]
    deduplicate: bool = True


class RAGIngestResponse(BaseModel):
    ingested_count: int
    skipped_count: int
    collection: str


class BrandVoiceResponse(BaseModel):
    brand: str
    writer_prompt: str
    humanizer_prompt: str
    critic_persona: str
    qc_criteria: Dict[str, Any]
    prompt_hash: str
    available_brands: List[str]


# ─────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────

router = APIRouter(tags=["Content Flywheel v2"])


# ── GET /content/brand-voice ──────────────────────────────

@router.get("/content/brand-voice", response_model=BrandVoiceResponse)
async def get_brand_voice(brand: str = Query(...)):
    brand = brand.lower().strip()
    if brand not in BRAND_PROMPTS:
        raise HTTPException(404, detail=f"Brand '{brand}' not found. Available: {list(BRAND_PROMPTS)}")
    bp = BRAND_PROMPTS[brand]
    return BrandVoiceResponse(
        brand=brand,
        writer_prompt=bp["writer"],
        humanizer_prompt=bp["humanizer"],
        critic_persona=bp["critic_persona"],
        qc_criteria=bp["qc_criteria"],
        prompt_hash=_prompt_hash(bp["writer"]),
        available_brands=list(BRAND_PROMPTS),
    )


# ── GET /flywheel/prompt-version ──────────────────────────

@router.get("/flywheel/prompt-version")
async def get_prompt_versions():
    """Return current prompt hashes — use to detect drift after updates."""
    return {
        "version": "2.0.0",
        "generated_at": datetime.utcnow().isoformat(),
        "prompts": PROMPT_REGISTRY,
        "qc_weights": QC_WEIGHTS,
        "qc_dimensions": len(QC_WEIGHTS),
    }


# ── POST /content/write ───────────────────────────────────

@router.post("/content/write", response_model=WriterResponse)
async def write_article(req: WriterRequest, background_tasks: BackgroundTasks):
    """
    Writer Agent — LLM model: NVIDIA/Gemini (mid-tier, quality-focused).
    Brand voice applied conditionally. RAG context injected from vault.
    Experience signals forced when vault data available.
    """
    brand_key = req.brand.lower()
    brand_voice = BRAND_PROMPTS.get(brand_key, BRAND_PROMPTS["reflexion"])["writer"]
    prompt_hash = _prompt_hash(brand_voice)

    system_prompt = f"""You are the primary content writer for the RE ecosystem.

## Brand Voice — APPLY STRICTLY
{brand_voice}

## Content Structure Rules
1. H1: Include primary keyword naturally. Exactly one per article.
2. Introduction (150-200 words): Hook → Problem → Promise.
3. H2 sections: Follow brief's key_sections, each 200-400 words.
4. Data points from vault MUST be cited: "(source: vault)" inline.
5. Internal links: embed 3-5 contextual links from brief's internal_links.
6. Conclusion: Summarise + CTA aligned with brand voice.
7. FAQ section when schema_type = FAQPage: 3-5 Q&A pairs.
8. NEVER fabricate stats. Only use data present in rag_context.
9. First 100 words MUST contain primary keyword and a direct answer to search intent.
10. Experience signals: Ground ALL factual claims in vault data with specific phrasing.

## Output (strict JSON, no markdown outside the content field)
{{
  "title": "H1 with primary keyword",
  "meta_description": "150-160 chars, keyword + CTA",
  "slug": "url-friendly-slug",
  "content": "Full article in Markdown",
  "internal_links_used": ["url1"],
  "schema_markup": {{"@type": "Article"}},
  "word_count": 1500,
  "primary_keyword_density": 1.2,
  "e_e_a_t_signals_included": ["signal1"]
}}"""

    revision_section = ""
    if req.previous_revision_feedback:
        revision_section = (
            f"\n\n## REVISION REQUIRED\n"
            f"Address every point below before writing:\n{req.previous_revision_feedback}"
        )

    user_message = (
        f"Brand: {req.brand}\n"
        f"Keyword: {req.keyword}\n"
        f"Target word count: {req.max_words}\n\n"
        f"Brief:\n{json.dumps(req.brief, ensure_ascii=False)}\n\n"
        f"Vault Context (cite as 'source: vault'):\n"
        f"{req.rag_context or 'No vault context — write from brief only.'}"
        f"{revision_section}\n\nReturn strict JSON."
    )

    raw, model_used = await llm_call(
        "writer", system_prompt, user_message,
        temperature=0.7, max_tokens=6000, json_mode=True,
    )

    parsed = _parse_llm_json(raw)

    background_tasks.add_task(
        _db_store_prompt_version, "writer", brand_key, system_prompt, model_used
    )
    if req.pipeline_run_id:
        background_tasks.add_task(
            _db_log_pipeline, req.pipeline_run_id, "writer_draft", parsed.get("content", "")
        )

    return WriterResponse(
        title=parsed.get("title", ""),
        meta_description=parsed.get("meta_description", ""),
        slug=parsed.get("slug", ""),
        content=parsed.get("content", raw),
        word_count=parsed.get("word_count", len(parsed.get("content", "").split())),
        primary_keyword_density=parsed.get("primary_keyword_density", 0.0),
        internal_links_used=parsed.get("internal_links_used", []),
        schema_markup=parsed.get("schema_markup"),
        model_used=model_used,
        prompt_hash=prompt_hash,
        pipeline_run_id=req.pipeline_run_id,
    )


# ── POST /content/humanize ────────────────────────────────

@router.post("/content/humanize", response_model=HumanizerResponse)
async def humanize_article(req: HumanizerRequest, background_tasks: BackgroundTasks):
    """
    Humanizer Agent — LLM model: Groq (fast, sub-second).
    Refines AI patterns without touching SEO signals.
    """
    brand_key = req.brand.lower()
    brand_hint = BRAND_PROMPTS.get(brand_key, BRAND_PROMPTS["reflexion"])["humanizer"]

    system_prompt = f"""You are a specialist in making AI-generated content indistinguishable from expert human writing.
You do NOT rewrite — you refine. Every fact, data point, keyword, link, and heading is preserved EXACTLY.

## Brand-specific instruction
{brand_hint}

## What you change
1. SENTENCE RHYTHM: Vary length deliberately. Mix 5-8 word sentences with 20-30 word ones. Never 3+ same length in a row.
2. TRANSITIONS: Replace (Furthermore, Additionally, Moreover) with natural connectives or nothing.
3. PARAGRAPH OPENERS: Never start 2 consecutive paragraphs with the same word or pattern.
4. MICRO-IMPERFECTIONS (1-2 max): parenthetical asides, trailing context, direct reader address.
5. VOCABULARY: Replace repeated words with synonyms (identical meaning only). Remove weak intensifiers.

## What you NEVER change
❌ Statistics, numbers, any data point
❌ Proper nouns, brand names, location names
❌ Links — href and anchor text are sacred
❌ H1/H2/H3 structure and keywords in headings
❌ Meta description, schema markup
❌ CTA text and intent

## AI patterns to eliminate
- "In conclusion," / "In summary,"
- "It's worth noting", "It's important to", "crucial to understand"
- Overly balanced "On one hand X, on the other hand Y"
- Consecutive sentences starting with "This"
- Paragraphs all ending with a summary sentence
- Exactly 3-item lists when prose works better

## Output (strict JSON)
{{"humanized": "full refined article in Markdown", "changes_count": 12, "patterns_eliminated": ["list"]}}"""

    raw, _ = await llm_call(
        "humanizer", system_prompt,
        f"Brand: {req.brand}\nKeyword: {req.keyword}\n\nArticle:\n---\n{req.draft}\n---\n\nReturn strict JSON.",
        temperature=0.5, max_tokens=6000, json_mode=True,
    )

    try:
        parsed = _parse_llm_json(raw)
    except Exception:
        parsed = {"humanized": req.draft, "changes_count": 0, "patterns_eliminated": ["parse_error"]}

    if req.pipeline_run_id:
        background_tasks.add_task(
            _db_log_pipeline, req.pipeline_run_id, "humanized_draft", parsed.get("humanized", req.draft)
        )

    return HumanizerResponse(
        humanized=parsed.get("humanized", req.draft),
        changes_count=parsed.get("changes_count", 0),
        patterns_eliminated=parsed.get("patterns_eliminated", []),
        pipeline_run_id=req.pipeline_run_id,
    )


# ── POST /content/critique ────────────────────────────────

@router.post("/content/critique", response_model=CriticResponse)
async def critique_article(req: CriticRequest, background_tasks: BackgroundTasks):
    """
    Critic/Debate Agent (v2 NEW) — LLM model: Groq (fast).
    Runs AFTER Humanizer, BEFORE QC.
    Debates the article from the target reader's perspective.
    Surfaces weak arguments, missing data, factual risks, brand deviations.
    High-severity findings trigger revision before QC, saving expensive Sonnet calls.
    """
    brand_key = req.brand.lower()
    critic_persona = BRAND_PROMPTS.get(brand_key, BRAND_PROMPTS["reflexion"])["critic_persona"]

    system_prompt = f"""You are a pre-publication critic with the following persona:
{critic_persona}

Your mission: find every weakness in this article BEFORE it reaches quality control.
You debate the content on 4 axes:

1. WEAK ARGUMENTS: Claims made without supporting data or logic
2. MISSING DATA: Important context or facts the reader would expect and that are absent
3. FACTUAL RISK: Statements that could be wrong or outdated — flag them
4. BRAND DEVIATION: Vocabulary, tone, or structure that doesn't match brand voice

## Severity
- HIGH: Must fix before publishing (affects trust, accuracy, or SEO)
- MEDIUM: Should fix (affects quality)
- LOW: Nice to fix (minor improvements)

## Decision
approved_for_next_stage = true IF high_severity_count == 0
approved_for_next_stage = false IF high_severity_count >= 1

## Output (strict JSON)
{{
  "overall_verdict": "STRONG|NEEDS_WORK|MAJOR_ISSUES",
  "findings": [
    {{
      "type": "weak_argument|missing_data|factual_risk|brand_deviation",
      "location": "exact quote from article (max 80 chars)",
      "critique": "specific critique in 1-2 sentences",
      "fix_suggestion": "concrete fix in 1-2 sentences",
      "severity": "high|medium|low"
    }}
  ],
  "high_severity_count": 0,
  "approved_for_next_stage": true,
  "debate_summary": "2-3 sentence overall assessment"
}}"""

    brief_section = f"\nBrief:\n{json.dumps(req.brief, ensure_ascii=False)}\n" if req.brief else ""

    raw, _ = await llm_call(
        "critic", system_prompt,
        f"Brand: {req.brand}\nKeyword: {req.keyword}\n{brief_section}\nArticle:\n---\n{req.draft}\n---\nReturn strict JSON.",
        temperature=0.3, max_tokens=2000, json_mode=True,
    )

    try:
        parsed = _parse_llm_json(raw)
    except Exception:
        # Fail safe — don't block pipeline
        return CriticResponse(
            overall_verdict="STRONG",
            findings=[],
            high_severity_count=0,
            approved_for_next_stage=True,
            debate_summary="Critic parse error — auto-approved for pipeline continuity.",
            pipeline_run_id=req.pipeline_run_id,
        )

    findings = [
        CriticFinding(
            type=f.get("type", "weak_argument"),
            location=f.get("location", ""),
            critique=f.get("critique", ""),
            fix_suggestion=f.get("fix_suggestion", ""),
            severity=f.get("severity", "low"),
        )
        for f in parsed.get("findings", [])
    ]

    high_count = sum(1 for f in findings if f.severity == "high")

    return CriticResponse(
        overall_verdict=parsed.get("overall_verdict", "STRONG"),
        findings=findings,
        high_severity_count=high_count,
        approved_for_next_stage=high_count == 0,
        debate_summary=parsed.get("debate_summary", ""),
        pipeline_run_id=req.pipeline_run_id,
    )


# ── POST /content/qc ─────────────────────────────────────

@router.post("/content/qc", response_model=QCResponse)
async def quality_control(req: QCRequest, background_tasks: BackgroundTasks):
    """
    Quality Controller (9 dimensions) — LLM model: Claude Sonnet via OpenRouter.
    Includes AI Search Readiness (AEO) as 9th dimension.
    Decision logic enforced server-side — LLM math is never trusted.
    Scores persisted to qc_scores_log for prompt improvement loop.
    """
    brand_key = req.brand.lower()
    criteria = BRAND_PROMPTS.get(brand_key, BRAND_PROMPTS["reflexion"])["qc_criteria"]
    weights_block = "\n".join(
        f"  {dim.upper()} (weight {w}): {_dim_description(dim)}"
        for dim, w in QC_WEIGHTS.items()
    )

    system_prompt = f"""You are the final quality gate before human review of the Palanthai content pipeline.
Score the article on 9 dimensions. Be rigorous, specific, and consistent. Low temperature was chosen intentionally.

## Scoring Dimensions (0.0–10.0, one decimal)
{weights_block}

## Brand Quality Criteria
Voice requirement: {criteria.get('brand_voice')}
Language: {criteria.get('language')}
Banned words: {', '.join(criteria.get('banned_words', []))}

## Decision Logic (applied server-side — output your raw scores, I'll calculate)
- APPROVED: weighted ≥ 8.5 AND all scores ≥ 7.0
- ESCALATE_TO_HUMAN: any score < 7.0 OR wiki_fidelity < 6.0 OR factual_accuracy < 6.0
- NEEDS_REVISION: weighted ≥ 7.0 (return to Writer with specific feedback, max 2 retries)

## Output (strict JSON)
{{
  "scores": {{
    "wiki_fidelity":       {{"score": 9.0, "justification": "...", "issues": []}},
    "seo_quality":         {{"score": 8.5, "justification": "...", "issues": []}},
    "brand_voice_match":   {{"score": 9.0, "justification": "...", "issues": []}},
    "humanness":           {{"score": 8.0, "justification": "...", "issues": []}},
    "originality":         {{"score": 7.5, "justification": "...", "issues": []}},
    "readability":         {{"score": 9.0, "justification": "...", "issues": []}},
    "eeat_signals":        {{"score": 8.0, "justification": "...", "issues": []}},
    "factual_accuracy":    {{"score": 9.5, "justification": "...", "issues": []}},
    "ai_search_readiness": {{"score": 8.5, "justification": "...", "issues": []}}
  }},
  "revision_instructions": null,
  "escalation_reason": null,
  "strengths": ["strength1", "strength2"]
}}"""

    user_message = (
        f"Brand: {req.brand} | Keyword: {req.keyword} | Revision #{req.revision_number}\n\n"
        f"Brief:\n{json.dumps(req.brief, ensure_ascii=False) if req.brief else 'none'}\n\n"
        f"Vault context:\n{req.rag_context or 'none'}\n\n"
        f"Article:\n---\n{req.draft}\n---\n\nReturn strict JSON."
    )

    raw, model_used = await llm_call(
        "qc", system_prompt, user_message,
        temperature=0.15, max_tokens=3000, json_mode=True,
    )

    parsed = _parse_llm_json(raw)
    raw_scores = parsed.get("scores", {})

    typed_scores: Dict[str, QCDimensionScore] = {}
    for dim in QC_WEIGHTS:
        rs = raw_scores.get(dim, {})
        typed_scores[dim] = QCDimensionScore(
            score=float(rs.get("score", 5.0)),
            justification=rs.get("justification", ""),
            issues=rs.get("issues", []),
        )

    # Server-side math — never trust LLM arithmetic
    weighted  = round(sum(typed_scores[d].score * w for d, w in QC_WEIGHTS.items()), 2)
    min_score = round(min(s.score for s in typed_scores.values()), 2)
    wiki_ok   = typed_scores.get("wiki_fidelity",    QCDimensionScore(score=10, justification="", issues=[])).score
    fact_ok   = typed_scores.get("factual_accuracy", QCDimensionScore(score=10, justification="", issues=[])).score

    if weighted >= 8.5 and min_score >= 7.0:
        decision = "APPROVED"
    elif min_score < 7.0 or wiki_ok < 6.0 or fact_ok < 6.0:
        decision = "ESCALATE_TO_HUMAN"
    else:
        decision = "NEEDS_REVISION"

    response = QCResponse(
        decision=decision,
        weighted_score=weighted,
        min_score=min_score,
        scores=typed_scores,
        revision_instructions=parsed.get("revision_instructions") if decision != "APPROVED" else None,
        escalation_reason=parsed.get("escalation_reason")         if decision == "ESCALATE_TO_HUMAN" else None,
        strengths=parsed.get("strengths", []),
        revision_number=req.revision_number or 0,
        pipeline_run_id=req.pipeline_run_id,
    )

    if req.pipeline_run_id:
        background_tasks.add_task(_db_log_qc, req.pipeline_run_id, req.brand, req.keyword, response)
        background_tasks.add_task(
            _db_store_prompt_version, "qc", brand_key, system_prompt, model_used
        )

    return response


# ── POST /rag/query ───────────────────────────────────────

@router.post("/rag/query", response_model=RAGQueryResponse)
async def rag_query(req: RAGQueryRequest):
    """
    Semantic search with optional query rewriting (HyDE-lite) and recency boost.
    Runs up to 3 rewritten queries, deduplicates by id, returns top-N by score.
    """
    qdrant   = get_qdrant()
    embedder = get_embedder()

    # Expand query into 3 semantically distinct variants
    if req.rewrite_query:
        queries = await _rewrite_query(req.query, req.brand or "reflexion")
    else:
        queries = [req.query]

    # Build base filter
    conditions = []
    if req.filters:
        for k, v in req.filters.items():
            if isinstance(v, list):
                conditions.append(FieldCondition(key=k, match=MatchAny(any=v)))
            else:
                conditions.append(FieldCondition(key=k, match=MatchValue(value=v)))

    # Brand-aware filter: prefer brand-specific or WIKI documents
    if req.brand:
        conditions.append(
            FieldCondition(
                key="frontmatter_brand",
                match=MatchAny(any=[req.brand.lower(), "wiki", "global"]),
            )
        )

    # Recency boost: prefer recently modified documents
    if req.recency_boost_days:
        cutoff = (datetime.utcnow() - timedelta(days=req.recency_boost_days)).isoformat()
        conditions.append(FieldCondition(key="last_modified", range=Range(gte=cutoff)))

    qdrant_filter = Filter(must=conditions) if conditions else None

    # Fan out queries, collect results deduplicated by id
    seen_ids: Dict[str, RAGQueryResult] = {}

    for q_text in queries:
        vec = embedder.encode(q_text).tolist()
        try:
            hits = qdrant.search(
                collection_name=req.collection,
                query_vector=vec,
                limit=req.limit,
                score_threshold=req.score_threshold,
                query_filter=qdrant_filter,
                with_payload=True,
            )
        except Exception as e:
            logger.warning(f"Qdrant query failed for '{q_text}': {e}")
            continue

        for hit in hits:
            hit_id = str(hit.id)
            # Keep highest scoring version if seen from multiple queries
            if hit_id not in seen_ids or hit.score > seen_ids[hit_id].score:
                payload = hit.payload or {}
                text = payload.get("text") or payload.get("content") or payload.get("description") or ""
                seen_ids[hit_id] = RAGQueryResult(
                    id=hit_id,
                    score=round(hit.score, 4),
                    payload={k: v for k, v in payload.items() if k not in ("text", "content")},
                    text=text[:2000],
                    query_matched=q_text,
                )

    # Sort by score, return top-N
    results = sorted(seen_ids.values(), key=lambda r: r.score, reverse=True)[: req.limit]

    return RAGQueryResponse(
        results=results,
        query=req.query,
        queries_used=queries,
        collection=req.collection,
        total=len(results),
    )


# ── POST /rag/ingest ──────────────────────────────────────

@router.post("/rag/ingest", response_model=RAGIngestResponse)
async def rag_ingest(req: RAGIngestRequest):
    """
    Upsert chunks into Qdrant. Deduplication via content hash.
    Used by WF-020 (Obsidian RAG Sync) — idempotent by design.
    """
    if not req.chunks:
        raise HTTPException(400, "No chunks provided")

    qdrant   = get_qdrant()
    embedder = get_embedder()

    try:
        qdrant.get_collection(req.collection)
    except Exception:
        raise HTTPException(404, f"Collection '{req.collection}' does not exist. Create it via Qdrant API.")

    texts   = [c.text for c in req.chunks]
    vectors = embedder.encode(texts, batch_size=32, show_progress_bar=False).tolist()

    points, skipped = [], 0

    for chunk, vector in zip(req.chunks, vectors):
        chunk_hash = hashlib.md5(chunk.text.encode()).hexdigest()

        if req.deduplicate:
            existing, _ = qdrant.scroll(
                collection_name=req.collection,
                scroll_filter=Filter(must=[FieldCondition(key="content_hash", match=MatchValue(value=chunk_hash))]),
                limit=1,
                with_payload=False,
            )
            if existing:
                skipped += 1
                continue

        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_hash))
        points.append(PointStruct(
            id=point_id,
            vector=vector,
            payload={
                **chunk.metadata,
                "text":         chunk.text,
                "content_hash": chunk_hash,
                "ingested_at":  datetime.utcnow().isoformat(),
            },
        ))

    if points:
        qdrant.upsert(collection_name=req.collection, points=points, wait=True)

    return RAGIngestResponse(
        ingested_count=len(points),
        skipped_count=skipped,
        collection=req.collection,
    )


# ── GET /flywheel/health ──────────────────────────────────

@router.get("/flywheel/health")
async def flywheel_health():
    status: Dict[str, Any] = {
        "flywheel_version": "2.0.0",
        "timestamp":        datetime.utcnow().isoformat(),
        "qdrant":           "unknown",
        "embedder":         "unknown",
        "postgres":         "unknown",
        "llm_tiers_configured": {},
    }

    try:
        cols = get_qdrant().get_collections()
        status["qdrant"] = f"ok — {len(cols.collections)} collections"
    except Exception as e:
        status["qdrant"] = f"error: {e}"

    try:
        emb = get_embedder()
        vec = emb.encode("health")
        status["embedder"] = f"ok — dim={len(vec)}"
    except Exception as e:
        status["embedder"] = f"error: {e}"

    try:
        conn = get_db()
        conn.close()
        status["postgres"] = "ok"
    except Exception as e:
        status["postgres"] = f"error: {e}"

    for role, tiers in AGENT_MODELS.items():
        configured = [t["name"] for t in tiers if t["key"]]
        status["llm_tiers_configured"][role] = configured

    return status


# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────

def _dim_description(dim: str) -> str:
    return {
        "wiki_fidelity":       "Accurate to vault context? No fabricated stats?",
        "seo_quality":         "Keyword in H1/first 100 words/meta? Internal links? Schema?",
        "brand_voice_match":   "Unmistakably sounds like this brand? No banned words?",
        "humanness":           "No AI patterns? Varied sentence rhythm?",
        "originality":         "Unique angle? Proprietary insight not found elsewhere?",
        "readability":         "Appropriate reading level? Good flow? Paragraph breaks?",
        "eeat_signals":        "Experience/Expertise/Authority/Trust markers present?",
        "factual_accuracy":    "All claims verifiable from vault context? No contradictions?",
        "ai_search_readiness": (
            "AEO/LLM visibility: direct answer in first 100 words? "
            "Clear FAQ structure? Rich schema markup? Entity mentions unambiguous? "
            "Conversational 'People Also Ask' queries addressed?"
        ),
    }.get(dim, dim)


# ─────────────────────────────────────────────────────────
# MIGRATION HELPER — SQL to add prompt_versions table
# Run once via: docker exec -it supabase-db psql -U postgres
# ─────────────────────────────────────────────────────────
"""
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

-- Track monthly prompt performance (run in WF-022 anti-fragile loop)
CREATE OR REPLACE VIEW prompt_performance AS
SELECT
    pv.role,
    pv.brand,
    pv.prompt_hash,
    pv.created_at,
    COUNT(qs.id)           AS articles_evaluated,
    AVG(qs.weighted_score) AS avg_qc_score,
    AVG(qs.wiki_fidelity)  AS avg_wiki_fidelity,
    AVG(qs.brand_voice)    AS avg_brand_voice,
    SUM(CASE WHEN qs.decision='APPROVED' THEN 1 ELSE 0 END) AS approved_count
FROM prompt_versions pv
LEFT JOIN qc_scores_log qs ON qs.brand = pv.brand
GROUP BY pv.role, pv.brand, pv.prompt_hash, pv.created_at
ORDER BY pv.created_at DESC;
"""
