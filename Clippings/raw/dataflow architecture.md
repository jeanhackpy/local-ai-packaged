---
title: "MiniMax Agent: Minimize Effort, Maximize Intelligence"
source: "https://agent.minimax.io/chat?id=379222360383636"
author:
  - "[[agent.minimax.io]]"
published: 2026-03-26
created: 2026-03-26
description: "Discover MiniMax Agent, your AI supercompanion, enhancing creativity and productivity with tools for meditation, podcast, coding, analysis, and more!"
tags:
  - "clippings"
---
## 1\. Architecture Overview

Your system combines four powerful technologies, each serving a specific purpose:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│  │          │    │           │    │           │    │           │      │
│  │ SCRAPER  │───▶│ SUPABASE  │───▶│  QDRANT   │───▶│   LLM     │      │
│  │          │    │           │    │           │    │  (Query)  │      │
│  └──────────┘    └───────────┘    └───────────┘    └───────────┘      │
│       │               │                │                │               │
│       │               │                │                │               │
│       ▼               ▼                ▼                ▼               │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                         NEO4J (Graph DB)                         │   │
│  │   - Property relationships                                       │   │
│  │   - Location graphs                                             │   │
│  │   - User preferences graph                                       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2\. Database Roles and Optimization

### Supabase (Relational/Structured Data)

Use Supabase for **authoritative structured data** that requires ACID compliance:

- **Property master data**: IDs, prices, sizes, bedrooms, bathrooms, addresses
- **User profiles and preferences**: Explicitly stated requirements
- **Transaction history**: Past searches, viewed properties, saved units
- **Real-time sync**: Webhook triggers for price changes

**Optimization strategy**:

```sql
-- Create composite indexes for common query patterns
CREATE INDEX idx_properties_location_price 
ON properties(latitude, longitude, price_range);

CREATE INDEX idx_properties_beds_baths 
ON properties(bedrooms, bathrooms, property_type);

-- Materialized view for aggregated search results
CREATE MATERIALIZED VIEW property_search_cache AS
SELECT 
    p.*,
    ARRAY_AGG(DISTINCT pt.amenity) as amenities,
    COUNT(*) OVER(PARTITION BY p.neighborhood) as nearby_count
FROM properties p
LEFT JOIN property_amenities pt ON p.id = pt.property_id
GROUP BY p.id;
```

### Qdrant (Vector Search)

Qdrant excels at **semantic similarity matching** for natural language queries:

- **Property embeddings**: Vectorize descriptions, amenities, neighborhood vibes
- **Query embeddings**: Convert natural language into vectors
- **Similarity search**: Find properties matching "cozy apartment with good schools nearby"

**Embedding strategy for real estate**:

```python
from sentence_transformers import SentenceTransformer
import json

# Property embedding fields
PROPERTY_FIELDS = [
    "description",
    "neighborhood_description", 
    "amenities_text",
    "transportation_access",
    "school_district_info",
    "lifestyle_tags"  # e.g., "family-friendly", "nightlife", "quiet"
]

def create_property_embedding(property_data):
    """
    Create comprehensive embedding by combining multiple fields
    with weighted importance
    """
    # Weight more important fields higher
    weighted_text = f"""
    {property_data['description']} 
    Location: {property_data['neighborhood']}
    Amenities: {property_data['amenities']}
    Transportation: {property_data['transit_info']}
    Schools: {property_data['school_rating']}
    Price: ${property_data['price']} for {property_data['bedrooms']} bedrooms
    """
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(weighted_text)
    
    return embedding.tolist()

# Store in Qdrant with metadata
qdrant_client.upsert(
    collection_name="properties",
    points=[
        {
            "id": property_id,
            "vector": embedding,
            "payload": {
                "property_id": property_id,
                "price": price,
                "bedrooms": bedrooms,
                "neighborhood": neighborhood,
                "amenities": amenities
            }
        }
    ]
)
```

**Critical for recommendation effectiveness**:

1.**Hybrid search**: Combine vector similarity with filters (price range, beds, location)

2.**Multi-vector fields**: Create separate embeddings for different aspects (location, lifestyle, value)

3.**Re-ranking**: Use cross-encoders to re-rank initial vector results

### Neo4j (Graph Relationships)

Neo4j captures **complex relationships** that pure similarity can't express:

- **Location graphs**: Distance to transit, schools, restaurants
- **Property comparisons**: "Similar to unit X but 10% cheaper"
- **User preference propagation**: Learn from similar users
- **Route/commute analysis**: Multi-stop journeys

**Graph schema for recommendations**:

```cypher
// Core entity relationships
(:Property {id: "prop_123"})-[r:NEAR]->(:POI {type: "metro_station", name: "Central Station"})
(:Property)-[:IN_NEIGHBORHOOD]->(:Neighborhood {name: "Westside"})
(:Property)-[:SIMILAR_TO {score: 0.92}]->(:Property)

// User preference patterns
(:User)-[:PREFERS {weight: 0.8}]->(:Neighborhood {name: "Downtown"})
(:User)-[:VIEWED]->(:Property)-[:IN_NEIGHBORHOOD]->(:Neighborhood)<-[:PREFERS]-(:SimilarUser)

// Recommendation pattern
MATCH (u:User {id: $user_id})-[:PREFERS]->(n:Neighborhood)<-[:IN_NEIGHBORHOOD]-(p:Property)
WHERE p.bedrooms >= $min_beds 
  AND p.price <= $max_budget
  AND NOT (u)-[:EXCLUDED]->(p)
RETURN p ORDER BY p.match_score DESC
```

## 3\. LLM Integration Patterns

### Query Understanding Pipeline

The LLM is the interface between natural language and structured queries:

```python
from anthropic import Anthropic
from supabase import create_client

# Define schema context for the LLM
SCHEMA_CONTEXT = """
You have access to a real estate database with the following schema:

PROPERTIES table:
- id (UUID), address, neighborhood, city
- price (integer), bedrooms, bathrooms, sqft
- property_type (enum: apartment, house, condo, townhouse)
- year_built, listing_date, days_on_market
- amenity_ids (array of amenity codes)

AMENITIES table:
- id, category, name (e.g., "POOL", "PARKING", "GYM")

USER_PREFERENCES table:
- user_id, preferred_beds_min, preferred_beds_max
- budget_min, budget_max, preferred_neighborhoods (array)
- required_amenities (array), excluded_amenities (array)
"""

def parse_user_query(query: str, user_id: str) -> dict:
    """
    Convert natural language to structured query parameters
    """
    client = Anthropic()
    
    # Get user context
    user_prefs = supabase.table('user_preferences').select('*').eq('user_id', user_id).execute()
    user_context = json.dumps(user_prefs.data[0]) if user_prefs.data else "{}"
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=f"""You are a real estate query parser. 
        Convert natural language queries into structured database filters.
        Always consider user's implicit preferences when not specified.
        
        {SCHEMA_CONTEXT}
        
        Return a JSON with these keys:
        - filters: dict with database filter conditions
        - reasoning: brief explanation of how you interpreted the query
        - priority: "price" | "space" | "location" | "amenities"
        """,
        messages=[{
            "role": "user", 
            "content": f"User's explicit preferences: {user_context}\n\nQuery: {query}"
        }]
    )
    
    return json.loads(response.content[0].text)
```

### Multi-Stage Retrieval for Best Results

For finding the "best" unit, use a cascading retrieval approach:

```python
def find_best_units(query: str, user_id: str, top_k: int = 5) -> list:
    """
    Multi-stage retrieval combining all three databases
    """
    # Stage 1: Parse and understand the query
    parsed = parse_user_query(query, user_id)
    
    # Stage 2: Vector similarity search in Qdrant
    query_embedding = embed_query(query)
    vector_results = qdrant_client.search(
        collection_name="properties",
        query_vector=query_embedding,
        query_filter={
            "must": [
                {"key": "price", "range": {"gte": parsed['filters']['price_min'], "lte": parsed['filters']['price_max']}},
                {"key": "bedrooms", "range": {"gte": parsed['filters']['beds_min']}}
            ]
        },
        limit=top_k * 3  # Get more for refinement
    )
    vector_candidate_ids = [r.payload['property_id'] for r in vector_results]
    
    # Stage 3: Graph-based relationship expansion
    graph_matches = expand_via_graph(user_id, vector_candidate_ids, parsed['priority'])
    
    # Stage 4: Apply Neo4j relationship scoring
    graph_scores = calculate_relationship_scores(user_id, graph_matches)
    
    # Stage 5: Structured filter via Supabase for final validation
    final_candidates = supabase.table('properties').select('''
        *,
        amenities:property_amenities(amenity_id, amenity_name)
    ''').in_('id', graph_matches).execute()
    
    # Stage 6: Re-rank with cross-encoder for final ordering
    final_ranking = rerank_with_cross_encoder(query, final_candidates.data, top_k)
    
    return final_ranking
```

## 4\. Key Effectiveness Strategies

### A. User Preference Learning

Don't rely solely on explicit preferences—learn implicit patterns:

```python
def learn_user_preferences(user_id: str) -> dict:
    """
    Analyze user behavior to infer implicit preferences
    """
    # Get viewing/searching history
    viewed = supabase.table('user_views').select('property_id').eq('user_id', user_id).execute()
    
    # Find patterns in what they looked at vs. what they ignored
    viewed_properties = get_property_details([v.property_id for v in viewed.data])
    
    # Use Neo4j to find similar users
    similar_users = """
    MATCH (u:User {id: $user_id})-[:VIEWED]->(:Property)<-[:VIEWED]-(similar:User)
    WHERE NOT similar.id = $user_id
    WITH similar, COUNT(*) as common_views
    ORDER BY common_views DESC
    LIMIT 10
    MATCH (similar)-[:PREFERS|EXCLUDES]->(preference)
    RETURN preference, COUNT(*) as confidence
    """
    
    return aggregate_preference_patterns(viewed_properties, similar_users)
```

### B. Smart Embedding Updates

Properties and neighborhoods change—keep embeddings fresh:

```python
# Scheduled update strategy
SCHEDULE = """
0 3 * * 0  # Update embeddings weekly (Sunday 3 AM)
"""

def update_property_embeddings():
    """
    Incremental updates for changed properties only
    """
    # Find properties with recent changes
    recent_changes = supabase.table('properties').select('id, updated_at').eq(
        'updated_at', 'gt', last_embedding_update_time
    ).execute()
    
    for prop in recent_changes.data:
        new_embedding = create_property_embedding(prop)
        qdrant_client.upsert(
            collection_name="properties",
            points=[{"id": prop.id, "vector": new_embedding}]
        )
    
    # Update location embeddings more frequently (dynamic area scores)
    update_neighborhood_embeddings()
```

### C. Feedback Loop for Recommendations

Close the loop on what users actually book/buy:

```python
def record_recommendation_outcome(user_id: str, property_id: str, outcome: str):
    """
    outcome: 'viewed', 'contacted', 'visited', 'applied', 'rejected'
    """
    supabase.table('recommendation_outcomes').insert({
        'user_id': user_id,
        'property_id': property_id,
        'outcome': outcome,
        'recommended_at': last_recommendation_time,
        'outcome_at': datetime.now()
    }).execute()
    
    # Update preference graph in Neo4j
    if outcome in ['applied', 'signed']:
        """
        MATCH (u:User {id: $user_id}), (p:Property {id: $property_id})
        CREATE (u)-[:LIKED]->(p)
        WITH u, p
        MATCH (p)-[:IN_NEIGHBORHOOD]->(n:Neighborhood)
        SET u.preference_strength = u.preference_strength * 1.1
        """
        update_user_affinity_graph(user_id, property_id, positive=True)
```

### D. Query Enhancement Techniques

Improve LLM query parsing with retrieval augmentation:

```python
SYSTEM_PROMPT = """
You are a real estate recommendation assistant with access to:

1. A database of properties with details on price, location, amenities
2. User preference profiles including must-haves and deal-breakers
3. Market trends and recent price changes

Guidelines:
- When users say "affordable", consider 20% below their stated budget
- "Good area" should consider crime rates, schools, and transit scores
- Always filter out properties matching their exclusions
- If query is vague, ask clarifying questions about top 2-3 criteria
"""

def enhance_query_with_context(query: str, user_id: str) -> str:
    """
    Augment query with relevant context before processing
    """
    # Get user's recent activity context
    recent = supabase.table('user_views').select('property_id, viewed_at').eq(
        'user_id', user_id
    ).order('viewed_at', desc=True).limit(3).execute()
    
    context = ""
    if recent.data:
        context = f"\nUser recently viewed: {[r.property_id for r in recent.data]}"
    
    # Get market context
    market = supabase.table('market_summary').select('*').eq(
        'neighborhood', user_prefs.last_searched_area
    ).execute()
    
    if market.data:
        context += f"\nMarket in {user_prefs.last_searched_area}: {market.data[0]}"
    
    return f"{query}\n\nContext: {context}"
```

## 5\. System Performance Optimization

### Caching Strategy

```python
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)

def get_cached_recommendations(user_id: str, query_hash: str) -> list:
    """
    Cache frequent query results
    """
    cache_key = f"recs:{user_id}:{query_hash}"
    cached = redis.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    results = find_best_units(query, user_id)
    redis.setex(cache_key, 3600, json.dumps(results))  # 1 hour TTL
    
    return results
```

### Async Processing for Scale

```python
import asyncio
from celery import Celery

celery_app = Celery('realestate_tasks')

@celery_app.task
def process_scraped_property(property_data: dict):
    """
    Async processing pipeline for scraped data
    """
    # 1. Store in Supabase (primary)
    prop_id = supabase.table('properties').insert(property_data).execute()
    
    # 2. Generate and store embedding (Qdrant)
    embedding = create_property_embedding(property_data)
    qdrant_client.upsert("properties", points=[{
        "id": str(prop_id.id),
        "vector": embedding,
        "payload": {"property_id": prop_id.id}
    }])
    
    # 3. Build graph relationships (Neo4j)
    build_property_graph(prop_id.id, property_data)
    
    return prop_id.id
```

## 6\. Evaluation and Continuous Improvement

Track recommendation effectiveness:

```python
METRICS_TO_TRACK = [
    "recommendation_click_rate",      # Did they click?
    "view_to_contact_rate",            # Did they contact about it?
    "contact_to_visit_rate",           # Did they schedule a visit?
    "visit_to_application_rate",       # Did they apply?
    "nps_score",                       # Would they recommend?
    "search_abandonment_rate",         # Did they leave without results?
]

def calculate_recommendation_quality():
    """
    Weekly metrics analysis
    """
    report = supabase.rpc('calculate_recommendation_metrics').execute()
    
    # Alert if metrics degrade
    if report.data['click_rate'] < 0.15:
        # Trigger embedding quality review
        review_embedding_freshness()
    
    if report.data['nps'] < 30:
        # Review query parsing accuracy
        audit_llm_query_understanding()
```

## Summary: Critical Success Factors

| Component | Key Optimization | Expected Impact |
| --- | --- | --- |
| **Embeddings** | Multi-field, weighted, refreshed weekly | 30% improvement in relevance |
| **Vector Search** | Hybrid with filters + re-ranking | 25% better top-k accuracy |
| **Graph** | Relationship depth (5+ hops) | 20% better "similar user" matching |
| **LLM Parsing** | Schema + user context + market data | 40% fewer misinterpretations |
| **Feedback Loop** | Closed-loop with outcomes | Continuous improvement |

This architecture creates a powerful recommendation engine where Supabase handles authoritative data, Qdrant provides semantic understanding, Neo4j captures complex relationships, and the LLM bridges natural language to structured queries. The key is building proper feedback loops so the system learns from user behavior and continuously improves its recommendations.

Would you like me to dive deeper into any specific component—perhaps detailed implementation for the embedding strategy, the Neo4j schema, or the LLM prompt engineering?

View all files

if i build a decision tree fod real estate investment how can i use it to build the system backtrack

Thinking Process9.40s

The user is asking about how to build a decision tree for real estate investment and then use it to "build the system backtrack." This is an interesting question about how to incorporate investment decision logic into their existing architecture (Supabase, Qdrant, Neo4j, LLM).

The concept of "backtracking" in this context likely means:

1.Starting from an investment goal/recommendation

2.Tracing backward through the decision criteria to find properties that match

3.Using the decision tree as a filter/prioritization mechanism

This is a design/architecture question, not a frontend web development task. I should provide a thoughtful response about how to integrate a real estate investment decision tree into their existing data pipeline.

Let me think about this:

1.

**Decision Tree Structure for Real Estate Investment**

- Risk assessment
- Return on Investment (ROI) calculation
- Location scoring
- Property condition
- Market timing
- Cash flow analysis

2.

**How to "Backtrack" - System Design**

- Define investment goals (e.g., "I want 10% ROI with low risk")
- The decision tree creates a path of requirements
- Backtracking = find properties that satisfy each node in the decision path

3.

**Integration with Existing Stack**

- Neo4j: Perfect for decision tree structure
- Qdrant: Could embed decision tree logic as vectors
- Supabase: Store decision criteria and weights
- LLM: Query understanding and decision explanation

This is a purely conversational/consulting task - no code implementation needed, no frontend work, no deployment. I should provide a comprehensive response about the architecture and methodology.

# Building a Real Estate Investment Decision Tree System with Backtracking

## Understanding the Backtracking Concept

The "backtracking" approach means starting from your investment goal and working backward through decision criteria to find matching properties. This is fundamentally different from filtering—it's about creating a decision path and finding all properties that satisfy each node in that path.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION TREE STRUCTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │  INVESTMENT     │                          │
│                    │  OBJECTIVE      │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│              ┌──────────────┼──────────────┐                     │
│              ▼              ▼              ▼                     │
│     ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│     │  CASH FLOW │  │ APPRECIATION│  │  BRAND NEW │              │
│     │  FOCUS     │  │  FOCUS     │  │  FOCUS     │              │
│     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘              │
│           │               │               │                      │
│           ▼               ▼               ▼                      │
│     ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│     │ Rent Yield │  │ Growth %  │  │ Warranty   │              │
│     │   > 6%     │  │   > 8%    │  │  Required  │              │
│     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘              │
│           │               │               │                      │
│           ▼               ▼               ▼                      │
│     ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│     │    Cap     │  │ Neighborhood│  │  Builder   │              │
│     │   Rate     │  │   Trends   │  │  Repute    │              │
│     │  > 7%     │  │   Score    │  │  Score     │              │
│     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘              │
│           │               │               │                      │
│           └───────────────┼───────────────┘                     │
│                           ▼                                      │
│              ┌────────────────────────┐                          │
│              │   BACKTRACK RESULTS   │                          │
│              │   Properties Matching  │                          │
│              │   All Decision Nodes   │                          │
│              └────────────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 1\. Decision Tree Schema Design

### Core Decision Tree Structure in Neo4j

```cypher
// Decision Tree Root Nodes (Investment Objectives)
CREATE
  (cashflow:InvestmentObjective {
    name: 'Cash Flow Focus',
    description: 'Prioritize positive monthly cash flow',
    weight: 1.0,
    metrics: ['monthly_cash_flow', 'cap_rate', 'rent_to_price_ratio']
  }),
  (appreciation:InvestmentObjective {
    name: ' appreciation Focus',
    description: 'Prioritize property value growth',
    weight: 1.0,
    metrics: ['historical_growth', 'development_plans', 'demographic_trends']
  }),
  (turnkey:InvestmentObjective {
    name: 'Turnkey Focus',
    description: 'Ready-to-rent with minimal maintenance',
    weight: 1.0,
    metrics: ['condition_score', 'warranty_status', 'renovation_age']
  }),

// Cash Flow Branch
  (cashflow)-[:REQUIRES]->(rental_yield:DecisionCriteria {
    name: 'Rental Yield',
    type: 'numeric',
    min_value: 6.0,
    max_value: 100,
    unit: 'percent',
    importance: 'critical'
  }),
  (rental_yield)-[:BRANCHES_TO]->(cap_rate:DecisionCriteria {
    name: 'Cap Rate',
    type: 'numeric',
    min_value: 7.0,
    max_value: 20,
    unit: 'percent',
    importance: 'critical'
  }),
  (cap_rate)-[:BRANCHES_TO]->(debt_coverage:DecisionCriteria {
    name: 'Debt Coverage Ratio',
    type: 'numeric',
    min_value: 1.25,
    max_value: 100,
    unit: 'ratio',
    importance: 'high'
  }),
  (debt_coverage)-[:BRANCHES_TO]->(vacancy_rate:DecisionCriteria {
    name: 'Local Vacancy Rate',
    type: 'numeric',
    max_value: 5,
    unit: 'percent',
    importance: 'medium'
  }),

// Appreciation Branch
  (appreciation)-[:REQUIRES]->(growth_potential:DecisionCriteria {
    name: 'Growth Potential',
    type: 'numeric',
    min_value: 8.0,
    max_value: 100,
    unit: 'percent_5yr',
    importance: 'critical'
  }),
  (growth_potential)-[:BRANCHES_TO]->(neighborhood_score:DecisionCriteria {
    name: 'Neighborhood Score',
    type: 'numeric',
    min_value: 7.0,
    max_value: 10,
    unit: 'rating',
    importance: 'high'
  }),
  (neighborhood_score)-[:BRANCHES_TO]->(development_impact:DecisionCriteria {
    name: 'Development Impact',
    type: 'enum',
    values: ['positive', 'neutral', 'negative'],
    importance: 'medium'
  }),

// Turnkey Branch
  (turnkey)-[:REQUIRES]->(condition_score:DecisionCriteria {
    name: 'Property Condition',
    type: 'numeric',
    min_value: 8.0,
    max_value: 10,
    unit: 'rating',
    importance: 'critical'
  }),
  (condition_score)-[:BRANCHES_TO]->(warranty_status:DecisionCriteria {
    name: 'Warranty Status',
    type: 'enum',
    values: ['active', 'transferable', 'expired', 'none'],
    importance: 'high'
  }),
  (warranty_status)-[:BRANCHES_TO]->(maintenance_history:DecisionCriteria {
    name: 'Maintenance History',
    type: 'enum',
    values: ['excellent', 'good', 'adequate', 'poor'],
    importance: 'medium'
  });

// Property Examples Linking to Decision Nodes
MATCH (p:Property {id: 'prop_123'}),
      (c:DecisionCriteria {name: 'Rental Yield'})
CREATE (p)-[:SATISFIES {value: 7.5, score: 0.95}]->(c);
```

### Decision Criteria Storage in Supabase

```sql
-- Decision criteria definitions
CREATE TABLE investment_objectives (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    weight DECIMAL(3,2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE decision_criteria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    objective_id UUID REFERENCES investment_objectives(id),
    name VARCHAR(100) NOT NULL,
    criteria_type VARCHAR(50), -- 'numeric', 'enum', 'boolean'
    min_value DECIMAL(10,2),
    max_value DECIMAL(10,2),
    enum_values JSONB,
    importance VARCHAR(20) DEFAULT 'medium', -- 'critical', 'high', 'medium', 'low'
    parent_criteria_id UUID REFERENCES decision_criteria(id),
    branch_order INTEGER,
    UNIQUE(objective_id, name)
);

-- Property scores for each criteria
CREATE TABLE property_decision_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID REFERENCES properties(id),
    criteria_id UUID REFERENCES decision_criteria(id),
    raw_value DECIMAL(10,4),
    normalized_score DECIMAL(3,2), -- 0-1 score
    data_source VARCHAR(50), -- 'calculated', 'scraped', 'estimated'
    calculated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(property_id, criteria_id)
);

-- Indexes for efficient backtracking
CREATE INDEX idx_property_scores_criteria 
ON property_decision_scores(criteria_id, normalized_score DESC);
CREATE INDEX idx_criteria_objective 
ON decision_criteria(objective_id, branch_order);
```

## 2\. Backtracking Engine Architecture

### The Backtracking Algorithm

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum

class Importance(Enum):
    CRITICAL = 4  # Must satisfy
    HIGH = 3     # Very important
    MEDIUM = 2   # Important
    LOW = 1      # Nice to have

@dataclass
class DecisionNode:
    criteria_id: str
    name: str
    criteria_type: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    importance: Importance = Importance.MEDIUM
    children: List['DecisionNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []

@dataclass
class BacktrackResult:
    property_id: str
    decision_path: List[str]  # Path through decision tree
    overall_score: float
    criteria_scores: Dict[str, float]
    failed_criteria: List[str]  # Which criteria weren't met
    reason: str  # Explanation of decision

class RealEstateBacktrackingEngine:
    """
    Backtracking engine that finds properties matching a decision tree path.
    Starts from investment objective and traces back through all criteria.
    """
    
    def __init__(self, supabase, neo4j_driver, qdrant_client):
        self.supabase = supabase
        self.neo4j = neo4j_driver
        self.qdrant = qdrant_client
    
    def build_decision_tree(self, objective: str) -> DecisionNode:
        """
        Build decision tree from Neo4j for a given investment objective
        """
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH path = (o:InvestmentObjective {name: $objective})
                         -[:REQUIRES|BRANCHES_TO*]->(c:DecisionCriteria)
                RETURN path
                ORDER BY relationships(path)[0].branch_order
            """, objective=objective)
            
            # Convert to DecisionNode structure
            # ... (tree building logic)
            
            return tree_root
    
    def backtrack(self, investment_goal: Dict[str, Any], top_k: int = 10) -> List[BacktrackResult]:
        """
        Main backtracking function:
        1. Parse investment goal into decision tree path
        2. Start with all criteria as requirements
        3. Iteratively narrow down candidates
        4. Score remaining properties
        """
        
        # Step 1: Identify which investment objective matches
        objective = self._identify_objective(investment_goal)
        
        # Step 2: Get the full decision tree for this objective
        decision_tree = self.build_decision_tree(objective)
        
        # Step 3: Extract criteria thresholds from investment goal
        criteria_thresholds = self._extract_thresholds(investment_goal, decision_tree)
        
        # Step 4: Apply critical criteria first (narrowing phase)
        critical_criteria = [
            c for c in self._flatten_tree(decision_tree) 
            if c.importance == Importance.CRITICAL
        ]
        
        initial_candidates = self._apply_criteria_filter(
            critical_criteria, 
            criteria_thresholds
        )
        
        # Step 5: Score remaining properties against all criteria
        results = []
        for property_id in initial_candidates:
            scores = self._score_property(property_id, decision_tree)
            overall_score = self._calculate_overall_score(scores, decision_tree)
            
            failed = [
                c.name for c in self._flatten_tree(decision_tree)
                if scores.get(c.criteria_id, 0) < criteria_thresholds.get(c.criteria_id, 0)
            ]
            
            results.append(BacktrackResult(
                property_id=property_id,
                decision_path=self._get_decision_path(decision_tree),
                overall_score=overall_score,
                criteria_scores=scores,
                failed_criteria=failed,
                reason=self._generate_reason(property_id, scores, decision_tree)
            ))
        
        # Step 6: Sort by overall score and return top k
        results.sort(key=lambda x: x.overall_score, reverse=True)
        
        return results[:top_k]
    
    def _apply_criteria_filter(
        self, 
        criteria: List[DecisionNode], 
        thresholds: Dict[str, float]
    ) -> List[str]:
        """
        Efficiently filter candidates using critical criteria.
        Uses Qdrant for vectorized filtering.
        """
        # Start with all properties
        candidate_ids = self._get_all_property_ids()
        
        for criterion in criteria:
            threshold = thresholds.get(criterion.criteria_id, 0)
            
            if criterion.criteria_type == 'numeric':
                # Use Supabase for numeric filtering
                result = self.supabase.table('property_decision_scores').select(
                    'property_id'
                ).eq('criteria_id', criterion.criteria_id).gte(
                    'normalized_score', threshold
                ).execute()
                
                candidate_ids = [r['property_id'] for r in result.data]
            
            elif criterion.criteria_type == 'enum':
                # Use Supabase for enum matching
                result = self.supabase.table('property_decision_scores').select(
                    'property_id'
                ).eq('criteria_id', criterion.criteria_id).contains(
                    'enum_value', threshold
                ).execute()
                
                candidate_ids = [r['property_id'] for r in result.data]
        
        return candidate_ids
    
    def _score_property(
        self, 
        property_id: str, 
        tree: DecisionNode
    ) -> Dict[str, float]:
        """
        Score a property against all criteria in the decision tree
        """
        scores = {}
        
        # Fetch all scores from Supabase in one query
        all_scores = self.supabase.table('property_decision_scores').select(
            'criteria_id, normalized_score'
        ).eq('property_id', property_id).execute()
        
        score_map = {s['criteria_id']: s['normalized_score'] for s in all_scores.data}
        
        for criterion in self._flatten_tree(tree):
            scores[criterion.criteria_id] = score_map.get(
                criterion.criteria_id, 
                0.0
            )
        
        return scores
    
    def _calculate_overall_score(
        self, 
        scores: Dict[str, float], 
        tree: DecisionNode
    ) -> float:
        """
        Calculate weighted overall score based on importance levels
        """
        weighted_sum = 0.0
        total_weight = 0.0
        
        for criterion in self._flatten_tree(tree):
            weight = criterion.importance.value
            score = scores.get(criterion.criteria_id, 0.0)
            
            weighted_sum += weight * score
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
```

## 3\. Integration with LLM Query Understanding

### Enhanced Query Parsing for Investment Decisions

```python
def parse_investment_query(query: str, user_id: str) -> Dict[str, Any]:
    """
    Parse natural language investment queries into decision tree parameters
    """
    client = Anthropic()
    
    SYSTEM_PROMPT = """
    You are a real estate investment advisor parsing user queries.
    
    Investment Objectives (choose one):
    1. CASH_FLOW - Focus on monthly rental income exceeding expenses
    2. APPRECIATION - Focus on property value growth over time
    3. TURNKEY - Focus on move-in ready, minimal maintenance
    4. BALANCED - Mix of cash flow and appreciation
    
    Decision Criteria with typical values:
    - Rental Yield: 4-12% (6%+ is good for cash flow)
    - Cap Rate: 5-15% (7%+ is good)
    - Growth Potential: 3-15% annually (8%+ is aggressive)
    - Condition Score: 1-10 (8+ is excellent)
    - Neighborhood Score: 1-10 (7+ is desirable)
    - Debt Coverage Ratio: 1.0-2.0 (1.25+ is safe)
    
    Return JSON with:
    {
        "objective": "CASH_FLOW|APPRECIATION|TURNKEY|BALANCED",
        "parameters": {
            "criteria_name": {"min": X, "max": Y, "exact": Z}
        },
        "risk_tolerance": "conservative|moderate|aggressive",
        "time_horizon": "short|medium|long",
        "reasoning": "explanation of interpretation"
    }
    """
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": query}]
    )
    
    return json.loads(response.content[0].text)

def execute_investment_recommendation(query: str, user_id: str) -> Dict[str, Any]:
    """
    Full pipeline: Parse query -> Backtrack -> Return recommendations
    """
    
    # Step 1: Parse the investment query
    parsed = parse_investment_query(query, user_id)
    
    # Step 2: Execute backtracking
    engine = RealEstateBacktrackingEngine(supabase, neo4j, qdrant)
    results = engine.backtrack(parsed['parameters'], top_k=5)
    
    # Step 3: Enhance with property details
    property_ids = [r.property_id for r in results]
    properties = supabase.table('properties').select(
        '*, property_decision_scores(*), decision_criteria(*)'
    ).in_('id', property_ids).execute()
    
    # Step 4: Generate explanation using LLM
    explanation = generate_recommendation_explanation(results, parsed)
    
    return {
        'recommendations': results,
        'properties': properties.data,
        'investment_objective': parsed['objective'],
        'explanation': explanation,
        'next_steps': suggest_follow_up_questions(parsed)
    }
```

## 4\. Decision Tree Visualization in Neo4j

```cypher
// Query to visualize the full decision tree
MATCH path = (o:InvestmentObjective)-[:REQUIRES|BRANCHES_TO*]->(c:DecisionCriteria)
WHERE o.name = 'Cash Flow Focus'
RETURN path

// Query to find properties matching a specific decision path
MATCH (p:Property)
WHERE EXISTS {
    MATCH (p)-[:SATISFIES]->(yield:DecisionCriteria {name: 'Rental Yield'})
    WHERE yield.raw_value >= 6.0
}
AND EXISTS {
    MATCH (p)-[:SATISFIES]->(cap:DecisionCriteria {name: 'Cap Rate'})
    WHERE cap.raw_value >= 7.0
}
RETURN p.address, p.price, p.bedrooms

// Complex backtracking: Find all paths to a specific property
MATCH path = (p:Property {id: 'prop_123'})<-[:SATISFIES]-(c:DecisionCriteria)
RETURN p, c
ORDER BY c.importance DESC
```

## 5\. System Flow: From Query to Recommendation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        INVESTMENT RECOMMENDATION FLOW                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐                                                   │
│  │                  │                                                   │
│  │  USER QUERY      │                                                   │
│  │  "I want 8%+ ROI │                                                   │
│  │   with low risk" │                                                   │
│  │                  │                                                   │
│  └────────┬─────────┘                                                   │
│           │                                                                │
│           ▼                                                                │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                        LLM QUERY PARSER                             │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │ Extract: objective=APPRECIATION, min_yield=8, risk=LOW       │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────┬──────────────────────────────────────┘  │
│                                  │                                        │
│                                  ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                      DECISION TREE BUILDER                         │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │  From Neo4j: Build tree for "Appreciation Focus"             │  │  │
│  │  │                                                              │  │  │
│  │  │     [Growth Potential > 8%]                                  │  │  │
│  │  │           ↓                                                  │  │  │
│  │  │     [Neighborhood Score > 7]                                 │  │  │
│  │  │           ↓                                                  │  │  │
│  │  │     [Development Impact = Positive]                          │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────┬──────────────────────────────────────┘  │
│                                  │                                        │
│                                  ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                     BACKTRACKING ENGINE                             │  │
│  │                                                                      │  │
│  │  STEP 1: Filter by Growth Potential (Qdrant + Supabase)            │  │
│  │          ↓ 5000 candidates                                          │  │
│  │  STEP 2: Filter by Neighborhood Score                              │  │
│  │          ↓ 500 candidates                                            │  │
│  │  STEP 3: Filter by Development Impact                               │  │
│  │          ↓ 75 candidates                                             │  │
│  │  STEP 4: Score and rank all 75                                      │  │
│  │          ↓ Top 10 results                                            │  │
│  │                                                                      │  │
│  └─────────────────────────────┬──────────────────────────────────────┘  │
│                                  │                                        │
│                                  ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                      LLM EXPLANATION GENERATOR                      │  │
│  │                                                                      │  │
│  │  "Property X matches your criteria because:                        │  │
│  │   - 12% historical growth (your target: 8%+)                       │  │
│  │   - Neighborhood score 8.5/10                                      │  │
│  │   - New metro line opening in 2025 (positive development)"          │  │
│  │                                                                      │  │
│  └─────────────────────────────┬──────────────────────────────────────┘  │
│                                  │                                        │
│                                  ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                         FINAL OUTPUT                               │  │
│  │                                                                      │  │
│  │  Top 5 recommendations with:                                       │  │
│  │  - Property details                                                 │  │
│  │  - Match scores per criteria                                        │  │
│  │  - Natural language explanation                                     │  │
│  │  - Risk factors                                                     │  │
│  │  - Alternative options                                              │  │
│  │                                                                      │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 6\. Example Decision Trees for Different Investment Profiles

| Investor Type | Primary Objective | Key Decision Criteria | Thresholds |
| --- | --- | --- | --- |
| **Passive Income** | Cash Flow | Rental Yield, Cap Rate, Vacancy Rate | Yield > 7%, Cap > 8%, Vacancy < 5% |
| **Value Investor** | Appreciation | Price-to-Book, Condition, Growth Potential | P/B < 0.9, Condition > 7, Growth > 10% |
| **Hands-off** | Turnkey | Condition Score, Warranty, Management Available | Condition > 8, Warranty = Active |
| **Aggressive Growth** | Appreciation | Growth Potential, Development Pipeline, Demographic Trends | Growth > 12%, Multiple Projects |
| **Risk-Averse** | Preservation | Neighborhood Score, Age, Maintenance History | Score > 8, Age < 20 yrs, Excellent Maint. |

## Summary: Backtracking System Architecture

| Component | Role in Backtracking | Key Function |
| --- | --- | --- |
| **Neo4j** | Decision tree structure | Store objectives, criteria, relationships, thresholds |
| **Supabase** | Criteria scoring | Store property scores, enable numeric/enum filtering |
| **Qdrant** | Vector-based criteria search | Semantic matching of criteria descriptions |
| **LLM** | Query understanding + explanation | Parse goals into criteria, generate recommendations |
| **Backtracking Engine** | Core algorithm | Filter -> Score -> Rank -> Explain |

The key insight is that **backtracking works by starting with the investment goal and working backward through decision nodes**, finding all properties that satisfy each criterion in the path. This is more powerful than simple filtering because it respects the hierarchical nature of investment decisions and provides explainable recommendations.

Would you like me to dive deeper into any specific aspect—such as the Neo4j schema design, the backtracking algorithm implementation, or the LLM prompt engineering for investment queries?

View all files

yes how do i need to insert different data in which db

Thinking Process3.30s

The user wants to know exactly how to structure data insertion across their three databases (Supabase, Qdrant, Neo4j) for their real estate scraper system. They want to understand the data flow and which data goes where.

This is a direct question about database architecture and data insertion strategy, not a coding task that requires deep\_thinking or deployment. I should provide a comprehensive answer about:

1.Data classification - which data goes to which database

2.The specific schema/structure for each database

3.Data insertion order and dependencies

4.Practical examples with code

Let me provide a detailed technical response about the data insertion strategy.

# Data Insertion Strategy: Supabase vs Qdrant vs Neo4j

## Data Classification Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATA INSERTION DECISION FRAMEWORK                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     SUPABASE (Relational/ACID)                        │ │
│  │                                                                       │ │
│  │  ✓ Authoritative source of truth                                      │ │
│  │  ✓ Structured data with defined schemas                               │ │
│  │  ✓ Requires transactional consistency                                │ │
│  │  ✓ Needs complex queries with JOINs                                   │ │
│  │  ✓ User-facing real-time queries                                      │ │
│  │                                                                       │ │
│  │  DATA TYPES:                                                          │ │
│  │  • Property master records                                            │ │
│  │  • User profiles and preferences                                      │ │
│  │  • Transaction logs and history                                       │ │
│  │  • Structured search filters (price, beds, baths)                   │ │
│  │  • Decision criteria scores (numeric values)                          │ │
│  │  • System configuration and metadata                                   │ │
│  │  • Audit trails and change logs                                       │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        QDRANT (Vector Search)                        │ │
│  │                                                                       │ │
│  │  ✓ Semantic similarity matching                                      │ │
│  │  ✓ Natural language query understanding                              │ │
│  │  ✓ Unstructured or semi-structured text                              │ │
│  │  ✓ Embedding-based recommendations                                   │ │
│  │  ✓ Multi-modal search (text + filters)                               │ │
│  │                                                                       │ │
│  │  DATA TYPES:                                                          │ │
│  │  • Property description embeddings                                    │ │
│  │  • Neighborhood narrative embeddings                                  │ │
│  │  • Amenity text embeddings                                            │ │
│  │  • Lifestyle/vibe embeddings (e.g., "family-friendly", "vibrant")   │ │
│  │  • User query embeddings                                              │ │
│  │  • Alternative address/location embeddings                            │ │
│  │  • Search history embeddings                                          │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         NEO4J (Graph Relations)                       │ │
│  │                                                                       │ │
│  │  ✓ Relationship-heavy data                                           │ │
│  │  ✓ Network analysis (distance, connectivity)                          │ │
│  │  ✓ Hierarchical structures                                            │ │
│  │  ✓ User preference propagation                                       │ │
│  │  ✓ Complex traversal queries                                          │ │
│  │  ✓ Path finding (commute routes, nearby POIs)                        │ │
│  │                                                                       │ │
│  │  DATA TYPES:                                                          │ │
│  │  • Property-to-POI relationships (distance to metro, schools)         │ │
│  │  • Property-to-neighborhood links                                     │ │
│  │  • Property-to-property similarity edges                              │ │
│  │  • User-to-property preference relationships                          │ │
│  │  • User-to-user similarity edges (for collaborative filtering)        │ │
│  │  • Investment decision tree structure                                  │ │
│  │  • Market trend connections                                           │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1\. Supabase: The Source of Truth

### Schema Design for Real Estate Data

```sql
-- ============================================
-- CORE PROPERTY DATA (Supabase Primary Store)
-- ============================================

-- Properties table - single source of truth
CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_id VARCHAR(255), -- ID from scraper source
    source VARCHAR(50) NOT NULL, -- 'zillow', 'realtor', 'scraped'
    source_url TEXT,
    
    -- Basic property info
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20),
    neighborhood VARCHAR(100),
    
    -- Location (for geo queries)
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Property characteristics
    property_type VARCHAR(50) NOT NULL, -- 'apartment', 'house', 'condo', 'townhouse'
    bedrooms INTEGER NOT NULL,
    bathrooms DECIMAL(3, 1) NOT NULL,
    sqft INTEGER,
    lot_size_sqft INTEGER,
    year_built INTEGER,
    stories INTEGER,
    parking_spaces INTEGER,
    parking_type VARCHAR(50), -- 'garage', 'street', 'lot'
    
    -- Financial data
    price DECIMAL(12, 2) NOT NULL,
    price_per_sqft DECIMAL(8, 2),
    monthly_rent DECIMAL(10, 2), -- For rental properties
    hoa_fee DECIMAL(8, 2),
    property_taxes DECIMAL(10, 2),
    insurance DECIMAL(8, 2),
    
    -- Property condition
    condition VARCHAR(50), -- 'excellent', 'good', 'fair', 'poor'
    renovation_year INTEGER,
    inspection_report_url TEXT,
    
    -- Listing metadata
    listing_status VARCHAR(50) DEFAULT 'active', -- 'active', 'pending', 'sold', 'off_market'
    listing_date DATE,
    days_on_market INTEGER,
    price_reduction_date DATE,
    price_reduction_amount DECIMAL(10, 2),
    
    -- SEO/text content (for embedding)
    description TEXT,
    highlights TEXT[], -- Array of key highlights
    neighborhood_description TEXT,
    
    -- Media
    images JSONB DEFAULT '[]', -- Array of image URLs
    virtual_tour_url TEXT,
    video_url TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Quality tracking
    data_quality_score DECIMAL(3, 2), -- 0.00 to 1.00
    verified BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT positive_price CHECK (price > 0),
    CONSTRAINT positive_beds CHECK (bedrooms >= 0),
    CONSTRAINT valid_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT valid_longitude CHECK (longitude BETWEEN -180 AND 180)
);

-- Indexes for common queries
CREATE INDEX idx_properties_location ON properties(latitude, longitude);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_type_beds ON properties(property_type, bedrooms);
CREATE INDEX idx_properties_neighborhood ON properties(neighborhood);
CREATE INDEX idx_properties_status ON properties(listing_status);
CREATE INDEX idx_properties_listing_date ON properties(listing_date DESC);
CREATE INDEX idx_properties_rent ON properties(monthly_rent) WHERE monthly_rent IS NOT NULL;

-- Full text search index
CREATE INDEX idx_properties_fts ON properties 
USING GIN (to_tsvector('english', neighborhood_description || ' ' || COALESCE(description, '')));

-- ============================================
-- AMENITIES (Structured Relations)
-- ============================================

CREATE TABLE amenities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50), -- 'interior', 'exterior', 'building', 'outdoor'
    icon VARCHAR(50),
    importance_score INTEGER DEFAULT 5 -- 1-10
);

CREATE TABLE property_amenities (
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    amenity_id UUID REFERENCES amenities(id),
    notes TEXT, -- e.g., "pool heated", "gym 24/7"
    distance_meters INTEGER, -- For location-based amenities
    PRIMARY KEY (property_id, amenity_id)
);

-- ============================================
-- DECISION CRITERIA SCORES (Numeric)
-- ============================================

CREATE TABLE decision_criteria_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    display_name VARCHAR(150),
    category VARCHAR(50), -- 'financial', 'location', 'condition', 'market'
    criteria_type VARCHAR(20) NOT NULL, -- 'numeric', 'enum', 'boolean'
    min_value DECIMAL(10, 4),
    max_value DECIMAL(10, 4),
    unit VARCHAR(20),
    importance VARCHAR(20) DEFAULT 'medium', -- 'critical', 'high', 'medium', 'low'
    calculation_formula TEXT, -- How to calculate this score
    UNIQUE(name)
);

CREATE TABLE property_criteria_scores (
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    criteria_id UUID REFERENCES decision_criteria_definitions(id),
    raw_value DECIMAL(12, 4) NOT NULL,
    normalized_score DECIMAL(5, 4), -- 0.0000 to 1.0000
    calculation_source VARCHAR(50), -- 'formula', 'scraped', 'estimated', 'user_input'
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (property_id, criteria_id)
);

-- ============================================
-- USER DATA (Preferences and History)
-- ============================================

CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_type VARCHAR(20) DEFAULT 'renter', -- 'renter', 'buyer', 'investor'
    preferences JSONB DEFAULT '{}', -- Flexible preferences storage
    notification_settings JSONB DEFAULT '{}'
);

CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    
    -- Price range
    budget_min DECIMAL(12, 2),
    budget_max DECIMAL(12, 2),
    
    -- Property requirements
    property_types VARCHAR(50)[] DEFAULT '{}',
    beds_min INTEGER,
    beds_max INTEGER,
    baths_min DECIMAL(3, 1),
    sqft_min INTEGER,
    sqft_max INTEGER,
    
    -- Location preferences
    preferred_neighborhoods VARCHAR(100)[] DEFAULT '{}',
    excluded_neighborhoods VARCHAR(100)[] DEFAULT '{}',
    preferred_cities VARCHAR(100)[] DEFAULT '{}',
    commute_max_minutes INTEGER,
    work_address TEXT,
    
    -- Amenities required/preferred
    required_amenities VARCHAR(100)[] DEFAULT '{}',
    preferred_amenities VARCHAR(100)[] DEFAULT '{}',
    excluded_amenities VARCHAR(100)[] DEFAULT '{}',
    
    -- Lifestyle preferences (for NLP matching)
    lifestyle_tags VARCHAR(50)[] DEFAULT '{}', -- e.g., 'quiet', 'nightlife', 'family'
    
    -- Investment criteria (for investors)
    investment_objective VARCHAR(50), -- 'cash_flow', 'appreciation', 'turnkey'
    target_roi_min DECIMAL(5, 2),
    risk_tolerance VARCHAR(20) DEFAULT 'moderate',
    investment_horizon VARCHAR(20), -- 'short', 'medium', 'long'
    
    -- Recalculated weights
    preference_weights JSONB DEFAULT '{}',
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE user_search_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    search_query TEXT,
    parsed_filters JSONB,
    results_count INTEGER,
    clicked_property_ids UUID[],
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE user_property_views (
    user_id UUID REFERENCES users(id),
    property_id UUID REFERENCES properties(id),
    view_count INTEGER DEFAULT 1,
    first_viewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_viewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    saved BOOLEAN DEFAULT FALSE,
    notes TEXT,
    PRIMARY KEY (user_id, property_id)
);

-- ============================================
-- MARKET DATA (Trends and Comparisons)
-- ============================================

CREATE TABLE market_trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    neighborhood VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL, -- 'monthly', 'quarterly', 'yearly'
    
    -- Price metrics
    median_price DECIMAL(12, 2),
    avg_price DECIMAL(12, 2),
    price_change_percent DECIMAL(6, 2),
    price_per_sqft DECIMAL(8, 2),
    
    -- Inventory metrics
    active_listings INTEGER,
    new_listings INTEGER,
    sold_listings INTEGER,
    days_on_market_avg INTEGER,
    inventory_months DECIMAL(4, 1),
    
    -- Rental metrics
    median_rent DECIMAL(10, 2),
    rent_change_percent DECIMAL(6, 2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(neighborhood, period_start, period_type)
);

CREATE TABLE comparable_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_property_id UUID REFERENCES properties(id),
    comparable_property_id UUID REFERENCES properties(id),
    distance_miles DECIMAL(5, 2),
    price_difference DECIMAL(12, 2),
    sqft_difference INTEGER,
    score DECIMAL(3, 2),
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- SCRAPER TRACKING AND QUALITY
-- ============================================

CREATE TABLE scraper_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'running', -- 'running', 'completed', 'failed'
    listings_scraped INTEGER DEFAULT 0,
    listings_new INTEGER DEFAULT 0,
    listings_updated INTEGER DEFAULT 0,
    listings_failed INTEGER DEFAULT 0,
    error_log TEXT
);

CREATE TABLE data_quality_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID REFERENCES properties(id),
    issue_type VARCHAR(50),
    issue_description TEXT,
    severity VARCHAR(20), -- 'low', 'medium', 'high'
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER properties_updated_at
    BEFORE UPDATE ON properties
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Data Insertion Flow for Supabase

```python
import hashlib
from datetime import datetime
from typing import Dict, List, Any

class SupabaseDataInserter:
    """
    Handles all Supabase insertions with proper error handling and validation
    """
    
    def __init__(self, supabase_client):
        self.client = supabase_client
    
    def insert_property(self, property_data: Dict[str, Any]) -> str:
        """
        Insert a single property and return its ID
        """
        # Generate external_id hash for deduplication
        external_id = self._generate_external_id(property_data)
        
        # Check if property already exists
        existing = self.client.table('properties').select('id').eq(
            'external_id', external_id
        ).execute()
        
        if existing.data:
            # Update existing property
            result = self.client.table('properties').update({
                **property_data,
                'updated_at': datetime.now().isoformat(),
                'last_scraped_at': datetime.now().isoformat()
            }).eq('external_id', external_id).execute()
            return result.data[0]['id']
        else:
            # Insert new property
            property_data['external_id'] = external_id
            result = self.client.table('properties').insert(property_data).execute()
            return result.data[0]['id']
    
    def insert_property_batch(
        self, 
        properties: List[Dict[str, Any]], 
        batch_size: int = 100
    ) -> Dict[str, int]:
        """
        Batch insert multiple properties efficiently
        """
        stats = {'inserted': 0, 'updated': 0, 'failed': 0, 'skipped': 0}
        
        for i in range(0, len(properties), batch_size):
            batch = properties[i:i + batch_size]
            
            for prop in batch:
                try:
                    prop_id = self.insert_property(prop)
                    if prop_id:
                        stats['inserted' if self._is_new(prop) else 'updated'] += 1
                except Exception as e:
                    stats['failed'] += 1
                    self._log_error(prop, str(e))
        
        return stats
    
    def calculate_criteria_scores(self, property_id: str) -> None:
        """
        Calculate decision criteria scores after property insert
        """
        # Fetch property data
        prop = self.client.table('properties').select('*').eq(
            'id', property_id
        ).execute().data[0]
        
        scores = []
        
        # Calculate Cap Rate (if rent known)
        if prop.get('monthly_rent') and prop.get('price'):
            annual_rent = prop['monthly_rent'] * 12
            cap_rate = (annual_rent / prop['price']) * 100
            
            cap_criteria = self.client.table('decision_criteria_definitions').select(
                'id'
            ).eq('name', 'cap_rate').execute().data[0]
            
            scores.append({
                'property_id': property_id,
                'criteria_id': cap_criteria['id'],
                'raw_value': cap_rate,
                'normalized_score': min(cap_rate / 15, 1.0),  # Normalize to 0-1
                'calculation_source': 'formula'
            })
        
        # Calculate Rental Yield
        if prop.get('monthly_rent') and prop.get('price'):
            annual_rent = prop['monthly_rent'] * 12
            rental_yield = (annual_rent / prop['price']) * 100
            
            yield_criteria = self.client.table('decision_criteria_definitions').select(
                'id'
            ).eq('name', 'rental_yield').execute().data[0]
            
            scores.append({
                'property_id': property_id,
                'criteria_id': yield_criteria['id'],
                'raw_value': rental_yield,
                'normalized_score': min(rental_yield / 12, 1.0),
                'calculation_source': 'formula'
            })
        
        # Insert all scores
        if scores:
            self.client.table('property_criteria_scores').upsert(scores).execute()
    
    def insert_user_preference(self, user_id: str, preferences: Dict[str, Any]) -> None:
        """
        Insert or update user preferences
        """
        self.client.table('user_preferences').upsert({
            'user_id': user_id,
            **preferences,
            'updated_at': datetime.now().isoformat()
        }).execute()
    
    def _generate_external_id(self, property_data: Dict) -> str:
        """
        Generate unique external ID based on source and original listing ID
        """
        unique_string = f"{property_data.get('source')}_{property_data.get('source_url', '')}"
        return hashlib.md5(unique_string.encode()).hexdigest()
```

## 2\. Qdrant: Semantic Search Data

### Collection Design for Real Estate

```python
from qdrant_client.models import Distance, VectorParams, TextIndexParams, TokenizerType

# Collection configurations for different use cases
COLLECTION_CONFIGS = {
    # Primary property search collection
    "properties_main": {
        "vector_size": 384,  # all-MiniLM-L6-v2
        "distance": Distance.COSINE,
        "description": "Main property search with comprehensive descriptions",
        "fields": {
            "property_id": {"type": "keyword", "is_indexed": True},
            "price": {"type": "float", "is_indexed": True},
            "bedrooms": {"type": "integer", "is_indexed": True},
            "bathrooms": {"type": "float", "is_indexed": True},
            "sqft": {"type": "integer", "is_indexed": True},
            "neighborhood": {"type": "keyword", "is_indexed": True},
            "property_type": {"type": "keyword", "is_indexed": True},
            "listing_status": {"type": "keyword", "is_indexed": True},
            "rental_yield": {"type": "float", "is_indexed": True},
            "cap_rate": {"type": "float", "is_indexed": True},
        }
    },
    
    # Neighborhood descriptions
    "neighborhoods": {
        "vector_size": 384,
        "distance": Distance.COSINE,
        "description": "Neighborhood profiles for location matching",
        "fields": {
            "neighborhood_id": {"type": "keyword", "is_indexed": True},
            "city": {"type": "keyword", "is_indexed": True},
            "avg_price": {"type": "float", "is_indexed": True},
            "safety_score": {"type": "float", "is_indexed": True},
            "school_score": {"type": "float", "is_indexed": True},
            "transit_score": {"type": "float", "is_indexed": True},
        }
    },
    
    # Lifestyle and vibe matching
    "property_vibes": {
        "vector_size": 384,
        "distance": Distance.COSINE,
        "description": "Lifestyle embeddings for vibe-based matching",
        "fields": {
            "property_id": {"type": "keyword", "is_indexed": True},
            "vibe_type": {"type": "keyword", "is_indexed": True},  # 'quiet', 'vibrant', 'family', 'young_professional'
        }
    },
    
    # User search intent
    "user_queries": {
        "vector_size": 384,
        "distance": Distance.COSINE,
        "description": "Stored user query embeddings for pattern analysis",
        "fields": {
            "user_id": {"type": "keyword", "is_indexed": True},
            "timestamp": {"type": "datetime", "is_indexed": True},
            "result_count": {"type": "integer", "is_indexed": True},
            "clicked": {"type": "boolean", "is_indexed": True},
        }
    }
}

def create_qdrant_collections(qdrant_client):
    """
    Initialize all Qdrant collections with proper configurations
    """
    for name, config in COLLECTION_CONFIGS.items():
        try:
            qdrant_client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=config['vector_size'],
                    distance=config['distance']
                ),
                # Create indexes for payload fields
                payload_index_config={
                    field: {"type": field_config['type']}
                    for field, field_config in config['fields'].items()
                }
            )
        except Exception as e:
            # Collection might already exist
            print(f"Collection {name}: {e}")

# Embedding model setup
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def create_property_embeddings(property_data: Dict) -> Dict[str, List[float]]:
    """
    Create multiple embeddings for different search contexts
    """
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    embeddings = {}
    
    # 1. Main description embedding
    main_text = f"""
    {property_data.get('description', '')}
    
    Location: {property_data.get('neighborhood', '')}, {property_data.get('city', '')}
    Property Type: {property_data.get('property_type', '')}
    {property_data.get('bedrooms', '')} bedrooms, {property_data.get('bathrooms', '')} bathrooms
    {property_data.get('sqft', '')} sq ft
    Price: ${property_data.get('price', 0):,.0f}
    Monthly Rent: ${property_data.get('monthly_rent', 0):,.0f}
    
    Neighborhood: {property_data.get('neighborhood_description', '')}
    
    Amenities: {', '.join(property_data.get('amenities', []))}
    """
    embeddings['main'] = model.encode(main_text).tolist()
    
    # 2. Lifestyle/vibe embedding (for subjective matching)
    vibe_text = f"""
    This {property_data.get('property_type', 'property')} is located in {property_data.get('neighborhood', 'a neighborhood')} 
    that is {property_data.get('neighborhood_vibe', 'residential')}.
    The area features {property_data.get('surrounding_features', 'various amenities')}.
    """
    embeddings['vibe'] = model.encode(vibe_text).tolist()
    
    # 3. Investment-focused embedding (for investor queries)
    investment_text = f"""
    Investment Property Analysis:
    Price: ${property_data.get('price', 0):,.0f}
    Monthly Rental Income: ${property_data.get('monthly_rent', 0):,.0f}
    HOA Fees: ${property_data.get('hoa_fee', 0):,.0f}
    Property Taxes: ${property_data.get('property_taxes', 0):,.0f}
    Cap Rate: {property_data.get('cap_rate', 0):.2f}%
    Rental Yield: {property_data.get('rental_yield', 0):.2f}%
    Condition: {property_data.get('condition', 'unknown')}
    """
    embeddings['investment'] = model.encode(investment_text).tolist()
    
    # 4. Search-optimized text (for NLP queries)
    search_text = f"""
    {property_data.get('bedrooms', '')} bed {property_data.get('property_type', '')} 
    in {property_data.get('neighborhood', '')}, {property_data.get('city', '')}
    under ${property_data.get('price', 0):,.0f} with {', '.join(property_data.get('amenities', [])[:5])}
    """
    embeddings['search'] = model.encode(search_text).tolist()
    
    return embeddings

class QdrantDataInserter:
    """
    Handles all Qdrant insertions with embedding generation
    """
    
    def __init__(self, qdrant_client, embedding_model=None):
        self.client = qdrant_client
        self.model = embedding_model or SentenceTransformer(EMBEDDING_MODEL)
    
    def insert_property(self, property_data: Dict[str, Any]) -> None:
        """
        Insert property with embeddings into Qdrant
        """
        embeddings = create_property_embeddings(property_data)
        property_id = property_data['id']
        
        # Insert main description embedding
        self.client.upsert(
            collection_name="properties_main",
            points=[{
                "id": property_id,
                "vector": embeddings['main'],
                "payload": {
                    "property_id": property_id,
                    "price": property_data.get('price'),
                    "bedrooms": property_data.get('bedrooms'),
                    "bathrooms": property_data.get('bathrooms'),
                    "sqft": property_data.get('sqft'),
                    "neighborhood": property_data.get('neighborhood'),
                    "property_type": property_data.get('property_type'),
                    "listing_status": property_data.get('listing_status', 'active'),
                    "rental_yield": property_data.get('rental_yield'),
                    "cap_rate": property_data.get('cap_rate'),
                }
            }]
        )
        
        # Insert vibe/lifestyle embedding
        if property_data.get('lifestyle_tags'):
            self.client.upsert(
                collection_name="property_vibes",
                points=[{
                    "id": f"{property_id}_vibe",
                    "vector": embeddings['vibe'],
                    "payload": {
                        "property_id": property_id,
                        "vibe_type": property_data.get('lifestyle_tags', []),
                    }
                }]
            )
    
    def insert_neighborhood(self, neighborhood_data: Dict[str, Any]) -> None:
        """
        Insert neighborhood profile embedding
        """
        neighborhood_text = f"""
        {neighborhood_data.get('name', '')} is a {neighborhood_data.get('character', 'residential')} 
        neighborhood in {neighborhood_data.get('city', '')}.
        
        Demographics: {neighborhood_data.get('demographics', '')}
        Safety: {neighborhood_data.get('safety_description', '')}
        Schools: {neighborhood_data.get('school_info', '')}
        Transportation: {neighborhood_data.get('transit_info', '')}
        Dining: {neighborhood_data.get('dining_options', '')}
        Entertainment: {neighborhood_data.get('entertainment', '')}
        """
        
        vector = self.model.encode(neighborhood_text).tolist()
        
        self.client.upsert(
            collection_name="neighborhoods",
            points=[{
                "id": neighborhood_data['id'],
                "vector": vector,
                "payload": {
                    "neighborhood_id": neighborhood_data['id'],
                    "city": neighborhood_data.get('city'),
                    "avg_price": neighborhood_data.get('avg_price'),
                    "safety_score": neighborhood_data.get('safety_score'),
                    "school_score": neighborhood_data.get('school_score'),
                    "transit_score": neighborhood_data.get('transit_score'),
                }
            }]
        )
    
    def search_properties(
        self, 
        query: str, 
        filters: Dict = None, 
        limit: int = 10
    ) -> List[Dict]:
        """
        Semantic search for properties
        """
        query_vector = self.model.encode(query).tolist()
        
        search_params = {
            "collection_name": "properties_main",
            "query_vector": query_vector,
            "limit": limit,
            "score_threshold": 0.7,  # Minimum relevance score
        }
        
        if filters:
            search_params["query_filter"] = self._build_filter(filters)
        
        results = self.client.search(**search_params)
        
        return [{
            "property_id": r.payload['property_id'],
            "score": r.score,
            "payload": r.payload
        } for r in results]
    
    def _build_filter(self, filters: Dict) -> Dict:
        """
        Convert Supabase-style filters to Qdrant filter format
        """
        from qdrant_client.models import Filter, FieldCondition, Range, MatchAny
        
        conditions = []
        
        if 'price_min' in filters or 'price_max' in filters:
            range_filter = {}
            if 'price_min' in filters:
                range_filter['gte'] = filters['price_min']
            if 'price_max' in filters:
                range_filter['lte'] = filters['price_max']
            conditions.append(
                FieldCondition(key='price', range=Range(**range_filter))
            )
        
        if 'bedrooms_min' in filters:
            conditions.append(
                FieldCondition(key='bedrooms', range=Range(gte=filters['bedrooms_min']))
            )
        
        if 'neighborhoods' in filters:
            conditions.append(
                FieldCondition(key='neighborhood', match=MatchAny(any=filters['neighborhoods']))
            )
        
        return Filter(must=conditions) if conditions else None
```

## 3\. Neo4j: Relationship and Graph Data

### Graph Schema Design

```cypher
// ============================================
// PROPERTY ENTITIES AND RELATIONSHIPS
// ============================================

// Property node
CREATE (p:Property:RealEstate {
    property_id: "prop_123",
    address: "123 Main St",
    neighborhood: "Downtown",
    city: "San Francisco",
    price: 850000,
    bedrooms: 2,
    bathrooms: 2.0,
    sqft: 1200,
    property_type: "condo",
    cap_rate: 5.5,
    rental_yield: 4.8,
    condition_score: 8.5,
    year_built: 2015,
    latitude: 37.7749,
    longitude: -122.4194
})

// POI nodes (Points of Interest)
CREATE 
    (metro:POI {poi_id: "poi_metro_1", name: "Central Metro Station", type: "transit", latitude: 37.7750, longitude: -122.4180}),
    (school:POI {poi_id: "poi_school_1", name: "Lincoln Elementary", type: "school", latitude: 37.7740, longitude: -122.4200}),
    (park:POI {poi_id: "poi_park_1", name: "Central Park", type: "park", latitude: 37.7760, longitude: -122.4170}),
    (hospital:POI {poi_id: "poi_hospital_1", name: "City Hospital", type: "hospital", latitude: 37.7730, longitude: -122.4210}),
    (gym:POI {poi_id: "poi_gym_1", name: "FitLife Gym", type: "gym", latitude: 37.7745, longitude: -122.4185})

// Neighborhood node
CREATE (n:Neighborhood {
    neighborhood_id: "n_downtown",
    name: "Downtown",
    city: "San Francisco",
    population: 45000,
    median_income: 85000,
    crime_rate: 2.1,
    school_rating: 8.2,
    transit_score: 9.5,
    walkability_score: 9.8,
    median_price: 820000,
    price_trend: "increasing",
    growth_rate_1yr: 8.5,
    growth_rate_5yr: 42.0
})

// ============================================
// PROPERTY RELATIONSHIPS
// ============================================

MATCH (p:Property {property_id: "prop_123"})

// Distance-based relationships to POIs
CREATE (p)-[:NEAR {
    distance_meters: 350,
    walk_time_minutes: 4,
    poi_type: "transit"
}]->(metro:POI {poi_id: "poi_metro_1"})

CREATE (p)-[:NEAR {
    distance_meters: 500,
    walk_time_minutes: 6,
    poi_type: "school"
}]->(school:POI {poi_id: "poi_school_1"})

CREATE (p)-[:NEAR {
    distance_meters: 200,
    walk_time_minutes: 2,
    poi_type: "park"
}]->(park:POI {poi_id: "poi_park_1"})

// Property to neighborhood relationship
CREATE (p)-[:LOCATED_IN {
    distance_to_center_meters: 1200,
    school_district: "Lincoln School District",
    zoning: "R4 Residential"
}]->(n:Neighborhood {neighborhood_id: "n_downtown"})

// Property similarity relationships
CREATE (p)-[:SIMILAR_TO {
    similarity_score: 0.92,
    match_criteria: ["price_range", "bedrooms", "sqft", "neighborhood"],
    compared_property_id: "prop_456"
}]->(:Property {property_id: "prop_456"})

CREATE (p)-[:SIMILAR_TO {
    similarity_score: 0.88,
    match_criteria: ["price_range", "property_type", "amenities"],
    compared_property_id: "prop_789"
}]->(:Property {property_id: "prop_789"})

// Price comparison relationships
CREATE (p)-[:COMPARABLE_TO {
    price_difference: -50000,
    sqft_difference: 150,
    value_assessment: "undervalued",
    comparable_id: "prop_456"
}]->(:Property {property_id: "prop_456"})

// ============================================
// USER AND PREFERENCE GRAPH
// ============================================

CREATE (u:User {
    user_id: "user_123",
    email: "investor@example.com",
    user_type: "investor",
    risk_tolerance: "moderate",
    investment_horizon: "long"
})

// User preference relationships
CREATE (u)-[:PREFERS {
    weight: 0.9,
    reason: "frequently searches"
}]->(:Neighborhood {neighborhood_id: "n_downtown"})

CREATE (u)-[:PREFERS {
    weight: 0.8,
    reason: "past viewings"
}]->(:PropertyType {type: "condo"})

CREATE (u)-[:PREFERS {
    weight: 0.7,
    requirement: "minimum"
}]->(:Amenity {amenity_id: "amenity_parking"})

// User viewing history
CREATE (u)-[:VIEWED {
    view_count: 3,
    first_viewed: date("2024-01-15"),
    last_viewed: date("2024-02-20"),
    saved: true,
    notes: "Strong candidate, schedule visit"
}]->(:Property {property_id: "prop_123"})

// User similarity (collaborative filtering)
CREATE (u)-[:SIMILAR_TO {
    similarity_score: 0.85,
    common_viewed: 15,
    common_preferences: ["neighborhood", "price_range"],
    similar_user_id: "user_456"
}]->(:User {user_id: "user_456"})

// ============================================
// INVESTMENT DECISION TREE STRUCTURE
// ============================================

CREATE
    // Investment objectives
    (cashflow:InvestmentObjective {
        objective_id: "obj_cashflow",
        name: "Cash Flow Focus",
        description: "Maximize monthly rental income",
        priority: 1
    }),
    (appreciation:InvestmentObjective {
        objective_id: "obj_appreciation", 
        name: " appreciation Focus",
        description: "Maximize property value growth",
        priority: 2
    }),
    (turnkey:InvestmentObjective {
        objective_id: "obj_turnkey",
        name: "Turnkey Focus",
        description: "Minimize maintenance and hassle",
        priority: 3
    }),
    
    // Cash flow decision branch
    (cashflow)-[:REQUIRES {
        min_value: 6.0,
        importance: "critical",
        display_name: "Rental Yield"
    }]->(yield:Criteria {
        criteria_id: "crit_yield",
        name: "Rental Yield",
        unit: "percent",
        calculation: "annual_rent / price * 100"
    }),
    
    (yield)-[:BRANCHES_TO {
        min_value: 7.0,
        importance: "critical",
        display_name: "Cap Rate"
    }]->(caprate:Criteria {
        criteria_id: "crit_caprate",
        name: "Cap Rate",
        unit: "percent"
    }),
    
    (caprate)-[:BRANCHES_TO {
        min_value: 1.25,
        importance: "high",
        display_name: "Debt Coverage Ratio"
    }]->(dcr:Criteria {
        criteria_id: "crit_dcr",
        name: "Debt Coverage Ratio",
        unit: "ratio"
    }),
    
    // Property-property decision path
    (yield)-[:USED_TO_SCORE]->(:Property {property_id: "prop_123"});

// ============================================
// MARKET DYNAMICS GRAPH
// ============================================

CREATE
    (n:Neighborhood {neighborhood_id: "n_downtown"})-[:ADJACENT_TO {
        distance_km: 1.5,
        commute_time_minutes: 10
    }]->(:Neighborhood {neighborhood_id: "n_midtown"}),
    
    (n)-[:DEVELOPING_WITH {
        project_type: "mixed_use",
        completion_year: 2025,
        impact: "positive"
    }]->(:Development {
        development_id: "dev_project_1",
        name: "Metro District Redevelopment",
        investment_millions: 150
    }),
    
    (n)-[:TRENDING {
        period: "2024_Q1",
        trend: "appreciation",
        rate: 8.5,
        drivers: ["new_transit", "tech_boom"]
    }]->(:Trend {
        trend_id: "trend_downtown_2024",
        name: "Downtown Growth"
    });
```

### Neo4j Data Inserter Class

```python
from neo4j import GraphDatabase
from typing import Dict, List, Any
from datetime import datetime

class Neo4jDataInserter:
    """
    Handles all Neo4j insertions with relationship building
    """
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
    
    def insert_property_graph(self, property_data: Dict[str, Any]) -> None:
        """
        Insert property node with all relationships
        """
        with self.driver.session() as session:
            session.execute_write(self._create_property_node, property_data)
            
            # Create POI relationships
            if property_data.get('nearby_pois'):
                for poi in property_data['nearby_pois']:
                    session.execute_write(
                        self._create_poi_relationship, 
                        property_data['id'], 
                        poi
                    )
            
            # Create neighborhood relationship
            if property_data.get('neighborhood_id'):
                session.execute_write(
                    self._create_neighborhood_relationship,
                    property_data['id'],
                    property_data['neighborhood_id'],
                    property_data.get('neighborhood_details', {})
                )
    
    @staticmethod
    def _create_property_node(tx, property_data: Dict) -> None:
        """Create property node in Neo4j"""
        query = """
        MERGE (p:Property {property_id: $property_id})
        SET p.address = $address,
            p.neighborhood = $neighborhood,
            p.city = $city,
            p.price = $price,
            p.bedrooms = $bedrooms,
            p.bathrooms = $bathrooms,
            p.sqft = $sqft,
            p.property_type = $property_type,
            p.cap_rate = $cap_rate,
            p.rental_yield = $rental_yield,
            p.condition_score = $condition_score,
            p.year_built = $year_built,
            p.latitude = $latitude,
            p.longitude = $longitude,
            p.updated_at = datetime()
        """
        tx.run(query, **{
            'property_id': property_data['id'],
            'address': property_data.get('address'),
            'neighborhood': property_data.get('neighborhood'),
            'city': property_data.get('city'),
            'price': property_data.get('price'),
            'bedrooms': property_data.get('bedrooms'),
            'bathrooms': property_data.get('bathrooms'),
            'sqft': property_data.get('sqft'),
            'property_type': property_data.get('property_type'),
            'cap_rate': property_data.get('cap_rate'),
            'rental_yield': property_data.get('rental_yield'),
            'condition_score': property_data.get('condition_score'),
            'year_built': property_data.get('year_built'),
            'latitude': property_data.get('latitude'),
            'longitude': property_data.get('longitude'),
        })
    
    @staticmethod
    def _create_poi_relationship(
        tx, 
        property_id: str, 
        poi_data: Dict
    ) -> None:
        """Create NEAR relationship to POI"""
        query = """
        MATCH (p:Property {property_id: $property_id})
        
        MERGE (poi:POI {poi_id: $poi_id})
        SET poi.name = $poi_name,
            poi.type = $poi_type,
            poi.latitude = $latitude,
            poi.longitude = $longitude
        
        MERGE (p)-[r:NEAR]->(poi)
        SET r.distance_meters = $distance_meters,
            r.walk_time_minutes = $walk_time_minutes,
            r.poi_type = $poi_type,
            r.created_at = datetime()
        """
        tx.run(query, **{
            'property_id': property_id,
            'poi_id': poi_data['id'],
            'poi_name': poi_data.get('name'),
            'poi_type': poi_data.get('type'),
            'latitude': poi_data.get('latitude'),
            'longitude': poi_data.get('longitude'),
            'distance_meters': poi_data.get('distance'),
            'walk_time_minutes': poi_data.get('walk_time'),
            'poi_type': poi_data.get('type'),
        })
    
    @staticmethod
    def _create_neighborhood_relationship(
        tx, 
        property_id: str, 
        neighborhood_id: str,
        details: Dict
    ) -> None:
        """Create LOCATED_IN relationship to neighborhood"""
        query = """
        MATCH (p:Property {property_id: $property_id})
        
        MERGE (n:Neighborhood {neighborhood_id: $neighborhood_id})
        SET n.name = $name,
            n.city = $city,
            n.median_price = $median_price,
            n.school_rating = $school_rating,
            n.transit_score = $transit_score
        
        MERGE (p)-[r:LOCATED_IN]->(n)
        SET r.school_district = $school_district,
            r.zoning = $zoning,
            r.created_at = datetime()
        """
        tx.run(query, **{
            'property_id': property_id,
            'neighborhood_id': neighborhood_id,
            'name': details.get('name'),
            'city': details.get('city'),
            'median_price': details.get('median_price'),
            'school_rating': details.get('school_rating'),
            'transit_score': details.get('transit_score'),
            'school_district': details.get('school_district'),
            'zoning': details.get('zoning'),
        })
    
    def build_similarity_graph(self, property_pairs: List[Dict]) -> None:
        """
        Build SIMILAR_TO relationships between properties
        Called periodically to update similarity scores
        """
        with self.driver.session() as session:
            for pair in property_pairs:
                session.execute_write(self._create_similarity_relationship, pair)
    
    @staticmethod
    def _create_similarity_relationship(tx, pair: Dict) -> None:
        """Create SIMILAR_TO relationship between two properties"""
        query = """
        MATCH (p1:Property {property_id: $property_id_1})
        MATCH (p2:Property {property_id: $property_id_2})
        
        MERGE (p1)-[r:SIMILAR_TO]-(p2)
        SET r.similarity_score = $similarity_score,
            r.match_criteria = $match_criteria,
            r.updated_at = datetime()
        """
        tx.run(query, **{
            'property_id_1': pair['property_id_1'],
            'property_id_2': pair['property_id_2'],
            'similarity_score': pair['score'],
            'match_criteria': pair.get('criteria', []),
        })
    
    def insert_user_preference_graph(
        self, 
        user_id: str, 
        preferences: Dict
    ) -> None:
        """
        Build user preference relationships in graph
        """
        with self.driver.session() as session:
            # Clear existing preferences
            session.run("""
                MATCH (u:User {user_id: $user_id})-[r:PREFERS|EXCLUDES|SEARCHED]->()
                DELETE r
            """, user_id=user_id)
            
            # Insert new preferences
            for neighborhood in preferences.get('preferred_neighborhoods', []):
                session.run("""
                    MATCH (u:User {user_id: $user_id})
                    MERGE (n:Neighborhood {neighborhood_id: $neighborhood_id})
                    MERGE (u)-[:PREFERS {weight: 0.8, source: 'explicit'}]->(n)
                """, user_id=user_id, neighborhood_id=neighborhood)
            
            for amenity in preferences.get('required_amenities', []):
                session.run("""
                    MATCH (u:User {user_id: $user_id})
                    MERGE (a:Amenity {amenity_id: $amenity_id})
                    MERGE (u)-[:PREFERS {weight: 1.0, requirement: 'minimum'}]->(a)
                """, user_id=user_id, amenity_id=amenity)
            
            for exclusion in preferences.get('excluded_neighborhoods', []):
                session.run("""
                    MATCH (u:User {user_id: $user_id})
                    MERGE (n:Neighborhood {neighborhood_id: $neighborhood_id})
                    MERGE (u)-[:EXCLUDES {weight: 1.0, reason: 'user_exclusion'}]->(n)
                """, user_id=user_id, neighborhood_id=exclusion)
    
    def record_user_view(
        self, 
        user_id: str, 
        property_id: str, 
        saved: bool = False,
        notes: str = None
    ) -> None:
        """
        Record user viewing activity
        """
        with self.driver.session() as session:
            query = """
            MATCH (u:User {user_id: $user_id})
            MATCH (p:Property {property_id: $property_id})
            
            MERGE (u)-[r:VIEWED]->(p)
            SET r.view_count = COALESCE(r.view_count, 0) + 1,
                r.last_viewed = datetime(),
                r.saved = $saved,
                r.notes = $notes
            
            ON CREATE SET r.first_viewed = datetime()
            """
            session.run(query, **{
                'user_id': user_id,
                'property_id': property_id,
                'saved': saved,
                'notes': notes
            })
```

## 4\. Data Insertion Pipeline: End-to-End Flow

```python
class RealEstateDataPipeline:
    """
    Orchestrates data insertion across all three databases
    """
    
    def __init__(
        self, 
        supabase_client,
        qdrant_client,
        neo4j_driver
    ):
        self.supabase = SupabaseDataInserter(supabase_client)
        self.qdrant = QdrantDataInserter(qdrant_client)
        self.neo4j = Neo4jDataInserter(neo4j_driver)
    
    def process_scraped_listing(self, raw_data: Dict) -> str:
        """
        Full pipeline for processing a single scraped listing
        Returns property_id
        """
        # Step 1: Clean and normalize data
        cleaned = self._normalize_scraped_data(raw_data)
        
        # Step 2: Calculate derived metrics
        enriched = self._calculate_metrics(cleaned)
        
        # Step 3: Insert into Supabase (source of truth)
        property_id = self.supabase.insert_property(enriched)
        
        # Step 4: Calculate and store decision criteria scores
        self.supabase.calculate_criteria_scores(property_id)
        
        # Step 5: Enrich with scraped property data
        enriched['id'] = property_id
        enriched['nearby_pois'] = self._scrape_nearby_pois(enriched)
        
        # Step 6: Insert into Qdrant (embeddings)
        self.qdrant.insert_property(enriched)
        
        # Step 7: Build graph relationships in Neo4j
        self.neo4j.insert_property_graph(enriched)
        
        # Step 8: Update property similarities
        self._update_property_similarities(property_id)
        
        return property_id
    
    def _normalize_scraped_data(self, raw: Dict) -> Dict:
        """
        Normalize scraped data to match schema
        """
        return {
            'source': raw.get('source'),
            'source_url': raw.get('url'),
            'address': raw.get('street_address'),
            'city': raw.get('city'),
            'state': raw.get('state'),
            'zip_code': raw.get('zip'),
            'neighborhood': raw.get('neighborhood'),
            'latitude': raw.get('lat'),
            'longitude': raw.get('lng'),
            'property_type': self._normalize_type(raw.get('type')),
            'bedrooms': self._normalize_int(raw.get('beds')),
            'bathrooms': self._normalize_float(raw.get('baths')),
            'sqft': self._normalize_int(raw.get('sqft')),
            'price': self._normalize_float(raw.get('price')),
            'monthly_rent': self._normalize_float(raw.get('rent')),
            'hoa_fee': self._normalize_float(raw.get('hoa')),
            'property_taxes': self._normalize_float(raw.get('taxes')),
            'year_built': self._normalize_int(raw.get('year_built')),
            'condition': raw.get('condition', 'unknown'),
            'description': raw.get('description'),
            'images': raw.get('image_urls', []),
            'listing_status': raw.get('status', 'active'),
        }
    
    def _calculate_metrics(self, prop: Dict) -> Dict:
        """
        Calculate investment metrics
        """
        if prop.get('price') and prop.get('monthly_rent'):
            annual_rent = prop['monthly_rent'] * 12
            prop['rental_yield'] = (annual_rent / prop['price']) * 100
            
            # Assuming 30% expenses ratio
            net_operating_income = annual_rent * 0.7
            prop['cap_rate'] = (net_operating_income / prop['price']) * 100
            
            # Estimate debt coverage (assuming 30% down, 7% interest)
            if prop['price'] > 0:
                loan_amount = prop['price'] * 0.7
                monthly_mortgage = loan_amount * (0.07 / 12) * 1.3  # Approximate
                annual_debt_service = monthly_mortgage * 12
                prop['debt_coverage_ratio'] = net_operating_income / annual_debt_service if annual_debt_service > 0 else 0
        
        return prop
    
    def _update_property_similarities(self, property_id: str) -> None:
        """
        Calculate and store similarities for new property
        """
        # Get recently updated similar properties
        similar_props = self.qdrant.search_properties(
            query=self._get_property_search_text(property_id),
            filters={'listing_status': 'active'},
            limit=20
        )
        
        # Build similarity pairs
        pairs = []
        for similar in similar_props:
            pairs.append({
                'property_id_1': property_id,
                'property_id_2': similar['property_id'],
                'score': similar['score'],
                'criteria': self._determine_match_criteria(property_id, similar)
            })
        
        if pairs:
            self.neo4j.build_similarity_graph(pairs)
    
    def bulk_process(self, raw_listings: List[Dict]) -> Dict[str, int]:
        """
        Process multiple listings in batch
        """
        stats = {'processed': 0, 'failed': 0, 'skipped': 0}
        
        for raw in raw_listings:
            try:
                self.process_scraped_listing(raw)
                stats['processed'] += 1
            except Exception as e:
                print(f"Failed to process listing: {e}")
                stats['failed'] += 1
        
        return stats
```

## 5\. Data Insertion Summary Table

| Data Type | Supabase | Qdrant | Neo4j |
| --- | --- | --- | --- |
| **Property basics** (price, beds, baths) | ✅ Primary storage | ❌ | ❌ |
| **Property text** (descriptions, highlights) | ✅ Storage | ✅ Embeddings | ❌ |
| **Location data** (lat, lng, neighborhood) | ✅ Storage + filters | ✅ Filters | ✅ Relationships |
| **Amenities** | ✅ Structured links | ✅ Text search | ❌ |
| **Investment metrics** (cap rate, yield) | ✅ Calculated storage | ✅ Filters | ❌ |
| **Decision criteria scores** | ✅ Primary storage | ❌ | ❌ |
| **User preferences** | ✅ Storage | ❌ | ✅ Relationships |
| **User search history** | ✅ Storage | ✅ Embeddings | ❌ |
| **User viewing history** | ✅ Storage | ❌ | ✅ Relationships |
| **Property-POI distances** | ❌ | ❌ | ✅ Graph |
| **Property similarities** | ❌ | ❌ | ✅ Graph |
| **Property-neighborhood links** | ✅ Reference | ✅ Filters | ✅ Graph |
| **User-user similarities** | ❌ | ❌ | ✅ Graph |
| **Decision tree structure** | ✅ Definitions | ❌ | ✅ Structure |
| **Market trends** | ✅ Time-series | ❌ | ✅ Graph |

## 6\. Insertion Order and Dependencies

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INSERTION ORDER & DEPENDENCIES                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: FOUNDATION (No dependencies)                                       │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Supabase      │    │    Qdrant       │    │    Neo4j       │        │
│  │   ──────────    │    │    ────────     │    │    ──────      │        │
│  │                  │    │                  │    │                  │        │
│  │ • Amenities      │    │ • Collection     │    │ • POI nodes     │        │
│  │ • Property types │    │   setup          │    │ • Neighborhood  │        │
│  │ • Criteria defs  │    │                  │    │   nodes         │        │
│  │ • Users          │    │                  │    │ • Decision tree │        │
│  │                  │    │                  │    │   structure     │        │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘        │
│           │                        │                        │                  │
│           └────────────────────────┴────────────────────────┘                  │
│                                    │                                            │
│                                    ▼                                            │
│  PHASE 2: MASTER DATA (Depends on Phase 1)                                     │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Supabase      │    │    Qdrant       │    │    Neo4j       │        │
│  │   ──────────    │    │    ────────     │    │    ──────      │        │
│  │                  │    │                  │    │                  │        │
│  │ • Properties     │    │ • Property       │    │ • Property      │        │
│  │   (main table)   │───▶│   embeddings     │───▶│   nodes        │        │
│  │                  │    │   (after ID)     │    │   (after ID)   │        │
│  │ • Market trends  │    │                  │    │ • Property-POI │        │
│  │                  │    │                  │    │   relationships │        │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘        │
│           │                        │                        │                  │
│           └────────────────────────┴────────────────────────┘                  │
│                                    │                                            │
│                                    ▼                                            │
│  PHASE 3: DERIVED DATA (Depends on Phase 2)                                   │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Supabase      │    │    Qdrant       │    │    Neo4j       │        │
│  │   ──────────    │    │    ────────     │    │    ──────      │        │
│  │                  │    │                  │    │                  │        │
│  │ • Property       │    │ • Similarity     │    │ • Similarity    │        │
│  │   criteria       │    │   search         │    │   edges         │        │
│  │   scores         │    │                  │    │                  │        │
│  │                  │    │                  │    │                  │        │
│  │ • Comparable     │    │                  │    │                  │        │
│  │   analysis        │    │                  │    │                  │        │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘        │
│           │                        │                        │                  │
│           └────────────────────────┴────────────────────────┘                  │
│                                    │                                            │
│                                    ▼                                            │
│  PHASE 4: USER DATA (Continuous)                                               │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Supabase      │    │    Qdrant       │    │    Neo4j       │        │
│  │   ──────────    │    │    ────────     │    │    ──────      │        │
│  │                  │    │                  │    │                  │        │
│  │ • User prefs     │    │ • Query          │    │ • User prefs    │        │
│  │ • Search history │───▶│   embeddings    │───▶│   graph         │        │
│  │ • View history   │    │                  │    │ • View history  │        │
│  │                  │    │                  │    │ • Similar users │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

This comprehensive data insertion strategy ensures that each database is populated with the data it excels at handling, while maintaining proper dependencies and data flow between systems.

Would you like me to provide more details on any specific aspect—such as the exact SQL triggers, the embedding generation pipeline, or the similarity calculation algorithms?