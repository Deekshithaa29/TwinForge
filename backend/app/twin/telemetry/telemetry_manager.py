from app.twin.factory.factory import Factory
from app.twin.telemetry.telemetry import Telemetry
from app.twin.telemetry.telemetry_service import TelemetryService
from app.infrastructure.mqtt.publisher import Publisher


class TelemetryManager:
    """
    Collects telemetry from all machines in the factory.
    """

    def __init__(self, factory: Factory, publisher: Publisher | None = None,):
        self.factory = factory
        self.publisher = publisher

        # Latest snapshot for each machine
        self.latest_snapshots: dict[str, Telemetry] = {}

    def collect(self):
        """
        Collect telemetry from every machine.
        """

        for machine in self.factory.machines:

            snapshot = TelemetryService.create_snapshot(machine)

            self.latest_snapshots[machine.id] = snapshot

            if self.publisher:
                self.publisher.publish(snapshot)

    def get_latest(self):

        return self.latest_snapshots