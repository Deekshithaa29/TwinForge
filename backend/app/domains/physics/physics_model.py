from abc import ABC, abstractmethod

from app.domains.machine.machine import Machine


class PhysicsModel(ABC):
    """
    Base class for all physics models.
    """

    @abstractmethod
    def update(
        self,
        machine: Machine,
        dt: float
    ):
        pass