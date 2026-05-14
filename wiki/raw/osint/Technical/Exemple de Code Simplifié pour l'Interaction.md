### Exemple de Code Simplifié pour l'Interaction
```python
# Example of using Flask for RESTful API in Python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Agent 1 API Endpoint
@app.route('/analyze_market', methods=['POST'])
def analyze_market():
    data = request.json
    # Process data and perform market analysis
    result = perform_market_analysis(data)
    return jsonify(result)

# Agent 2 API Endpoint
@app.route('/financial_forecast', methods=['POST'])
def financial_forecast():
    data = request.json
    # Process data and perform financial forecasting
    result = perform_financial_forecasting(data)
    return jsonify(result)

# Starting the Flask application
if __name__ == '__main__':
    app.run(debug=True)

# Example of using RabbitMQ for message passing in Python
import pika

# Setting up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='market_analysis')

# Publish a message
channel.basic_publish(exchange='', routing_key='market_analysis', body='New market data')

# Close the connection
connection.close()

# Consume messages
def callback(ch, method, properties, body):
    print(f"Received {body}")

channel.basic_consume(queue='market_analysis', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```