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
    health_state: str

    runtime_hours: float
    predicted_rul_hours: float | None = None

    def to_dict(self):
        """
        convert the telemetry data to a dictionary
        """

        data = asdict(self)

        data["timestamp"] = self.timestamp.isoformat()

        if self.temperature is not None:
            data["temperature"] = round(self.temperature, 2)

        if self.vibration is not None:
            data["vibration"] = round(self.vibration, 2)

        if self.predicted_rul_hours is not None:
            data["predicted_rul_hours"] = round(self.predicted_rul_hours, 2)

        data["current_rpm"] = round(self.current_rpm, 2)
        data["load"] = round(self.load, 2)
        data["health"] = round(self.health, 4)
        data["runtime_hours"] = round(self.runtime_hours, 4)

        return data

    def to_database(self) -> tuple:
        """
        Convert the telemetry data to a tuple for database insertion.
        """

        return (
            self.timestamp.isoformat(),
            self.machine_id,
            self.machine_name,
            self.machine_type,
            self.status,
            self.temperature,
            self.vibration,
            self.current_rpm,
            self.load,
            self.health,
            self.runtime_hours,
            self.predicted_rul_hours
        )
