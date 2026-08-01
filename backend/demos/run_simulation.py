from app.infrastructure.listeners.console_listener import ConsoleTelemetryListener
from app.twin.factory.factory import Factory
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor
from app.twin.simulation.simulation import SimulationEngine

from app.infrastructure.listeners.console_listener import ConsoleTelemetryListener
from app.infrastructure.listeners.mqtt_listener import MQTTTelemetryListener
from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher

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

simulation = SimulationEngine(factory)

simulation.add_tick_listener(
    ConsoleTelemetryListener(factory)
)

publisher = MQTTPublisher()
publisher.connect()

simulation.add_tick_listener(
    MQTTTelemetryListener(factory, publisher)
)

simulation.start(max_ticks=10)
publisher.disconnect()