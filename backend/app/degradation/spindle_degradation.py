from app.degradation.degradation_model import DegradationModel
from app.twin.machine.machine import Machine
from app.twin.sensor.enums import SensorType


class SpindleDegradationModel(DegradationModel):
    """
    Degradation model for a CNC spindle.
    Degradation increases as operating stress increases.
    """

    def update(self, machine: Machine, dt: float) -> None:

        temperature_sensor = machine.get_sensor_by_type(
            SensorType.TEMPERATURE
        )

        vibration_sensor = machine.get_sensor_by_type(
            SensorType.VIBRATION
        )

        temperature = (
            temperature_sensor.value
            if temperature_sensor
            else 25.0
        )

        vibration = (
            vibration_sensor.value
            if vibration_sensor
            else 0.0
        )

        rpm_ratio = machine.current_rpm / machine.max_rpm
        load = machine.load

        stress = (
            0.30 * rpm_ratio
            + 0.35 * load
            + 0.20 * max(0.0, (temperature - 40.0) / 60.0)
            + 0.15 * max(0.0, vibration / 10.0)
        )

        degradation_per_hour = 0.05 * stress

        degradation = degradation_per_hour * (dt / 3600)

        machine.health = max(
            0.0,
            machine.health - degradation,
        )