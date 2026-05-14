### Soumission du Texte à un LLM pour Entraînement

Une fois le texte extrait, vous pouvez l'utiliser pour entraîner un modèle de langage (LLM). Pour ce faire, il vous faudra un framework de formation de modèles comme TensorFlow, PyTorch, ou des outils plus spécialisés comme Hugging Face's `transformers` et `datasets`.

**Exemple avec Hugging Face Transformers** :
```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset

# Charger le tokenizer et le modèle
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Créer un dataset
def load_dataset(file_path, tokenizer, block_size=128):
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    tokenized_text = tokenizer.encode(text)
    examples = [tokenized_text[i:i+block_size] for i in range(0, len(tokenized_text)-block_size+1, block_size)]
    inputs = [torch.tensor(e) for e in examples]
    return TextDataset(inputs)

dataset = load_dataset("extracted_texts.txt", tokenizer)

# Configurer l'entraînement
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=1,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()
```