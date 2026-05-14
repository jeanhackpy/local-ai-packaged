---
tags: [ai, llm, openai, gpt-4, api, python]
---
### Accès à l'API GPT-4 d'OpenAI
Configurer l'accès à l'API GPT-4 pour traiter les requêtes en langage naturel.
```python
import openai

openai.api_key = 'YOUR_API_KEY'

def query_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
```