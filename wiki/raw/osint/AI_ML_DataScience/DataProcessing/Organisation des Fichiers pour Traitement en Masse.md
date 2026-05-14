### Organisation des Fichiers pour Traitement en Masse

Vous pouvez créer un dossier pour stocker vos fichiers PDF et EPUB, puis écrire un script Python pour parcourir ce dossier, extraire le texte de chaque fichier, et le sauvegarder pour un entraînement ultérieur.

**Exemple d'Organisation et Traitement en Masse** :
1. Créez un dossier nommé `documents` et placez-y vos fichiers EPUB et PDF.
2. Utilisez le script suivant pour extraire le texte de tous les fichiers dans ce dossier.

```python
import os

def extract_text_from_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            documents.append(extract_text_from_pdf(pdf_path))
        elif filename.endswith(".epub"):
            epub_path = os.path.join(folder_path, filename)
            documents.append(extract_text_from_epub(epub_path))
    return documents

# Change 'documents' to the path where your files are located
folder_path = "documents"
all_texts = extract_text_from_documents(folder_path)

# Example: Save extracted texts to a file
with open("extracted_texts.txt", "w", encoding="utf-8") as f:
    for text in all_texts:
        f.write(text + "\n---\n")

print("Text extraction complete.")
```