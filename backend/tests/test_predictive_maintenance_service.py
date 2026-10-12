import pytest

from app.maintenance.predictive_maintenance_service import (
    PredictiveMaintenanceService,
)
from app.maintenance.maintenance_status import MaintenanceStatus


@pytest.mark.parametrize(
    "health_state",
    ["FAILED", "Failed", "failed"],
)
def test_failed_machine_receives_failure_message(health_state):
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=0.0,
        health=19.99,
        health_state=health_state,
    )

    assert assessment.status == MaintenanceStatus.CRITICAL
    assert assessment.severity == "CRITICAL"
    assert "Machine failure detected" in assessment.message
    assert "Do not restart" in assessment.recommended_action

@pytest.mark.parametrize(
    "rul, expected_status",
    [
        (151.0, MaintenanceStatus.NORMAL),
        (150.0, MaintenanceStatus.DUE_SOON),
        (50.0, MaintenanceStatus.REQUIRED),
        (20.0, MaintenanceStatus.CRITICAL),
    ],
)
def test_maintenance_threshold_boundaries(rul, expected_status):
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=rul,
        health=100.0,
        health_state="HEALTHY",
    )

    assert assessment.status == expected_status


def test_failed_machine_without_rul_remains_critical():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=None,
        health=19.99,
        health_state="FAILED",
    )

    assert assessment.status == MaintenanceStatus.CRITICAL
    assert "Machine failure detected" in assessment.message


def test_approaching_failure_retains_existing_message():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=10.0,
        health=25.0,
        health_state="CRITICAL",
    )

    assert assessment.status == MaintenanceStatus.CRITICAL
    assert assessment.message == (
        "Machine is approaching the end of its useful life."
    )


def test_normal_machine():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=633.0,
        health=99.0,
        health_state="HEALTHY",
    )

    assert assessment.status == MaintenanceStatus.NORMAL
    assert assessment.severity == "INFO"


def test_maintenance_due_soon():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=100.0,
        health=70.0,
        health_state="HEALTHY",
    )

    assert assessment.status == MaintenanceStatus.DUE_SOON
    assert assessment.severity == "WARNING"


def test_maintenance_required():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=40.0,
        health=45.0,
        health_state="DEGRADED",
    )

    assert assessment.status == MaintenanceStatus.REQUIRED
    assert assessment.severity == "HIGH"


def test_critical_machine():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=10.0,
        health=18.0,
        health_state="CRITICAL",
    )

    assert assessment.status == MaintenanceStatus.CRITICAL
    assert assessment.severity == "CRITICAL"


def test_critical_health_overrides_high_rul():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=300.0,
        health=30.0,
        health_state="CRITICAL",
    )

    assert assessment.status == MaintenanceStatus.REQUIRED
    assert assessment.severity == "HIGH"

def test_failed_machine_is_critical():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=100.0,
        health=0.0,
        health_state="FAILED",
    )

    assert assessment.status == MaintenanceStatus.CRITICAL


def test_missing_rul_prediction():
    service = PredictiveMaintenanceService()

    assessment = service.evaluate(
        predicted_rul_hours=None,
        health=100.0,
        health_state="HEALTHY",
    )

    assert assessment.status == MaintenanceStatus.NORMAL
    assert assessment.predicted_rul_hours is None
    assert assessment.severity == "INFO"