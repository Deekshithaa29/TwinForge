from app.maintenance.maintenance_assessment import MaintenanceAssessment
from app.maintenance.maintenance_status import MaintenanceStatus


class PredictiveMaintenanceService:

    DUE_SOON_RUL_HOURS = 150.0
    REQUIRED_RUL_HOURS = 50.0
    CRITICAL_RUL_HOURS = 20.0

    def evaluate(
        self,
        predicted_rul_hours: float | None,
        health: float,
        health_state: str,
    ) -> MaintenanceAssessment:

        if health_state.upper() == "FAILED":
            return MaintenanceAssessment(
                status=MaintenanceStatus.CRITICAL,
                severity="CRITICAL",
                message=("Machine failure detected. "
                         "Operation stopped. Immediate maintenance required."),
                recommended_action=("Do not restart the machine until the failure "
                                    "has been diagnosed and corrective maintenance completed."),
                predicted_rul_hours=predicted_rul_hours,
            )

        if predicted_rul_hours is None:
            return MaintenanceAssessment(
                status=MaintenanceStatus.NORMAL,
                severity="INFO",
                message="RUL prediction is not currently available.",
                recommended_action="Continue monitoring the machine.",
                predicted_rul_hours=None,
            )

        if (
            predicted_rul_hours <= self.CRITICAL_RUL_HOURS
        ):
            return MaintenanceAssessment(
                status=MaintenanceStatus.CRITICAL,
                severity="CRITICAL",
                message="Machine is approaching the end of its useful life.",
                recommended_action=(
                    "Stop operation when safe and perform maintenance immediately."
                ),
                predicted_rul_hours=predicted_rul_hours,
            )

        if (
            predicted_rul_hours <= self.REQUIRED_RUL_HOURS
            or health_state == "CRITICAL"
        ):
            return MaintenanceAssessment(
                status=MaintenanceStatus.REQUIRED,
                severity="HIGH",
                message="Maintenance is required soon.",
                recommended_action=(
                    "Schedule maintenance at the earliest available opportunity."
                ),
                predicted_rul_hours=predicted_rul_hours,
            )

        if (
            predicted_rul_hours <= self.DUE_SOON_RUL_HOURS
            or health_state == "DEGRADED"
        ):
            return MaintenanceAssessment(
                status=MaintenanceStatus.DUE_SOON,
                severity="WARNING",
                message="Machine degradation indicates upcoming maintenance.",
                recommended_action=(
                    "Plan maintenance during the next available maintenance window."
                ),
                predicted_rul_hours=predicted_rul_hours,
            )

        return MaintenanceAssessment(
            status=MaintenanceStatus.NORMAL,
            severity="INFO",
            message="Machine operating within expected conditions.",
            recommended_action="Continue normal operation.",
            predicted_rul_hours=predicted_rul_hours,
        )