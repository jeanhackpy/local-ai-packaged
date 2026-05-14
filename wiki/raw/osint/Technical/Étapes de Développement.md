### Étapes de développement

#### 1. Configuration de l'environnement
Assurez-vous d'avoir installé Flask et les bibliothèques nécessaires.

```bash
pip install flask requests
```

#### 2. Développement du backend Flask

Créez un fichier `app.py` :

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
def call_crew_ai(input_text):
    headers = {
        'Authorization': f'Bearer {CREW_AI_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
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

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data.get('input')

    # Appeler Crew AI
    crew_ai_response = call_crew_ai(input_text)
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

#### 3. Développement de l'interface utilisateur

Vous pouvez utiliser HTML et JavaScript pour créer une interface simple qui envoie des requêtes à votre backend Flask.

Créez un fichier `index.html` :

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI App</title>
</head>
<body>
    <h1>AI App using Crew AI and Mistral 7B</h1>
    <textarea id="inputText" rows="4" cols="50" placeholder="Enter your text here..."></textarea><br>
    <button onclick="sendRequest()">Submit</button>
    <h2>Output:</h2>
    <p id="output"></p>

    <script>
        function sendRequest() {
            const inputText = document.getElementById('inputText').value;

            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ input: inputText })
            })
            .then(response => response.json())
            .then(data => {
                const output = `Crew AI Output: ${data.crew_ai_output}<br>Mistral 7B Output: ${data.mistral_7b_output}`;
                document.getElementById('output').innerHTML = output;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
</body>
</html>
```

#### 4. Lancer l'application

Exécutez votre application Flask :

```bash
python app.py
```

Ensuite, ouvrez `index.html` dans votre navigateur pour accéder à l'interface utilisateur.