from machine import Pin, ADC
from micropython import const
import time
import json

#Sensor Types ---
SENSOR_ADC = const(0)
SENSOR_DIN = const(1)

####################### Base Sensor class ###########################
class Sensor:
    def __init__(self, name, pin_num, unit):
        self.pin     = None
        self.name    = name
        self.pin_num = pin_num
        self.unit    = unit

    def read(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_data(self):
        if self.pin == None:
            raise Exception("Pin not configured")
        return json.dumps({
            "name"      : self.name,
            "pin_num"   : self.pin_num,
            "value"     : float(self.read()),
            "unit"      : self.unit
        })

##################### Sensor Digital input class ####################
class Sensor_Din(Sensor):
    def __init__(self, name, pin_num, pu_pd, unit):
        super().__init__(name, pin_num, unit)
        self.pu_pd = pu_pd
        self.pin   = Pin(pin_num, Pin.IN, pu_pd)

    def read(self):
        val = self.pin.value()
        if self.pu_pd == Pin.PULL_UP:
            val = not val #Invert because using pull-up
        return val

##################### Sensor ADC input class ########################
class Sensor_Adc (Sensor):
    def __init__(self, name, pin_num, unit, adc_attn = ADC.ATTN_11DB, adc_res = ADC.WIDTH_12BIT, scaling = 1.0):
        super().__init__(name, pin_num, unit)
        self.pin = ADC(Pin(pin_num))
        self.pin.atten(adc_attn)
        self.pin.width(adc_res)
        self.scaling = scaling

    def read(self):
        return (self.pin.read() * self.scaling)
