from time import sleep

from app.domains.machine.cnc_spindle import CNCSpindle
from app.domains.sensor.sensor import Sensor
from app.domains.sensor.enums import SensorType

spindle = CNCSpindle(
    name="Main Spindle",
    machine_type="Spindle"
)

temperature = Sensor(
    name="Temperature",
    sensor_type=SensorType.TEMPERATURE,
    unit="°C",
    min_value=20,
    max_value=120
)

temperature.update(30)

spindle.add_sensor(temperature)

spindle.start()

for _ in range(5):

    spindle.update(1)

    print(
        spindle.get_sensor(
            SensorType.TEMPERATURE
        ).read()
    )

    sleep(1)