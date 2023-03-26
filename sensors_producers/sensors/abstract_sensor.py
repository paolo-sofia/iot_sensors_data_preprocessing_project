import json
import tomllib
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from time import sleep

from kafka3 import KafkaProducer

from src.sensors_producers.sensor_type import SensorFamilyType


@dataclass
class AbstractSensor(ABC):
    config_file: str = field(default_factory=Path)
    id: str = ''
    name: str = ''
    type: str = ''
    topic: str = ''
    data_topic: str = ''
    frequency: float = 1.0
    producer: KafkaProducer = None

    def __post_init__(self) -> None:
        self.load_config(self.config_file)
        return

    def load_config(self, config_file: str) -> None:
        with open(config_file, 'rb') as f:
            config = tomllib.load(f)

        config['producer']['api_version'] = tuple(config['producer']['api_version'])
        self.producer: KafkaProducer = KafkaProducer(**dict(config['producer']))
        self.id: str = config['sensor'].get('id', '')
        self.name: str = config['sensor'].get('name', '')
        self.topic: str = config['sensor'].get('topic', '')
        self.data_topic: str = config['sensor'].get('data_topic', '')

        self.type: str = config['sensor'].get('type', SensorFamilyType.NO_FAMILY_TYPE)
        if self.type not in SensorFamilyType.ALL_TYPES:
            self.type = SensorFamilyType.NO_FAMILY_TYPE

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
        data_readings = {
            'id': self.id,
            'name': self.name,
            'value': current_value,
            'sensor_type': self.type
        }
        data_readings = json.dumps(data_readings).encode('utf-8')

        self.producer.send(self.data_topic, value=data_readings, key=self.id.encode('utf-8'))
        return

    def publish_sensor_initialization(self) -> None:
        sensor = {
            'id': self.id,
            'name': self.name
        }
        sensor = json.dumps(sensor).encode('utf-8')
        self.producer.send(self.data_topic, value=sensor, key=self.id.encode('utf-8'))
        print(f'published {sensor}')
        return

    def sensor_loop(self) -> None:
        """Runs the main loop for this sensor: a.k.a, reads the sensor value at the specified interval and publish the
        value on the current topic
        """
        self.publish_sensor_initialization()
        while True:
            current_value = self.read_sensor_value()
            self.publish_current_value(current_value)
            sleep(1 / self.frequency)
        return
