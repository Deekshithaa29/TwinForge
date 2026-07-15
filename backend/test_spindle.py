from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType

# Create spindle
spindle = CNCSpindle("Main Spindle")

# Create temperature sensor
temperature_sensor = Sensor(
    name="Temperature",
    sensor_type=SensorType.TEMPERATURE,
    unit="°C",
    min_value=0,
    max_value=150,
)

# Initial value
temperature_sensor.update(25.0)

# Attach sensor
spindle.add_sensor(temperature_sensor)

# Start machine
spindle.start()

print("=" * 50)

for tick in range(1, 11):

    spindle.update(1)

    print(
        f"Tick {tick:02d} | "
        f"Temperature: {spindle.get_sensor(SensorType.TEMPERATURE).read():.2f}°C | "
        f"Health: {spindle.health:.4f}% | "
        f"Runtime: {spindle.runtime_hours:.6f} h"
    )

print("=" * 50)