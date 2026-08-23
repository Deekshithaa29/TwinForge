from app.twin.factory.factory import Factory
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor
from app.twin.telemetry.telemetry_manager import TelemetryManager
from app.infrastructure.repository.memory_repository import InMemoryTelemetryRepository

def test_collects_latest_snapshot():

    factory = Factory("Factory")

    spindle = CNCSpindle("Main Spindle")

    temperature = Sensor(
        name="Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=0,
        max_value=150,
    )

    temperature.update(30)

    spindle.add_sensor(temperature)

    factory.add_machine(spindle)

    repository = InMemoryTelemetryRepository()

    manager = TelemetryManager(factory = factory, telemetry_repository = repository)

    manager.collect()

    snapshots = manager.get_latest()

    assert len(snapshots) == 1
    assert spindle.id in snapshots