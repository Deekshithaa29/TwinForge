from dataclasses import dataclass


@dataclass
class SimulationContext:
    """
    Shared information for every simulation tick.
    """

    tick: int
    dt: float
    simulation_time: float
