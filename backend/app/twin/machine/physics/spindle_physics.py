from app.twin.machine.physics.physics_model import PhysicsModel
from app.twin.sensor.enums import SensorType


class SpindlePhysics(PhysicsModel):
    """
    Physics model for a CNC spindle.
    """

    def __init__(self):

        # Degrees Celsius increase per second
        self.heating_rate = 0.15

        # Health degradation per second
        self.wear_rate = 0.0002

    def update(self, machine, dt: float):

        # ----------------------------
        # Temperature
        # ----------------------------

        temperature_sensor = machine.get_sensor_by_type(SensorType.TEMPERATURE)

        if temperature_sensor:

            current_temp = temperature_sensor.read()

            new_temp = current_temp + (self.heating_rate * dt)

            temperature_sensor.update(new_temp)

        # ----------------------------
        # Machine Health
        # ----------------------------

        machine.health -= self.wear_rate * dt

        machine.health = max(machine.health, 0.0)
