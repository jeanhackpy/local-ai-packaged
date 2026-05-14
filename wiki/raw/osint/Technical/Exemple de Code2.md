### Exemple de Code

#### 1. **Exécution d'un Modèle LLM sur la Station Fixe**
```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)
model_name = "gpt2-medium"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

@app.route('/generate', methods=['POST'])
def generate_text():
    input_text = request.json.get('text')
    inputs = tokenizer.encode(input_text, return_tensors='pt')
    outputs = model.generate(inputs, max_length=200)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'generated_text': generated_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

#### 2. **Contrôle du Robot Mobile**
```python
import paho.mqtt.client as mqtt
from gpiozero import Robot, LED
import cv2
import pyttsx3

robot = Robot(left=(4, 14), right=(17, 18))
engine = pyttsx3.init()

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    if command == 'forward':
        robot.forward()
    elif command == 'backward':
        robot.backward()
    elif command == 'left':
        robot.left()
    elif command == 'right':
        robot.right()
    elif command == 'stop':
        robot.stop()
    elif command.startswith('speak:'):
        text = command.split('speak:')[1]
        engine.say(text)
        engine.runAndWait()

client = mqtt.Client()
client.on_message = on_message
client.connect('adresse_ip_de_la_station_fixe', 1883, 60)
client.subscribe('robot/control')
client.loop_forever()
```