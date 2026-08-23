from app.degradation.spindle_degradation import SpindleDegradationModel
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor


def create_spindle():
    spindle = CNCSpindle("Test Spindle")

    temperature = Sensor(
        name="Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=0,
        max_value=150,
    )

    vibration = Sensor(
        name="Vibration",
        sensor_type=SensorType.VIBRATION,
        unit="mm/s",
        min_value=0,
        max_value=50,
    )

    spindle.add_sensor(temperature)
    spindle.add_sensor(vibration)

    return spindle


def test_health_decreases_under_stress():
    spindle = create_spindle()

    spindle.current_rpm = 5000
    spindle.max_rpm = 6000
    spindle.load = 0.8

    spindle.get_sensor_by_type(
        SensorType.TEMPERATURE
    ).update(80)

    spindle.get_sensor_by_type(
        SensorType.VIBRATION
    ).update(8)

    initial_health = spindle.health

    model = SpindleDegradationModel()

    model.update(spindle, 3600)

    assert spindle.health < initial_health

def test_high_stress_degrades_faster():
    low = create_spindle()
    high = create_spindle()

    low.current_rpm = 1000
    low.max_rpm = 6000
    low.load = 0.2

    low.get_sensor_by_type(
        SensorType.TEMPERATURE
    ).update(30)

    low.get_sensor_by_type(
        SensorType.VIBRATION
    ).update(1)

    high.current_rpm = 5500
    high.max_rpm = 6000
    high.load = 0.9

    high.get_sensor_by_type(
        SensorType.TEMPERATURE
    ).update(90)

    high.get_sensor_by_type(
        SensorType.VIBRATION
    ).update(10)

    model = SpindleDegradationModel()

    model.update(low, 3600)
    model.update(high, 3600)

    assert high.health < low.health

def test_health_never_below_zero():
    spindle = create_spindle()

    spindle.health = 0.01
    spindle.current_rpm = 6000
    spindle.max_rpm = 6000
    spindle.load = 1.0

    spindle.get_sensor_by_type(
        SensorType.TEMPERATURE
    ).update(120)

    spindle.get_sensor_by_type(
        SensorType.VIBRATION
    ).update(20)

    model = SpindleDegradationModel()

    model.update(spindle, 100000)

    assert spindle.health >= 0.0