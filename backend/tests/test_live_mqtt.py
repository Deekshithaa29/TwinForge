import time

from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher
from app.twin.telemetry.telemetry_service import TelemetryService
from tests.helpers import create_spindle

publisher = MQTTPublisher()

publisher.connect()

try:
    spindle = create_spindle()

    telemetry = TelemetryService.create_snapshot(spindle)

    publisher.publish(telemetry)

    print("Telemetry published!")

    time.sleep(2)

finally:
    publisher.disconnect()

    print("Disconnected.")