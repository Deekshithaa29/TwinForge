import pytest

from app.configs.demo_config import DemoConfig
from app.twin.factory.factory import Factory
from app.twin.simulation.simulation import SimulationEngine
from app.twin.machine.cnc_spindle import CNCSpindle


def test_normal_simulation():
    factory = Factory("Test Factory")

    machine = CNCSpindle("Test Spindle")
    factory.add_machine(machine)
    machine.start()

    engine = SimulationEngine(factory)

    engine.running = True
    elapsed = engine._advance_simulation()

    assert elapsed == pytest.approx(1.0)
    assert machine.runtime_hours == pytest.approx(1 / 3600)


def test_accelerated_simulation():
    factory = Factory("Demo Factory")

    machine = CNCSpindle("Demo Spindle")
    factory.add_machine(machine)
    machine.start()

    config = DemoConfig(
        enabled=True,
        physics_step_seconds=10.0,
        simulated_seconds_per_tick=3600.0,
    )

    engine = SimulationEngine(factory, config)

    engine.running = True
    elapsed = engine._advance_simulation()

    assert elapsed == pytest.approx(3600.0)
    assert machine.runtime_hours == pytest.approx(1.0)


def test_demo_disabled_by_default():
    engine = SimulationEngine(Factory("Test Factory"))

    assert engine.demo_config.enabled is False