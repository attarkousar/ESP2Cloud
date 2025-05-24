from machine import Pin, ADC
import time
import json
import sensor
import ntptime

#--- Input Setup Example for ESP32 ---
_EXAMPLE_INPUTS_ESP32 = {
    # --- Digital Input Setup ---
    "button1": sensor.Sensor_Din(name = "button1", pin_num = 12, pu_pd = Pin.PULL_UP, unit = "bool"),
    "button2": sensor.Sensor_Din(name = "button2", pin_num = 14, pu_pd = Pin.PULL_UP, unit = "bool"),

    # --- ADC Input Setup ---
    "adc1": sensor.Sensor_Adc(name = "pot1", pin_num = 32, unit = "V", scaling = (3.3 / 4095)),
    "adc2": sensor.Sensor_Adc(name = "pot2", pin_num = 33, unit = "V", scaling = (3.3 / 4095)),
}

class InputReader:
    def __init__(self, inputs = None):
        self.data_list = []
        self.inputs = inputs 
        self.last_ts = None
        if self.inputs == None:
            self.inputs = _EXAMPLE_INPUTS_ESP32
        ntptime.settime()

    def get_all_sensor_data(self):
        local_time = time.localtime()
        if self.last_ts == local_time:
            #duplicate
            return None
        self.last_ts = local_time
        self.data_list = [({"ts": local_time})]

        for _, sensors in self.inputs.items():
            self.data_list.append(
                json.loads(sensors.get_data())
            )
        return json.dumps(self.data_list) #return all data as json obj

    def print_me(self):
        print("Hello from input reader")
