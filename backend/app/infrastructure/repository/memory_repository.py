from collections import defaultdict
from app.twin.telemetry.telemetry import Telemetry
from app.infrastructure.repository.telemetry_repository import TelemetryRepository


class InMemoryTelemetryRepository(TelemetryRepository):    
    """
    Stores telemetry snapshots in memory.

    Later this repository can be replaced with a database-backed
    implementation without affecting the rest of the application.
    """

    def __init__(self):
        self._latest: dict[str, Telemetry] = {}

        self._history: dict[str, list[Telemetry]] = defaultdict(list)

        self._history_limit = 1000

    def save(self, telemetry: Telemetry) -> None:
        """
        Save the latest telemetry and append it to history.
        """

        machine_id = telemetry.machine_id

        self._latest[machine_id] = telemetry

        history = self._history[machine_id]

        history.append(telemetry)

        if len(history) > self._history_limit:
            history.pop(0)

    
    def get_latest(self) -> dict[str, Telemetry]:
        return self._latest

    
    def get_latest_for_machine(
        self,
        machine_id: str,
    ) -> Telemetry | None:
        return self._latest.get(machine_id)

    
    def get_all_history(self) -> dict[str, list[Telemetry]]:
        """
        Return telemetry history for all machines.
        """
        return self._history

    
    def get_history_for_machine(
        self,
        machine_id: str,
    ) -> list[Telemetry]:
        """
        Return telemetry history for a single machine.
        """
        return self._history.get(machine_id, [])

    
    def clear(self):
        self._latest.clear()
        self._history.clear()