from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType
from app.twin.telemetry.telemetry_service import TelemetryService
from tests.helpers import create_spindle


def test_create_telemetry_snapshot():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    assert telemetry.machine_name == "Main Spindle"


def test_snapshot_contains_temperature():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    assert telemetry.temperature is not None
    assert telemetry.temperature >= 25.0


def test_snapshot_can_be_serialized():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    data = telemetry.to_dict()

    assert isinstance(data, dict)