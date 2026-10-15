
import os
from datetime import datetime, timezone

import pytest

from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher
from app.twin.telemetry.telemetry import Telemetry


@pytest.mark.integration
def test_live_mqtt_publish():
    if os.getenv("TWINFORGE_LIVE_MQTT") != "1":
        pytest.skip(
            "Live MQTT test disabled. "
            "Set TWINFORGE_LIVE_MQTT=1 to run."
        )

    publisher = MQTTPublisher()

    telemetry = Telemetry(
        timestamp=datetime.now(timezone.utc),
        machine_id="M1",
        machine_name="Test Spindle",
        machine_type="CNC_SPINDLE",
        status="RUNNING",
        temperature=65.0,
        vibration=2.5,
        current_rpm=3000.0,
        load=0.75,
        health=85.0,
        health_state="HEALTHY",
        runtime_hours=12.0,
        predicted_rul_hours=120.0,
    )

    try:
        publisher.connect()

        # Wait for the asynchronous connection callback.
        if not publisher._connected.wait(timeout=10):
            pytest.fail(
                "MQTT broker did not connect within 10 seconds"
            )

        publisher.publish(telemetry)

    finally:
        publisher.disconnect()
