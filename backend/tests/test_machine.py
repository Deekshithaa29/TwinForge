from app.twin.machine.machine import Machine


def test_machine_creation():
    machine = Machine(
        name="CNC Spindle",
        machine_type="Spindle",
    )

    assert machine.name == "CNC Spindle"
    assert machine.machine_type == "Spindle"


def test_machine_has_no_sensors_initially():
    machine = Machine(
        name="Machine-1",
        machine_type="Motor",
    )

    assert len(machine.sensors) == 0