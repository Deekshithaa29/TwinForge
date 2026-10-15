from app.configs.demo_config import DemoConfig
from app.twin.factory.factory import Factory
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.machine.health import HealthState
from app.twin.simulation.simulation import SimulationEngine
import threading


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


def test_stop_before_start_prevents_simulation():
    factory = Factory("Test Factory")
    engine = SimulationEngine(factory)

    engine.stop()
    engine.start(max_ticks=5)

    assert engine.tick == 0
    assert engine.running is False


def test_repeated_stop_is_safe():
    engine = SimulationEngine(Factory("Test Factory"))

    engine.stop()
    engine.stop()

    assert engine.running is False


def test_concurrent_start_does_not_duplicate_simulation():
    engine = SimulationEngine(Factory("Test Factory"))
    engine.tick_rate = 0.01

    entered = threading.Event()
    release = threading.Event()

    def blocking_listener(context):
        entered.set()
        release.wait(timeout=2)

    engine.add_tick_listener(blocking_listener)

    first = threading.Thread(target=engine.start)
    second = threading.Thread(target=engine.start)

    try:
        first.start()

        assert entered.wait(timeout=2)

        second.start()
        second.join(timeout=2)

        assert not second.is_alive()
        assert engine._active is True
    finally:
        engine.stop()
        release.set()
        first.join(timeout=2)
        second.join(timeout=2)

    assert not first.is_alive()
    assert engine.running is False


def test_stop_interrupts_simulation_wait():
    engine = SimulationEngine(Factory("Test Factory"))
    engine.tick_rate = 10.0

    first_tick = threading.Event()

    engine.add_tick_listener(
        lambda context: first_tick.set()
    )

    worker = threading.Thread(target=engine.start)

    try:
        worker.start()
        assert first_tick.wait(timeout=2)
    finally:
        engine.stop()
        worker.join(timeout=2)

    assert not worker.is_alive()
    assert engine.running is False
    