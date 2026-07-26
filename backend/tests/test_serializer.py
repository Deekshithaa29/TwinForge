import json

from app.infrastructure.mqtt.serializer import TelemetrySerializer
from app.twin.telemetry.telemetry_service import TelemetryService
from tests.helpers import create_spindle


def test_serializer_returns_json():
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    payload = TelemetrySerializer.to_json(telemetry)

    data = json.loads(payload)

    assert data["machine_name"] == "Main Spindle"