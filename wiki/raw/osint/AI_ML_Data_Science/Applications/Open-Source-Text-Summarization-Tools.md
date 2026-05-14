---
tags: [ai, nlp, text-summarization, open-source, python]
---
### Utiliser des Outils de Synthèse de Texte Open-Source
Vous pouvez utiliser des outils open-source pour extraire et résumer des textes.

#### a. Sumy
Sumy est un outil de résumés de texte qui supporte plusieurs algorithmes de résumé.

```python
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 5)  # Nombre de phrases de résumé
    return " ".join([str(sentence) for sentence in summary])

text = "Votre texte ici"
summary = summarize_text(text)

obsidian_path = "chemin/vers/votre/dossier/Obsidian"
note_path = os.path.join(obsidian_path, "note.md")

with open(note_path, "w", encoding="utf-8") as file:
    file.write(summary)

print(f"Résumé sauvegardé à {note_path}")
```