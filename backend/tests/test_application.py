from app.core.application import Application
from unittest.mock import patch


def test_application_creation():

    app = Application()

    assert app.factory is not None
    assert app.simulation is not None


def test_default_factory_contains_machine():

    app = Application()

    assert len(app.factory.machines) == 1

    machine = app.factory.machines[0]

    assert machine.name == "Main Spindle"

@patch("app.infrastructure.mqtt.mqtt_publisher.MQTTPublisher.connect")
def test_application_start(mock_connect):

    app = Application()

    app.start()

    mock_connect.assert_called_once()


@patch("app.infrastructure.mqtt.mqtt_publisher.MQTTPublisher.disconnect")
def test_application_stop(mock_disconnect):

    app = Application()

    app.stop()

    mock_disconnect.assert_called_once()