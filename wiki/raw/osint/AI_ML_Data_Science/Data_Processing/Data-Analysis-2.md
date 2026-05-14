---
tags: [ai, data-analysis, nlp, huggingface, gpt-3]
---
### Analyse des Données

Nous utilisons le modèle GPT-3 via l'API Hugging Face pour analyser et résumer les articles.

#### b. Configuration de l'API Hugging Face

```python
from transformers import pipeline

def analyze_news_articles(news):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn")
    summaries = []
    for article in news:
        summary = summarizer(article['title'] + ". " + article['link'], max_length=150, min_length=50, do_sample=False)
        summaries.append({
            "title": article['title'],
            "summary": summary[0]['summary_text'],
            "link": article['link']
        })
    return summaries
```