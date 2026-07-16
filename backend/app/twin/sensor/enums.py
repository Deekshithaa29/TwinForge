from enum import Enum


class SensorType(str, Enum):
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
    HUMIDITY = "humidity"
    VIBRATION = "vibration"
    FLOW = "flow"
    LEVEL = "level"
    PROXIMITY = "proximity"
    LIGHT = "light"
    SOUND = "sound"
