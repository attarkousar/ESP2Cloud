from mqtt import MqttSubscriber
import time

topics = ["esp32/pot", "esp32/button"]
mqtt_sub = MqttSubscriber(broker="broker.hivemq.com", topics=topics)
while True:
    data = mqtt_sub.get_data("esp32/pot")

    time.sleep(1)

    #create API to interact with front end
    # convert data into json and plot graph