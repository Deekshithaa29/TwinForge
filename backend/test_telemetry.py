from pprint import pprint

from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor
from app.twin.telemetry.telemetry_service import TelemetryService

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

spindle.start()

spindle.update(10)

telemetry = TelemetryService.create_snapshot(spindle)

pprint(telemetry.to_dict())
