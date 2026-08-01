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
    vibration: float | None

    current_rpm: float
    load: float

    health: float

    runtime_hours: float

    def to_dict(self):
        """
        convert the telemetry data to a dictionary
        """

        data = asdict(self)

        if self.temperature is not None:
            data["temperature"] = round(self.temperature, 2)

        if self.vibration is not None:
            data["vibration"] = round(self.vibration, 2)

        data["current_rpm"] = round(self.current_rpm, 2)
        data["load"] = round(self.load, 2)
        data["health"] = round(self.health, 4)
        data["runtime_hours"] = round(self.runtime_hours, 4)

        return data
