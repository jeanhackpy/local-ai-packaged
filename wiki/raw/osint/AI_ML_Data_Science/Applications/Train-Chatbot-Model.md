---
tags: [ai, chatbot, training, huggingface, python, nlp]
---
### Entraîner un modèle de chatbot

Pour entraîner le chatbot, nous allons utiliser `transformers` de Hugging Face, une bibliothèque populaire pour les modèles de langage.

Voici un script Python complet qui réalise toutes ces étapes :

```python
import fitz  # PyMuPDF
import pandas as pd
import os
from transformers import pipeline, Trainer, TrainingArguments, GPT2Tokenizer, GPT2LMHeadModel
from datasets import Dataset

# Fonction pour extraire le texte des fichiers PDF
def extract_text_from_pdfs(pdf_folder):
    texts = []
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            file_path = os.path.join(pdf_folder, pdf_file)
            doc = fitz.open(file_path)
            text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            texts.append(text)
    return texts

# Fonction pour combiner les données des fichiers PDF et CSV
def combine_data(pdf_texts, csv_folder):
    data = []
    for text in pdf_texts:
        data.append({"text": text, "source": "pdf"})

    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('.csv'):
            file_path = os.path.join(csv_folder, csv_file)
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                data.append({"text": row.to_string(), "source": "csv"})
    
    return data

# Extraction des textes des PDF
pdf_folder = "path/to/pdf/folder"
pdf_texts = extract_text_from_pdfs(pdf_folder)

# Combinaison des données
csv_folder = "path/to/csv/folder"
data = combine_data(pdf_texts, csv_folder)

# Préparation des données pour l'entraînement
df = pd.DataFrame(data)
dataset = Dataset.from_pandas(df)

# Tokenizer et modèle
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Pré-traitement des données
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Arguments d'entraînement
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Entraînement du modèle
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
)

trainer.train()

# Sauvegarde du modèle
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")
```