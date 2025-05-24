import os
from dotenv import load_dotenv, dotenv_values
import paho.mqtt.client as mqtt
from threading import Lock

TOPICS = ["kousar_iot/gateway_0/esp32/esp32_0/pot", "kousar_iot/gateway_0/esp32/esp32_0/button"]
load_dotenv()
# Certificate paths
ca_cert  = os.getenv("CA_CERT")
certfile = os.getenv("CERT_FILE")
keyfile  = os.getenv("KEY_FILE")

class MqttSubscriber:
    def __init__(self, broker, topics, port=1883, client_id=""):
        self.broker    = broker
        self.port      = port
        self.topics    = topics if isinstance(topics, list) else [topics]
        self.client    = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)
        self.datalist1 = []
        self.datalist2 = []
        self.lock      = Lock()
        # Attach callbacks
        self.client.tls_set(ca_certs=ca_cert, certfile=certfile, keyfile=keyfile)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # Connect and start listening
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, reasonCode, properties):
        print(f"Connected to broker at {self.broker}:{self.port}")
        for topic in self.topics:
            print(f"Subscribing to topic: {topic}")
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        with self.lock:
            if msg.topic == TOPICS[0]:
                data1 = ((msg.topic,msg.payload.decode()))
                if len(self.datalist1) >= 10: 
                    self.datalist1.pop(0)
                self.datalist1.append(data1)
            elif msg.topic == TOPICS[1]:
                data2 = ((msg.topic,msg.payload.decode()))
                if len(self.datalist2) >= 10: 
                    self.datalist2.pop(0)
                self.datalist2.append(data2)


    def get_data(self,topic):
        with self.lock:
            if topic == TOPICS[0]:
                if len(self.datalist1) == 0:
                    return None,None
                return self.datalist1.pop(0)
            elif topic == TOPICS[1]:
                if len(self.datalist2) == 0:
                    return None,None
                return self.datalist2.pop(0)       

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("MQTT subscriber disconnected")


