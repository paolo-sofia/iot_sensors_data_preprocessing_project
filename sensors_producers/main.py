import logging
from threading import Thread
from typing import List

from kafka3 import KafkaConsumer

from sensors_producers.sensors import SENSORS_LIST
from sensors_producers.sensors.abstract_sensor import AbstractSensor

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def readings_spark():
    consumer: KafkaConsumer = KafkaConsumer('output', bootstrap_servers='broker:9092',
                                            auto_offset_reset='earliest', group_id='sensors',
                                            consumer_timeout_ms=100, api_version=(3, 4, 0))
    consumer.poll()
    for msg in consumer:
        logger.error(f"MSG {msg.value.decode('utf-8')}")


if __name__ == '__main__':
    sensors: List[AbstractSensor] = [s() for s in SENSORS_LIST]
    threads: List[Thread] = []
    for sensor in sensors:
        sensor_thread: Thread = Thread(target=sensor.sensor_loop)
        threads.append(sensor_thread)
    logging.info(f'Starting to produce messages for sensors {[x.name for x in sensors]}')
    for sensor_thread in threads:
        sensor_thread.start()
