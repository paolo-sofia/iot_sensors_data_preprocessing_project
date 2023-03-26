import random
from dataclasses import dataclass
from pathlib import Path

from sensors_producers.sensors.abstract_sensor import AbstractSensor


@dataclass
class HumiditySensor(AbstractSensor):
    config_file: Path = Path('../sensors_producers/configs/humidity-sensor-config.toml')

    def read_sensor_value(self) -> float:
        """Reads sensor value and stores it into class attribute current_value.
        :return the sensor current value
        """
        return random.uniform((0., 100.), 3)
