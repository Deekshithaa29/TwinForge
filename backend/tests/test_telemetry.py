from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType
from app.twin.telemetry.telemetry_service import TelemetryService


def create_spindle():
    spindle = CNCSpindle("Main Spindle")

    temperature = Sensor(
        name="Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=0,
        max_value=150,
    )

    temperature.update(25.0)

    spindle.add_sensor(temperature)

    spindle.start()

    spindle.update(10)

    return spindle


def test_create_telemetry_snapshot():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    assert telemetry.machine_name == "Main Spindle"


def test_snapshot_contains_temperature():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    assert telemetry.temperature is not None
    assert telemetry.temperature > 25.0


def test_snapshot_can_be_serialized():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    data = telemetry.to_dict()

    assert isinstance(data, dict)