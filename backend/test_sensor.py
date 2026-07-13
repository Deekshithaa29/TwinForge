from app.domains.machine.machine import Machine
from app.domains.sensor.sensor import Sensor, SensorType

machine = Machine(
    name="CNC Spindle",
    machine_type="Spindle"
)

temperature  = Sensor(
    name="Spindle Temperature",
    sensor_type=SensorType.TEMPERATURE,
    unit="°C",
    min_value=20.0,
    max_value=120.0
)

temperature.update(85.0)

machine.add_sensor(temperature)

print(machine.name)
print(machine.sensors[0].name  )
print(machine.sensors[0].read())