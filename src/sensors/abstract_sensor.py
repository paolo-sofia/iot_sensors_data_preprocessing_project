from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.sensors.sensor_type import SensorType
from time import sleep
from kafka import KafkaProducer
from pathlib import Path
import tomllib


@dataclass
class AbstractSensor(ABC):
    config_file: Path
    id: str = ''
    type: str = ''
    topic: str = ''
    frequency: float = 1.0
    producer: KafkaProducer = None

    def __post_init__(self) -> None:
        self.load_config(self.config_file)
        return

    def load_config(self, config_file: str) -> None:
        with open(config_file, 'rb') as f:
            config = tomllib.load(f)

        self.producer: KafkaProducer = KafkaProducer(**dict(config['producer']))
        self.id: str = config['sensor'].get('id', '')
        self.topic: str = config['sensor'].get('topic', '')

        self.type: str = config['sensor'].get('type', SensorType.NO_FAMILY_TYPE)
        if self.type not in SensorType.ALL_TYPES:
            self.type = SensorType.NO_FAMILY_TYPE

        try:
            self.frequency: float = float(config['sensor'].get('frequency', ''))
        except ValueError as e:
            self.frequency: float = 1.0
        return

    @abstractmethod
    def read_sensor_value(self) -> float:
        """Reads sensor value and stores it into class attribute current_value.
        :return the sensor current value
        """
        pass

    def publish_current_value(self, current_value: float) -> None:
        """Publish the last rea value to its own custom topic.
        :param current_value: the value read from the sensor to be published.
        :return None"""
        self.producer.send(self.topic, value=bytes(current_value), key=bytes(self.id))
        return

    def sensor_loop(self) -> None:
        """Runs the main loop for this sensor: a.k.a, reads the sensor value at the specified interval and publish the
        value on the current topic
        """
        while True:
            current_value = self.read_sensor_value()
            self.publish_current_value(current_value)
            sleep(1 / self.frequency)
        return
