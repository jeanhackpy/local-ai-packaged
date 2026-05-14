### Développement de l'interface utilisateur

Créez un fichier `index.html` pour l'interface utilisateur :

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
    <select id="role">
        <option value="data_searcher">Data Searcher</option>
        <option value="data_analysis">Data Analysis</option>
        <option value="investor_advisor">Investor Advisor</option>
        <option value="travel_agent">Travel Agent</option>
        <option value="lawyer_advisor">Lawyer Advisor</option>
        <option value="airbnb_specialist">Airbnb Specialist</option>
    </select><br>
    <button onclick="sendRequest()">Submit</button>
    <h2>Output:</h2>
    <p id="output"></p>

    <script>
        function sendRequest() {
            const inputText = document.getElementById('inputText').value;
            const role = document.getElementById('role').value;

            fetch(`/predict/${role}`, {
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