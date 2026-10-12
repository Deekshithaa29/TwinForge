from app.configs.demo_config import DemoConfig
from app.twin.factory.factory import Factory
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.machine.health import HealthState
from app.twin.simulation.simulation import SimulationEngine


def test_simulation_stops_after_failure_and_notifies_listener(
    monkeypatch,
):
    factory = Factory("Lifecycle Test Factory")

    spindle = CNCSpindle("Test Spindle")
    spindle.health = 0.01
    spindle.degradation_model.base_degradation_rate = 100.0
    spindle.start()

    factory.add_machine(spindle)

    engine = SimulationEngine(
        factory=factory,
        demo_config=DemoConfig(
            enabled=True,
            physics_step_seconds=10.0,
            simulated_seconds_per_tick=3600.0,
        ),
    )

    received_states = []

    def capture_telemetry(context):
        received_states.append(
            {
                "tick": context.tick,
                "health": spindle.health,
                "health_state": spindle.health_state,
            }
        )

    engine.add_tick_listener(capture_telemetry)

    monkeypatch.setattr(
        "app.twin.simulation.simulation.time.sleep",
        lambda _: None,
    )

    engine.start(max_ticks=5)

    assert spindle.health_state == HealthState.FAILED
    assert engine.running is False
    assert engine.tick == 1

    assert len(received_states) == 1
    assert received_states[0]["health_state"] == HealthState.FAILED
    