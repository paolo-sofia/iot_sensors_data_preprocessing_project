import random
from pathlib import Path

from src.sensors_producers.sensors.abstract_sensor import AbstractSensor
from dataclasses import dataclass


@dataclass
class TemperatureSensor(AbstractSensor):
    config_file: Path = Path('sensors_producers/configs/temperature-sensor-config.toml')

    def read_sensor_value(self) -> float:
        """Reads sensor value and stores it into class attribute current_value.
        :return the sensor current value
        """
        return random.uniform(-20., 40.)


