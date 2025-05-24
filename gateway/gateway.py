import os
from dotenv import load_dotenv, dotenv_values
import socket
import json
from mqtt import MqttPublisher
import time

load_dotenv()
SERVER_IP     = "0.0.0.0"
SERVER_PORT   = int(os.getenv("SERVER_PORT_NUM"))
# Configuration
CLIENT_ID     = "python-publisher"
BROKER        = os.getenv("BROKER_NAME")
PORT          = int(os.getenv("PORT_NUM"))
TOPICS        = ["kousar_iot/gateway_0/esp32/esp32_0/pot", "kousar_iot/gateway_0/esp32/esp32_0/button"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print("Connecting to Mqtt....")

mqtt_pub = MqttPublisher(client_id = CLIENT_ID, broker = BROKER, topics = TOPICS, port = PORT)

print("Listening for connection...")

decoder = json.JSONDecoder()

while True:
    try:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        buffer = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("Client disconnected")
                break

            buffer += data.decode().strip()

            while buffer:
                try:
                    obj, idx = decoder.raw_decode(buffer)
                    buffer = buffer[idx:].lstrip()  
                    print(f"Parsed JSON: {obj}")

                    # Split into pot/button lists
                    ts = None
                    pot_entries = []
                    button_entries = []

                    for entry in obj:
                        if "ts" in entry:
                            ts = entry
                        elif "name" in entry:
                            if "pot" in entry["name"]:
                                pot_entries.append(entry)
                            elif "button" in entry["name"]:
                                button_entries.append(entry)

                    if ts:
                        if pot_entries:
                            pot_data = {
                                "ts" : ts, 
                                "sensor_value" : pot_entries
                            }
                            mqtt_pub.send_message(TOPICS[0], json.dumps(pot_data))
                        if button_entries:
                            button_data = {
                                "ts" : ts,
                                "sensor_value" : button_entries
                            }
                            mqtt_pub.send_message(TOPICS[1], json.dumps(button_data))
                        time.sleep(1)
                except json.JSONDecodeError:
                    break

    except KeyboardInterrupt:
        print("KeyboardInterrupt - shutting down.")
        mqtt_pub.stop()
        server_socket.close()
        break

    except Exception as e:
        print("Exception:", e)
