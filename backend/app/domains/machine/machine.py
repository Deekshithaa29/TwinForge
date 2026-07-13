from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .enums import MachineStatus
from app.domains.sensor.enums import SensorType
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.physics.physics_model import PhysicsModel

@dataclass
class Machine:
    """
    Base class for every machine in TwinForge.
    """

    name: str
    machine_type: str

    id: str = field(default_factory=lambda: str(uuid4()))
    status: MachineStatus = MachineStatus.IDLE
    health: float = 100.0
    runtime_hours: float = 0.0
    physics_model: Optional[PhysicsModel] = None

    sensors: list = field(default_factory=list)

    def get_sensor(self, sensor_type: SensorType):
        for sensor in self.sensors:
            if sensor.sensor_type == sensor_type:
                return sensor
        return None
    
    def has_sensor(self, sensor_type: SensorType):
        return self.get_sensor(sensor_type) is not None

    def start(self):
        self.status = MachineStatus.RUNNING

    def stop(self):
        self.status = MachineStatus.STOPPED

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def update(self, dt: float):
        """
        Called every simulation tick.

        dt = elapsed time in seconds
        """
        if self.status != MachineStatus.RUNNING:
            return

        self.runtime_hours += dt / 3600

        if self.physics_model:
            self.physics_model.update(self, dt)