import random
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

        self.ambient_temperature = 25.0  # Ambient temperature in °C
        self.cooling_rate = 0.02  # Cooling rate per second

    def _update_load(self, machine, dt: float):

        # Simulate increasing load over time
        if abs(machine.load - machine.target_load) < 0.02:
            machine.target_load = random.uniform(0.02, 1.00)

        if machine.load < machine.target_load:
            machine.load = min(
                machine.load + (machine.load_step * dt),
                machine.target_load,
            )
        elif machine.load > machine.target_load:
            machine.load = max(
                machine.load - (machine.load_step * dt),
                machine.target_load,
            )

    def _update_rpm(self, machine, dt: float):
        # Simulate RPM changes based on load
        machine.current_rpm = machine.max_rpm * machine.load

    def _update_temperature(self, machine, dt: float):

        sensor = machine.get_sensor_by_type(
            SensorType.TEMPERATURE
        )

        if sensor is None:
            return

        current_temperature = sensor.read()

        heating = (
            machine.current_rpm
            / machine.max_rpm
        ) * self.heating_rate

        cooling = (current_temperature - self.ambient_temperature) * self.cooling_rate

        new_temperature = current_temperature + (heating - cooling) * dt

        sensor.update(
            new_temperature
        )

    def _update_vibration(self, machine,dt):

        sensor = machine.get_sensor_by_type(
            SensorType.VIBRATION
        )

        if sensor is None:
            return

        base = 0.5

        rpm_effect = (
            machine.current_rpm
            / machine.max_rpm       
        ) * 4.0

        wear_effect = (
            (100 - machine.health)
            / 100
        ) * 5.0

        vibration = (
            base + rpm_effect + wear_effect
        )

        sensor.update(vibration)


    def _update_health(self, machine, dt: float):

        wear = (
            machine.current_rpm
            / machine.max_rpm
        ) * self.wear_rate

        machine.health = max(
            machine.health - (wear * dt),
            0.0,
        )

    def update(self, machine, dt: float):

        self._update_load(machine, dt)
        self._update_rpm(machine, dt)
        self._update_temperature(machine, dt)
        self._update_vibration(machine, dt)
        self._update_health(machine, dt)

        

