from abc import ABC, abstractmethod

from app.twin.telemetry.telemetry import Telemetry


class Publisher(ABC):
    """
    Base interface for telemetry publishers.
    """

    @abstractmethod
    def publish(self, telemetry: Telemetry) -> None:
        pass