from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.twin.machine.machine import Machine


class PhysicsModel(ABC):
    """
    Base class for every machine physics model.
    """

    @abstractmethod
    def update(self, machine: Machine, dt: float):
        """
        Update the machine's physical state for one simulation tick.

        Parameters
        ----------
        machine : Machine
            The machine being simulated.

        dt : float
            Delta time in seconds.
        """
        raise NotImplementedError
