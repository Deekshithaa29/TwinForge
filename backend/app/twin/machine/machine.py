from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from app.twin.machine.enums import MachineStatus
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor
from app.twin.machine.health import HealthState

if TYPE_CHECKING:
    from app.twin.machine.physics.physics_model import PhysicsModel
    from app.degradation.degradation_model import DegradationModel



@dataclass
class Machine:
    """
    Base class for every machine in the digital twin.
    """

    name: str
    machine_type: str

    id: str = field(default_factory=lambda: str(uuid4()))

    status: MachineStatus = MachineStatus.IDLE

    health: float = 100.0

    runtime_hours: float = 0.0

    degradation_model: Optional["DegradationModel"] = None
    # Key = SensorType, Value = Sensor object
    sensors: dict[SensorType, Sensor] = field(default_factory=dict)

    physics_model: Optional["PhysicsModel"] = None

    @property
    def health_state(self) -> HealthState:
        """Return the health state of the machine based on its health value."""
        if self.health >= 80.0:
            return HealthState.HEALTHY
        elif self.health >= 50.0:
            return HealthState.DEGRADED
        elif self.health >= 20.0:
            return HealthState.CRITICAL
        else:
            return HealthState.FAILED

    def start(self):
        """Start the machine."""
        self.status = MachineStatus.RUNNING

    def stop(self):
        """Stop the machine."""
        self.status = MachineStatus.STOPPED

    def add_sensor(self, sensor: Sensor):
        """Attach a sensor to the machine."""
        self.sensors[sensor.sensor_type] = sensor

    def remove_sensor(self, sensor_type: SensorType):
        """Remove a sensor from the machine."""
        self.sensors.pop(sensor_type, None)

    def get_sensor_by_type(self, sensor_type: SensorType):
        """Return a sensor if present."""
        return self.sensors.get(sensor_type)

    def has_sensor(self, sensor_type: SensorType) -> bool:
        """Check whether a sensor exists."""
        return sensor_type in self.sensors

    def update(self, dt: float):
        """
        Update the machine for one simulation tick.
        """

        if self.status != MachineStatus.RUNNING:
            return

        # Convert seconds to hours
        self.runtime_hours += dt / 3600

        # Delegate behavior to the physics model
        if self.physics_model:
            self.physics_model.update(self, dt)

        if self.degradation_model:
            self.degradation_model.update(self, dt)

        if self.health_state == HealthState.FAILED:
            self.status = MachineStatus.STOPPED
