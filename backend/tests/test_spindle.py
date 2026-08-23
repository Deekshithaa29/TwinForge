from app.twin.machine.physics.spindle_physics import SpindlePhysics
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

# def test_spindle_sets_default_rpm_when_started():

#     spindle = CNCSpindle("Main Spindle")

#     spindle.start()

#     assert spindle.current_rpm == 1500

def test_spindle_rpm_zero_when_stopped():

    spindle = CNCSpindle("Main Spindle")

    spindle.start()

    spindle.stop()

    assert spindle.current_rpm == 0

def test_load_increases_after_update():
    spindle = CNCSpindle("Main Spindle")

    physics = SpindlePhysics()

    spindle.load = 0.0

    physics.update(spindle, 1.0)

    assert spindle.load > 0.0

def test_rpm_follows_load():
    spindle = CNCSpindle("Main Spindle")

    physics = SpindlePhysics()

    spindle.load = 0.5

    physics.update(spindle, 1.0)

    assert spindle.current_rpm > 0

def test_spindle_uses_provided_machine_id():
    spindle = CNCSpindle(
        name="Main Spindle",
        machine_id="CNC-SPINDLE-001",
    )

    assert spindle.id == "CNC-SPINDLE-001"

def test_spindle_generates_id_when_not_provided():
    spindle = CNCSpindle("Main Spindle")

    assert spindle.id