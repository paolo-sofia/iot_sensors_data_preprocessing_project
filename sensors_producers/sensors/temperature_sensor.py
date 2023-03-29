import random
from dataclasses import dataclass
from pathlib import Path

from sensors_producers.sensors.abstract_sensor import AbstractSensor


@dataclass
class TemperatureSensor(AbstractSensor):
    config_file: Path = Path('sensors_producers/configs/temperature-sensor-config.toml')

    def read_sensor_value(self) -> float:
        """Reads sensor value and stores it into class attribute current_value.
        :return the sensor current value
        """
        return round(random.uniform(-20., 40.), 3)
