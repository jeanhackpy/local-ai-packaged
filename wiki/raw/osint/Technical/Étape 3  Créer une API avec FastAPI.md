### Étape 3 : Créer une API avec FastAPI

1. **Créer un fichier `app.py`** :

   ```python
   from fastapi import FastAPI, Request
   from mixral import MixralModel  # Assurez-vous d'importer correctement votre modèle Mixral

   app = FastAPI()

   # Charger le modèle Mixral
   model = MixralModel.load("path/to/your/mixral/model")

   @app.post("/generate")
   async def generate_text(request: Request):
       data = await request.json()
       prompt = data['prompt']
       
       response = model.generate(prompt)
       
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