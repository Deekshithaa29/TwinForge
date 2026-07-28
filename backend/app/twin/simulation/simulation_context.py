from dataclasses import dataclass
from collections.abc import Callable

@dataclass
class SimulationContext:
    """
    Shared information for every simulation tick.
    """

    tick: int
    dt: float
    simulation_time: float

    on_tick: Callable | None = None