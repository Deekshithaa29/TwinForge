from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType


def test_spindle_creation():
    spindle = CNCSpindle("Main Spindle")

    assert spindle.name == "Main Spindle"


def test_spindle_initially_has_no_sensors():
    spindle = CNCSpindle("Main Spindle")

    assert len(spindle.sensors) == 0

def test_add_sensor_to_spindle():
    spindle = CNCSpindle("Main Spindle")

    sensor = Sensor(
        name="Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=0,
        max_value=150,
    )

    spindle.add_sensor(sensor)

    assert len(spindle.sensors) == 1