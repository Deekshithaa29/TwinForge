from app.twin.factory.factory import Factory
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.simulation.simulation import SimulationEngine


def test_all_machines_failed():
    factory = Factory("Test Factory")

    spindle = CNCSpindle("Test Spindle")
    spindle.health = 0.0

    factory.add_machine(spindle)

    engine = SimulationEngine(factory)

    assert engine.all_machines_failed() is True


def test_healthy_machine_not_failed():
    factory = Factory("Test Factory")

    spindle = CNCSpindle("Test Spindle")
    factory.add_machine(spindle)

    engine = SimulationEngine(factory)

    assert engine.all_machines_failed() is False