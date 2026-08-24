
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.machine.enums import MachineStatus
from app.twin.machine.health import HealthState

def test_failed_machine_stops():
    spindle = CNCSpindle("Test Spindle")

    spindle.start()
    spindle.health = 0

    spindle.update(1)

    assert spindle.status == MachineStatus.STOPPED
    assert spindle.health_state == HealthState.FAILED

def test_machine_health_state_healthy():
    spindle = CNCSpindle("Test Spindle")
    spindle.health = 90

    assert spindle.health_state == HealthState.HEALTHY

def test_machine_health_state_degraded():
    spindle = CNCSpindle("Test Spindle")
    spindle.health = 70

    assert spindle.health_state == HealthState.DEGRADED

def test_machine_health_state_critical():
    spindle = CNCSpindle("Test Spindle")
    spindle.health = 30

    assert spindle.health_state == HealthState.CRITICAL

def test_machine_health_state_failed():
    spindle = CNCSpindle("Test Spindle")
    spindle.health = 10

    assert spindle.health_state == HealthState.FAILED