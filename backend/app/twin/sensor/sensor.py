from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .enums import SensorType


@dataclass
class Sensor:
    """
    Base Sensor class.

    Every physical sensor in TwinForge inherits from this.
    """

    name: str
    sensor_type: SensorType
    unit: str

    id: str = field(default_factory=lambda: str(uuid4()))

    value: float = 0.0

    min_value: float = 0.0
    max_value: float = 100.0

    def update(self, value: float):

        self.value = max(self.min_value, min(value, self.max_value))

    def read(self):

        return self.value
