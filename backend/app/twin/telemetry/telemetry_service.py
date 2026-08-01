from datetime import datetime, UTC

from app.twin.machine.machine import Machine
from app.twin.sensor.enums import SensorType
from app.twin.telemetry.telemetry import Telemetry


class TelemetryService:
    """
    Generates telemetry snapshots from machines.
    """

    @staticmethod
    def create_snapshot(machine: Machine) -> Telemetry:

        temperature_sensor = machine.get_sensor_by_type(SensorType.TEMPERATURE)
        vibration_sensor = machine.get_sensor_by_type(SensorType.VIBRATION)

        temperature = None
        vibration = None

        if vibration_sensor:
            vibration = vibration_sensor.read()


        if temperature_sensor:
            temperature = temperature_sensor.read()

        return Telemetry(
            timestamp=datetime.now(UTC),
            machine_id=machine.id,
            machine_name=machine.name,
            machine_type=machine.machine_type,
            status=machine.status.name,
            temperature=temperature,
            vibration=vibration,
            current_rpm=machine.current_rpm,
            load=machine.load,
            health=machine.health,
            runtime_hours=machine.runtime_hours,
        )
