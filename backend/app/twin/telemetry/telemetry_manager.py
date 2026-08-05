from app.twin.factory.factory import Factory
from app.twin.telemetry.telemetry import Telemetry
from app.twin.telemetry.telemetry_service import TelemetryService
from app.infrastructure.mqtt.publisher import Publisher
from app.infrastructure.websocket.manager import WebSocketManager


class TelemetryManager:
    """
    Collects telemetry from all machines in the factory.
    """

    def __init__(self, factory: Factory, publisher: Publisher | None = None, websocket_manager: WebSocketManager | None = None):
        self.factory = factory
        self.publisher = publisher
        self.websocket_manager = websocket_manager

        # Latest snapshot for each machine
        self.latest_snapshots: dict[str, Telemetry] = {}

    def collect(self):
        """
        Collect telemetry from every machine.
        """

        print("Telemetry websocket manager:", id(self.websocket_manager))

        for machine in self.factory.machines:

            snapshot = TelemetryService.create_snapshot(machine)

            self.latest_snapshots[machine.id] = snapshot

            if self.publisher:
                # print(f"Publishing telemetry for machine")
                self.publisher.publish(snapshot)

            if self.websocket_manager:
                self.websocket_manager.broadcast(snapshot.to_dict())

    def get_latest(self):

        return self.latest_snapshots