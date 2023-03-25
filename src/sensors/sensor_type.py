from enum import Enum
from typing import List


class SensorType(Enum):
    NO_FAMILY_TYPE = 'No_family_type'
    ENVIRONMENTAL = 'Environmental'
    DISTANCE = 'Distance'
    LIGHT = 'Distance'
    OPTICAL = 'Optical'
    SOUND = 'Sound'

    ALL_TYPES: List[str] = [NO_FAMILY_TYPE, ENVIRONMENTAL, DISTANCE, LIGHT, OPTICAL, SOUND]
