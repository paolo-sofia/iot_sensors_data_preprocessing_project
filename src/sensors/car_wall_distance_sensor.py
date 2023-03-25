from pathlib import Path
import random
from src.sensors.abstract_sensor import AbstractSensor
from dataclasses import dataclass

@dataclass
class CarWallDistanceSensor(AbstractSensor):
    config_file: Path = Path('sensors/configs/car-wall-distance-sensor-config.toml')

    def read_sensor_value(self) -> float:
        """Reads sensor value and stores it into class attribute current_value.
        :return the sensor current value
        """
        return random.uniform((0., 100.), 3)

