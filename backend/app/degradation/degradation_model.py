from abc import ABC, abstractmethod

from app.twin.machine.machine import Machine


class DegradationModel(ABC):
    """
    Defines how a machine degrades over time.
    """

    @abstractmethod
    def update(self, machine: Machine, dt: float) -> None:
        """
        Apply degradation for one simulation step.
        """
        pass