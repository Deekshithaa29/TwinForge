from dataclasses import dataclass


@dataclass
class LifecycleRecord:
    """
    Represents one observation during a machine lifecycle.
    """

    run_id: int 
    cycle: int

    machine_id: str

    runtime_hours: float

    temperature: float | None
    vibration: float | None

    rpm: float
    load: float

    health: float
    health_state: str

    rul_hours: float | None = None