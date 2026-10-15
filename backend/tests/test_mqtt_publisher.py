from unittest.mock import MagicMock, Mock, patch

import paho.mqtt.client as mqtt
import pytest
from app.infrastructure.mqtt.topics import MACHINE_TELEMETRY
from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher
from app.twin.telemetry.telemetry_service import TelemetryService

@pytest.fixture
def mock_client_class():
    with patch(
        "app.infrastructure.mqtt.mqtt_publisher.mqtt.Client"
    ) as mocked_class:

        mocked_client = mocked_class.return_value

        mocked_client.loop_start.return_value = (
            mqtt.MQTT_ERR_SUCCESS
        )

        mocked_client.publish.return_value.rc = (
            mqtt.MQTT_ERR_SUCCESS
        )

        yield mocked_class

def test_publish_calls_mqtt_client(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.loop_start.return_value = mqtt.MQTT_ERR_SUCCESS
    mock_client.publish.return_value.rc = mqtt.MQTT_ERR_SUCCESS

    publisher = MQTTPublisher()

    # Simulate a successful MQTT connection callback.
    publisher.on_connect(
        mock_client,
        None,
        None,
        0,
        None,
    )

    telemetry = Mock()

    with patch(
        "app.infrastructure.mqtt.mqtt_publisher.TelemetrySerializer.to_json",
        return_value='{"machine_id":"M1"}',
    ):
        publisher.publish(telemetry)

    mock_client.publish.assert_called_once_with(
        MACHINE_TELEMETRY,
        '{"machine_id":"M1"}',
        qos=0,
    )

def test_disconnect_calls_client(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.loop_start.return_value = mqtt.MQTT_ERR_SUCCESS

    publisher = MQTTPublisher()

    publisher.connect()
    publisher.disconnect()

    mock_client.disconnect.assert_called_once()
    mock_client.loop_stop.assert_called_once()

def test_connect_calls_client(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.loop_start.return_value = mqtt.MQTT_ERR_SUCCESS

    publisher = MQTTPublisher()

    publisher.connect()

    mock_client.connect_async.assert_called_once_with(
        "localhost",
        1883,
        keepalive=60,
    )
    mock_client.loop_start.assert_called_once()