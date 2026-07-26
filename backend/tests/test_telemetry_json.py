import json

from app.twin.telemetry.telemetry_service import TelemetryService
from tests.helpers import create_spindle


def test_snapshot_is_json_serializable():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    payload = json.dumps(telemetry.to_dict(), default=str)

    assert isinstance(payload, str)