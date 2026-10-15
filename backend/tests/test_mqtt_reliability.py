
from unittest.mock import Mock, patch

import paho.mqtt.client as mqtt
import pytest

from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher
from app.infrastructure.mqtt.topics import MACHINE_TELEMETRY


@pytest.fixture
def mqtt_client():
    with patch(
        "app.infrastructure.mqtt.mqtt_publisher.mqtt.Client"
    ) as client_class:
        client = client_class.return_value
        client.loop_start.return_value = mqtt.MQTT_ERR_SUCCESS
        client.publish.return_value.rc = mqtt.MQTT_ERR_SUCCESS
        yield client


def test_connect_starts_background_network_loop(mqtt_client):
    publisher = MQTTPublisher()

    publisher.connect()

    mqtt_client.connect_async.assert_called_once_with(
        "localhost",
        1883,
        keepalive=60,
    )
    mqtt_client.loop_start.assert_called_once()

    assert publisher.is_connected is False


def test_connect_is_idempotent(mqtt_client):
    publisher = MQTTPublisher()

    publisher.connect()
    publisher.connect()

    mqtt_client.connect_async.assert_called_once()
    mqtt_client.loop_start.assert_called_once()


def test_connect_callback_updates_connection_state(mqtt_client):
    publisher = MQTTPublisher()

    publisher.on_connect(
        mqtt_client, None, None, 0, None
    )

    assert publisher.is_connected is True

    publisher.on_disconnect(
        mqtt_client, None, None, 1, None
    )

    assert publisher.is_connected is False


def test_failed_connect_callback_keeps_disconnected(mqtt_client):
    publisher = MQTTPublisher()

    publisher.on_connect(
        mqtt_client, None, None, 128, None
    )

    assert publisher.is_connected is False


def test_publish_when_disconnected_raises(mqtt_client):
    publisher = MQTTPublisher()

    with pytest.raises(
        ConnectionError,
        match="not connected",
    ):
        publisher.publish(Mock())

    mqtt_client.publish.assert_not_called()


def test_publish_when_connected(mqtt_client):
    publisher = MQTTPublisher()

    publisher.on_connect(
        mqtt_client, None, None, 0, None
    )

    telemetry = Mock()

    with patch(
        "app.infrastructure.mqtt.mqtt_publisher.TelemetrySerializer.to_json",
        return_value='{"machine_id":"M1"}',
    ):
        publisher.publish(telemetry)

    mqtt_client.publish.assert_called_once_with(
        MACHINE_TELEMETRY,
        '{"machine_id":"M1"}',
        qos=0,
    )


def test_publish_failure_raises(mqtt_client):
    publisher = MQTTPublisher()

    publisher.on_connect(
        mqtt_client, None, None, 0, None
    )

    mqtt_client.publish.return_value.rc = mqtt.MQTT_ERR_NO_CONN

    with patch(
        "app.infrastructure.mqtt.mqtt_publisher.TelemetrySerializer.to_json",
        return_value="{}",
    ):
        with pytest.raises(
            ConnectionError,
            match="MQTT publish failed",
        ):
            publisher.publish(Mock())


def test_disconnect_is_idempotent(mqtt_client):
    publisher = MQTTPublisher()

    publisher.connect()
    publisher.disconnect()
    publisher.disconnect()

    mqtt_client.disconnect.assert_called_once()
    mqtt_client.loop_stop.assert_called_once()

    assert publisher.is_connected is False
