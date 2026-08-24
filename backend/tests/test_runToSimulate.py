from app.degradation.run_to_failure import RunToFailureSimulator
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.machine.health import HealthState


def test_run_to_failure_reaches_failed_state():
    spindle = CNCSpindle("Test Spindle")

    simulator = RunToFailureSimulator(
        run_id=1,
        machine=spindle,
        dt=3600,
        max_steps=100000,
    )

    records = simulator.run()

    assert len(records) > 0
    assert spindle.health_state == HealthState.FAILED
    assert records[-1].rul_hours == 0.0
    assert records[0].rul_hours > records[-1].rul_hours

    for previous, current in zip(records, records[1:]):
        assert previous.rul_hours >= current.rul_hours