import os
from dotenv import load_dotenv, dotenv_values
import network
import time

load_dotenv()
#--- Wifi Configuration ---
SSID        = os.getenv("MY_WIFI_SSID") #My Wifi Name, change according to which wifi you connect to
PASSWORD    = os.getenv("MY_WIFI_PASSWORD") #My Wifi password, change according to which wifi you connect to
#--- Wifi Configuration ---


# --- Wifi Client to connect to WiFI ---
class WifiClient:
    def __init__(self, ssid, password):
        self.wlan = network.WLAN(network.STA_IF)
        self.ssid = ssid
        self.password = password

    def connect_wifi(self):
        #force restart connection to wifi
        #self.wlan.active(False)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print("Connecting to Wifi...")
            self.wlan.connect(self.ssid, self.password)
            while not self.wlan.isconnected():
                time.sleep(1)
                print("WiFi not connected yet ..")
        print ("Wifi connected. IP: " , self.wlan.ifconfig()[0])
