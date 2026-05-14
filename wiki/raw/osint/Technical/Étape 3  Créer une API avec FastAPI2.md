### Étape 3 : Créer une API avec FastAPI

1. **Créer un fichier `app.py`** :

   ```python
   from fastapi import FastAPI, Request
   from transformers import LlamaTokenizer, LlamaForCausalLM
   import torch

   app = FastAPI()

   # Charger le tokenizer et le modèle LLaMA
   model_name = "meta-llama/Llama-2-7b"  # Remplacez par le chemin de votre modèle
   tokenizer = LlamaTokenizer.from_pretrained(model_name)
   model = LlamaForCausalLM.from_pretrained(model_name)

   @app.post("/generate")
   async def generate_text(request: Request):
       data = await request.json()
       prompt = data['prompt']
       
       inputs = tokenizer(prompt, return_tensors="pt")
       outputs = model.generate(**inputs, max_length=150, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
       response = tokenizer.decode(outputs[0], skip_special_tokens=True)
       
       return {"response": response}

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

2. **Lancer l'API** :

   ```bash
   python app.py
   ```

   L'API sera disponible à l'adresse `http://localhost:8000/generate`.