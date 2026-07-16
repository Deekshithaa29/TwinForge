from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class Telemetry:
    """
    Represents a single telemetry snapshot of a machine.
    """

    timestamp: datetime

    machine_id: str
    machine_name: str
    machine_type: str

    status: str

    temperature: float | None

    health: float

    runtime_hours: float

    def to_dict(self):
        """
        convert the telemetry data to a dictionary
        """

        return asdict(self)
