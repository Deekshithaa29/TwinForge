import random
from uuid import uuid4
from app.degradation.spindle_degradation import SpindleDegradationModel
from app.twin.machine.machine import Machine
from app.twin.machine.physics.spindle_physics import SpindlePhysics


class CNCSpindle(Machine):
    """
    Digital Twin representation of a CNC Spindle.
    """

    def __init__(self, name: str, machine_id: str | None = None):

        super().__init__(name=name, machine_type="CNC_SPINDLE", id=machine_id or str(uuid4()))

        self.current_rpm = 0.0  # Revolutions per minute
        self.max_rpm = 6000.0  # Target revolutions per minute
        self.load = 0.0

        self.target_load = random.uniform(0.02, 1.00)
        self.load_step = 0.05

        # Attach the physics model
        self.physics_model = SpindlePhysics()

        self.degradation_model = SpindleDegradationModel( base_degradation_rate=0.05)
