from typing import List


class QueryOptions:
    SENSOR = 'sensor'
    SENSOR_FAMILY = 'sensor_family'


class SensorFamilyType:
    NO_FAMILY_TYPE: str = 'No_family_type'
    ENVIRONMENTAL: str = 'Environmental'
    DISTANCE: str = 'Distance'
    LIGHT: str = 'Distance'
    OPTICAL: str = 'Optical'
    SOUND: str = 'Sound'

    ALL_TYPES: List[str] = [NO_FAMILY_TYPE, ENVIRONMENTAL, DISTANCE, LIGHT, OPTICAL, SOUND]
