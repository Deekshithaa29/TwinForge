from app.infrastructure.mqtt.console_publisher import ConsolePublisher
from app.twin.factory.factory import Factory
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor
from app.twin.telemetry.telemetry_manager import TelemetryManager


def test_console_publisher(capsys):
    factory = Factory("TwinForge Factory")

    spindle = CNCSpindle("Main Spindle")

    temperature = Sensor(
        name="Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=0,
        max_value=150,
    )

    temperature.update(25.0)

    spindle.add_sensor(temperature)

    factory.add_machine(spindle)

    publisher = ConsolePublisher()

    manager = TelemetryManager(factory, publisher)

    manager.collect()

    captured = capsys.readouterr()

    assert "Publishing Telemetry" in captured.out
    assert "Main Spindle" in captured.out