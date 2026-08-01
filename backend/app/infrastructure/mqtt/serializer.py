import json

from app.twin.telemetry.telemetry import Telemetry


class TelemetrySerializer:

    @staticmethod
    def to_json(telemetry: Telemetry) -> str:
        return json.dumps(
            telemetry.to_dict(),
            default=str,
        )