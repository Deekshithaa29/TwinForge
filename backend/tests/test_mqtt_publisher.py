from unittest.mock import MagicMock, patch

from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher
from app.twin.telemetry.telemetry_service import TelemetryService
from tests.helpers import create_spindle


@patch("app.infrastructure.mqtt.mqtt_publisher.mqtt.Client")
def test_publish_calls_mqtt_client(mock_client):

    fake_client = MagicMock()

    mock_client.return_value = fake_client

    publisher = MQTTPublisher()
    publisher.connect()

    telemetry = TelemetryService.create_snapshot(
        create_spindle()
    )

    publisher.publish(telemetry)

    fake_client.publish.assert_called_once()

@patch("app.infrastructure.mqtt.mqtt_publisher.mqtt.Client")
def test_disconnect_calls_client(mock_client):

    fake_client = MagicMock()

    mock_client.return_value = fake_client

    publisher = MQTTPublisher()

    publisher.disconnect()

    fake_client.disconnect.assert_called_once()

@patch("app.infrastructure.mqtt.mqtt_publisher.mqtt.Client")
def test_connect_calls_client(mock_client):

    fake_client = MagicMock()

    mock_client.return_value = fake_client

    publisher = MQTTPublisher()

    publisher.connect()

    fake_client.connect.assert_called_once_with(
        "localhost",
        1883,
    )