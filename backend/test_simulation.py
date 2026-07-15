from app.twin.simulation.simulation import SimulationEngine

from app.twin.factory.factory import Factory

from app.twin.machine.cnc_spindle import CNCSpindle

from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType


factory = Factory("TwinForge Factory")


spindle = CNCSpindle("Main Spindle")


temperature = Sensor(
    name="Temperature",
    sensor_type=SensorType.TEMPERATURE,
    unit="°C",
    min_value=0,
    max_value=150,
)

temperature.update(25)

spindle.add_sensor(temperature)

spindle.start()

factory.add_machine(spindle)

print(factory.machines)
print(spindle.sensors)
simulation = SimulationEngine(factory)

simulation.start(max_ticks=10)