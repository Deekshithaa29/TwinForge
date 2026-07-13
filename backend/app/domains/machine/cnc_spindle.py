from app.domains.machine.machine import Machine
from app.domains.sensor.enums import SensorType



class CNCSpindle(Machine):

    def update(self, dt: float):

        super().update(dt)

        if self.status.value != "running":
            return

        temperature_sensor = self.get_sensor(
            SensorType.TEMPERATURE
        )

        if temperature_sensor:

            new_temperature = (
                temperature_sensor.read() + 0.2
            )

            temperature_sensor.update(
                new_temperature
            )