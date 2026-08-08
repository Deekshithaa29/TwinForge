from app.twin.factory.factory import Factory
from app.twin.telemetry.telemetry import Telemetry
from app.twin.telemetry.telemetry_service import TelemetryService
from app.infrastructure.repository.telemetry_repository import TelemetryRepository
from app.infrastructure.mqtt.publisher import Publisher
from app.infrastructure.websocket.manager import WebSocketManager


class TelemetryManager:
    """
    Collects telemetry from all machines in the factory.
    """

    def __init__(self, factory: Factory, telemetry_repository: TelemetryRepository | None = None, publisher: Publisher | None = None, websocket_manager: WebSocketManager | None = None):
        self.factory = factory
        self.telemetry_repository = telemetry_repository
        self.publisher = publisher
        self.websocket_manager = websocket_manager


    def collect(self):
        """
        Collect telemetry from every machine.
        """

        print("Telemetry websocket manager:", id(self.websocket_manager))

        for machine in self.factory.machines:

            snapshot = TelemetryService.create_snapshot(machine)

            self.telemetry_repository.save(snapshot)

            if self.publisher:
                # print(f"Publishing telemetry for machine")
                self.publisher.publish(snapshot)

            if self.websocket_manager:
                self.websocket_manager.broadcast(snapshot.to_dict())

    def get_latest(self):

        return self.telemetry_repository.get_latest()

    def get_history(self):
        return self.telemetry_repository.get_all_history()

    def get_history_for_machine(
        self,
        machine_id: str,
    ):
        return self.telemetry_repository.get_history_for_machine(machine_id)    