import _thread
import machine
import time
import sys

from micropython  import const
from input_reader import InputReader
from wifi_client  import WifiClient, SSID, PASSWORD
from data_pusher  import DataPublisherSocket, PublisherQueue

TIMEOUT       = const(20000)
SAMPLING_RATE = const(1)

def push_thread_func(data_queue):
    wdt_push       = machine.WDT(timeout=TIMEOUT)
    data_publisher = DataPublisherSocket()

    while True:
        with data_queue.lock:
            queued_sensor_data = data_queue.get_q_data()
        if queued_sensor_data:
            data_publisher.send_data(queued_sensor_data)
            wdt_push.feed()
            time.sleep(0.05)

def input_thread_func(data_queue):
    input_reader = InputReader()
    wdt_ip       = machine.WDT(timeout=TIMEOUT)

    while True:
        all_sensor_data = input_reader.get_all_sensor_data()
        if all_sensor_data:
            with data_queue.lock:
                data_queue.add_q_data(all_sensor_data)
        wdt_ip.feed()
        time.sleep(0.05)

def main():
    lock = _thread.allocate_lock()
    data_queue = PublisherQueue(lock)
    _thread.start_new_thread(input_thread_func, (data_queue,)) # Starts input_thread_func() in parallel for each new client.
    push_thread_func(data_queue)


if __name__ == '__main__' :
    print("Starting Main")
    wifi_client = WifiClient(ssid=SSID, password=PASSWORD)
    wifi_client.connect_wifi()
    main()
