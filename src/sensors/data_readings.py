from typing import List
from threading import Thread

from src.sensors import SENSORS_LIST, AbstractSensor

if __name__ == '__main__':
    sensors: List[AbstractSensor] = [s() for s in SENSORS_LIST]
    threads: List[Thread] = []
    for sensor in sensors:
        sensor_thread: Thread = Thread(target=sensor.sensor_loop)
        threads.append(sensor_thread)

    for sensor_thread in threads:
        sensor_thread.start()
