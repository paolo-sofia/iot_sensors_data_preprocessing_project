import random
from dataclasses import dataclass
from pathlib import Path

from sensors_producers.sensors.abstract_sensor import AbstractSensor


@dataclass
class CarWallDistanceSensor(AbstractSensor):
    config_file: Path = Path('sensors_producers/configs/car-wall-distance-sensor-config.toml')

    def read_sensor_value(self) -> float:
        """Reads sensor value and stores it into class attribute current_value.
        :return the sensor current value
        """
        return round(random.uniform(0., 100.), 3)
