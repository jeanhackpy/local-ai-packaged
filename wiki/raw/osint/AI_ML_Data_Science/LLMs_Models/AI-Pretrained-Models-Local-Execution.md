---
tags: [ai, nlp, pre-trained-models, local-execution, gpt-2, python, tutorial, development]
---

### 1. Utiliser des Modèles Pré-Entraînés en Local
Des modèles de traitement du langage naturel (NLP) peuvent être téléchargés et utilisés localement sans coûts récurrents.

#### a. GPT-2 en Local
GPT-2 est un modèle puissant et disponible gratuitement que vous pouvez exécuter localement. Vous pouvez utiliser des bibliothèques comme `transformers` de Hugging Face.

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_note_from_text(text):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    inputs = tokenizer.encode("Prends des notes sur le texte suivant : " + text, return_tensors='pt')
    outputs = model.generate(inputs, max_length=500, num_return_sequences=1)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

text = "Votre texte ici"
note = generate_note_from_text(text)

obsidian_path = "chemin/vers/votre/dossier/Obsidian"
note_path = os.path.join(obsidian_path, "note.md")

with open(note_path, "w", encoding="utf-8") as file:
    file.write(note)

print(f"Note sauvegardée à {note_path}")
```