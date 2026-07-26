from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor


def create_temperature_sensor(
    value: float = 25.0,
) -> Sensor:
    """
    Creates a temperature sensor with an initial value.
    """

    sensor = Sensor(
        name="Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=0,
        max_value=150,
    )

    sensor.update(value)

    return sensor


def create_spindle(
    temperature: float = 25.0,
) -> CNCSpindle:
    """
    Creates a spindle with one temperature sensor.
    """

    spindle = CNCSpindle("Main Spindle")

    spindle.add_sensor(
        create_temperature_sensor(temperature)
    )

    return spindle