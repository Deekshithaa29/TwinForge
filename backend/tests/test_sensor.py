from app.twin.machine.machine import Machine
from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType


def test_add_temperature_sensor():
    machine = Machine(
        name="CNC Spindle",
        machine_type="Spindle",
    )

    temperature = Sensor(
        name="Spindle Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=20.0,
        max_value=120.0,
    )

    temperature.update(85.0)

    machine.add_sensor(temperature)

    sensor = machine.get_sensor_by_type(SensorType.TEMPERATURE)

    assert sensor is not None
    assert sensor.name == "Spindle Temperature"
    assert sensor.read() == 85.0