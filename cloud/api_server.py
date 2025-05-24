import os
from dotenv import load_dotenv, dotenv_values
from flask import Flask, jsonify, render_template
from mqtt import MqttSubscriber  
import atexit
from flask_cors import CORS

load_dotenv()
BROKER = os.getenv("BROKER_NAME")
PORT = int(os.getenv("PORT_NUM"))
TOPICS = ["kousar_iot/gateway_0/esp32/esp32_0/pot", "kousar_iot/gateway_0/esp32/esp32_0/button"]

app = Flask(__name__)
CORS(app)

subscriber = MqttSubscriber(broker= BROKER, topics=TOPICS, port=PORT)  

@app.route('/get-data/pot')
def get_data_pot():
    topic, message = subscriber.get_data(TOPICS[0])
    if message is None:
        return jsonify({"status": "no_data", "message": "No MQTT messages received yet."})
    return jsonify({"status": "success", "topic": topic, "message": message})

@app.route('/get-data/button')
def get_data_button():
    topic, message = subscriber.get_data(TOPICS[1])
    if message is None:
        return jsonify({"status": "no_data", "message": "No MQTT messages received yet."})
    return jsonify({"status": "success", "topic": topic, "message": message})
 
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/')
def index():
    return "MQTT Flask Server is Running"


atexit.register(subscriber.stop)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
    
