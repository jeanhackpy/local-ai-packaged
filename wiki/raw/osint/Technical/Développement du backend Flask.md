### Développement du backend Flask

Créez un fichier `app.py` avec la structure suivante :

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configurations (API Keys, etc.)
CREW_AI_API_KEY = 'votre_crew_ai_api_key'
MISTRAL_7B_API_KEY = 'votre_mistral_7b_api_key'
CREW_AI_URL = 'https://api.crew.ai/v1/predict'
MISTRAL_7B_URL = 'https://api.mistral.ai/v1/generate'

# Fonction pour appeler Crew AI
def call_crew_ai(role, input_text):
    headers = {
        'Authorization': f'Bearer {CREW_AI_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'role': role,
        'input': input_text
    }
    response = requests.post(CREW_AI_URL, headers=headers, json=payload)
    return response.json()

# Fonction pour appeler Mistral 7B
def call_mistral_7b(input_text):
    headers = {
        'Authorization': f'Bearer {MISTRAL_7B_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': input_text
    }
    response = requests.post(MISTRAL_7B_URL, headers=headers, json=payload)
    return response.json()

@app.route('/predict/<role>', methods=['POST'])
def predict(role):
    data = request.get_json()
    input_text = data.get('input')

    # Appeler Crew AI pour le rôle spécifique
    crew_ai_response = call_crew_ai(role, input_text)
    crew_ai_output = crew_ai_response.get('output')

    # Appeler Mistral 7B
    mistral_7b_response = call_mistral_7b(crew_ai_output)
    mistral_7b_output = mistral_7b_response.get('text')

    return jsonify({
        'crew_ai_output': crew_ai_output,
        'mistral_7b_output': mistral_7b_output
    })

if __name__ == '__main__':
    app.run(debug=True)
```