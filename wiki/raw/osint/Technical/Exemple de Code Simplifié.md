### Exemple de Code Simplifié

Voici un exemple simplifié de code Python pour générer du contenu en utilisant OpenAI GPT-4 :

```python
import openai

# Configuration de l'API OpenAI
openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_content(topic, keywords, length='medium'):
    prompt = f"Write a {length} article about {topic} including these keywords: {', '.join(keywords)}. The content should be optimized for SEO."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500  # Ajustez selon la longueur souhaitée
    )
    
    return response.choices[0].text.strip()

# Exemple d'utilisation
topic = "Les avantages du marketing digital pour les PME"
keywords = ["marketing digital", "PME", "SEO", "réseaux sociaux"]

content = generate_content(topic, keywords)
print(content)
```