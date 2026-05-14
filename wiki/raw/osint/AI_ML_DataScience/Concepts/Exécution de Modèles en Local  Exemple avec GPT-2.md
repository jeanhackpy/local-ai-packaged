### Exécution de Modèles en Local : Exemple avec GPT-2

Pour illustrer comment exécuter GPT-2 en local, voici un exemple de script :

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Charger le modèle et le tokenizer GPT-2
model_name = "gpt2-medium"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Préparer l'entrée
input_text = "Prends des notes sur le texte suivant : "
inputs = tokenizer.encode(input_text, return_tensors="pt")

# Générer du texte
outputs = model.generate(inputs, max_length=200, num_return_sequences=1)

# Décoder et afficher le texte généré
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
```