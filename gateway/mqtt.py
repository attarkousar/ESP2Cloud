import os
from dotenv import load_dotenv, dotenv_values
import paho.mqtt.client as mqtt
import time

load_dotenv()
# Certificate paths
ca_cert  = os.getenv("CA_CERT")
certfile = os.getenv("CERT_FILE")
keyfile  = os.getenv("KEY_FILE")

class MqttPublisher:
    def __init__(self, broker, topics, port = 1883, client_id = ""):
        self.broker = broker
        self.port   = port
        self.topics = topics if isinstance(topics, list) else [topics]
        self.client = mqtt.Client(client_id = client_id, protocol = mqtt.MQTTv5)
        self.client.tls_set(ca_certs = ca_cert, certfile = certfile, keyfile = keyfile)
        # Attach callbacks
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

        # Connect to broker
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, reasonCode, properties):
        print(f"Connected to broker at {self.broker}:{self.port}")

    def on_publish(self, client, userdata, mid):
        print(f"Message published (mid={mid})")

    def send_message(self, topic, message):
        if topic in self.topics:
            result = self.client.publish(topic, message, qos = 1)
            status = result.rc # Returns zero if successful
            if status != mqtt.MQTT_ERR_SUCCESS:
                print(f"Failed to send message. Error code: {status}")
        else:
            print(f"Topic '{topic}' not in allowed topics list.")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("MQTT client disconnected")


