from pathlib import Path
from dataclasses import dataclass
import random

from src.sensors.abstract_sensor import AbstractSensor


@dataclass
class CarWallDistanceSensor(AbstractSensor):
    config_file: str = Path('sensors/configs/car-wall-distance-sensor-config.toml')

    def read_sensor_value(self) -> float:
        """Reads sensor value and stores it into class attribute current_value.
        :return the sensor current value
        """
        return random.uniform((0., 100.), 3)

