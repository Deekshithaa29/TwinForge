from app.twin.factory.factory import Factory
from app.twin.machine.machine import Machine


def test_factory_creation():
    factory = Factory("Factory-A")

    assert factory.name == "Factory-A"
    assert len(factory.machines) == 0


def test_add_machine():
    factory = Factory("Factory-A")

    machine = Machine(
        name="Spindle",
        machine_type="Spindle",
    )

    factory.add_machine(machine)

    assert len(factory.machines) == 1
    assert factory.machines[0].name == "Spindle"