### Exemple de Code

#### Dockerfile
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### main.py (Back-end)
```python
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")
text_analyzer = pipeline("sentiment-analysis")

@app.post("/chat")
async def chat(query: str):
    response = chatbot(query)
    return {"response": response}

@app.post("/analyze")
async def analyze(text: str):
    analysis = text_analyzer(text)
    return {"analysis": analysis}
```

#### index.html (Front-end)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-LLM Agent PoC</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h1>Multi-LLM Agent PoC</h1>
        <div class="form-group">
            <label for="chat-input">Chat Input:</label>
            <input type="text" class="form-control" id="chat-input">
            <button class="btn btn-primary mt-2" onclick="chat()">Send</button>
        </div>
        <div class="form-group">
            <label for="analyze-input">Text to Analyze:</label>
            <textarea class="form-control" id="analyze-input"></textarea>
            <button class="btn btn-primary mt-2" onclick="analyze()">Analyze</button>
        </div>
        <div id="response" class="mt-3"></div>
    </div>

    <script>
        async function chat() {
            const query = document.getElementById('chat-input').value;
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query }),
            });
            const data = await response.json();
            document.getElementById('response').innerText = data.response;
        }

        async function analyze() {
            const text = document.getElementById('analyze-input').value;
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
            });
            const data = await response.json();
            document.getElementById('response').innerText = data.analysis;
        }
    </script>
</body>
</html>
```