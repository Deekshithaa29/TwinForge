from dataclasses import dataclass

from app.maintenance.maintenance_status import MaintenanceStatus


@dataclass(frozen=True)
class MaintenanceAssessment:
    status: MaintenanceStatus
    severity: str
    message: str
    recommended_action: str
    predicted_rul_hours: float | None