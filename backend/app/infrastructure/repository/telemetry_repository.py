from abc import ABC, abstractmethod
from typing import override

from app.twin.telemetry.telemetry import Telemetry


class TelemetryRepository(ABC):
    """
    Contract for telemetry persistence.
    """

    @abstractmethod
    def save(self, telemetry: Telemetry) -> None:
        """Persist a telemetry snapshot."""
        pass

    @override
    def get_latest(self) -> dict[str, Telemetry]:
        """Return the latest telemetry for all machines."""
        raise NotImplementedError

    @override
    def get_latest_for_machine(
        self,
        machine_id: str,
    ) -> Telemetry | None:
        """Return the latest telemetry for a machine."""
        raise NotImplementedError

    @override
    def get_all_history(self) -> dict[str, list[Telemetry]]:
        """Return the complete telemetry history."""
        raise NotImplementedError

    @override
    def get_history_for_machine(
        self,
        machine_id: str,
    ) -> list[Telemetry]:
        """Return the telemetry history for a machine."""
        raise NotImplementedError

    @override
    def clear(self) -> None:
        """Remove all stored telemetry."""
        raise NotImplementedError