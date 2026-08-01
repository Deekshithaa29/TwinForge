from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher
from app.twin.factory.factory import Factory
from app.twin.simulation.simulation_context import SimulationContext
from app.twin.telemetry.telemetry_manager import TelemetryManager


class MQTTTelemetryListener:
    """
    Publishes telemetry after every simulation tick.
    """

    def __init__(
        self,
        telemetry_manager: TelemetryManager,
    ):
        self.telemetry = telemetry_manager

    def __call__(self, context: SimulationContext) -> None:
        # print("Publishing telemetry...")
        # print(id(self.telemetry_manager))
        self.telemetry.collect()