from app.twin.machine.machine import Machine
from app.twin.machine.physics.spindle_physics import SpindlePhysics


class CNCSpindle(Machine):
    """
    Digital Twin representation of a CNC Spindle.
    """

    def __init__(self, name: str):

        super().__init__(
            name=name,
            machine_type="CNC_SPINDLE"
        )

        # Attach the physics model
        self.physics_model = SpindlePhysics()