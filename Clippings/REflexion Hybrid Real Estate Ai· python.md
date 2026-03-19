---
title: ChatGPT
source: https://chatgpt.com/c/6839d0c2-fce0-8003-a4ea-b775d1e8693b
author:
  - "[[REflexion Hybrid Real Estate Ai· python]]"
published:
created: 2026-03-19
description: ChatGPT is your AI chatbot for everyday use. Chat with the most advanced AI to explore ideas, solve problems, and learn faster.
tags:
  - clippings
---
Hybrid Real Estate Ai· python

\# 📦 Hybrid Real Estate Search System

\# Combines PostgreSQL (structured) + Qdrant (semantic) search with LLM orchestration

  

\# ---- Requirements ----

\# - LangChain

\# - Qdrant Client

\# - SQLAlchemy (or Supabase Python client)

\# - OpenAI or HuggingFace LLM API

\# - Pandas, Psycopg2

  

import pandas as pd

from qdrant\_client import QdrantClient

from qdrant\_client.http import models as qdrant\_models

from sqlalchemy import create\_engine, text

from langchain.llms import OpenAI

from langchain.chains import RetrievalQA

from langchain.embeddings import OpenAIEmbeddings

import openai

  

\# ---- 1. Load and prepare CSV ----

df = pd.read\_csv("real\_estate\_data.csv")

  

\# Sample fusion of columns for semantic vectorization

def build\_semantic\_description(row):

return f"{row\['type'\]} of {row\['area'\]}m2 in {row\['location'\]} with {row\['bedrooms'\]} bedrooms, {row\['bathrooms'\]} baths, priced at {row\['price'\]} THB. {row\['description'\]}"

  

df\["semantic\_text"\] = df.apply(build\_semantic\_description, axis=1)

  

\# ---- 2. Push to PostgreSQL (Supabase compatible) ----

postgres\_uri = "postgresql+psycopg2://user:password@host:port/dbname"

engine = create\_engine(postgres\_uri)

df.to\_sql("properties", engine, if\_exists="replace", index=False)

  

\# ---- 3. Vectorize and push to Qdrant ----

qdrant = QdrantClient(host="localhost", port=6333)

  

\# Create collection (if not exists)

qdrant.recreate\_collection(

collection\_name="real\_estate",

vectors\_config=qdrant\_models.VectorParams(size=1536, distance=qdrant\_models.Distance.COSINE)

)

  

\# Generate embeddings (OpenAI)

openai.api\_key = "sk-..."

embedding\_model = OpenAIEmbeddings()

  

vectors = embedding\_model.embed\_documents(df\["semantic\_text"\].tolist())

  

qdrant.upsert(

collection\_name="real\_estate",

points=\[

qdrant\_models.PointStruct(id=i, vector=vectors\[i\], payload=df.iloc\[i\].to\_dict())

for i in range(len(df))

\]

)

  

\# ---- 4. Hybrid Agent Logic ----

def is\_structured\_query(user\_input):

\# Simple rule-based detector (can be replaced with classifier)

keywords = \["moins de", "plus de", "THB", "m2", "chambres", "salle"\]

return any(k in user\_input.lower() for k in keywords)

  

\# ---- 5. Query PostgreSQL or Qdrant ----

def search\_properties(user\_input):

if is\_structured\_query(user\_input):

\# Text-to-SQL logic (mocked example)

sql\_query = "SELECT \* FROM properties WHERE price < 5000000 AND bedrooms >= 2"

with engine.connect() as conn:

result = conn.execute(text(sql\_query)).fetchall()

return \[dict(row) for row in result\]

else:

\# Vector search in Qdrant

query\_vector = embedding\_model.embed\_query(user\_input)

hits = qdrant.search(

collection\_name="real\_estate",

query\_vector=query\_vector,

limit=5

)

return \[hit.payload for hit in hits\]

  

\# ---- 6. Run Example ----

if \_\_name\_\_ == "\_\_main\_\_":

query = "Villa balinaise avec piscine, vibes zen proche nature, moins de 10M THB"

results = search\_properties(query)

for r in results: