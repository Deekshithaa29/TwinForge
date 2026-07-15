from app.domains.factory.factory import Factory
from app.domains.machine.machine import Machine

factory = Factory(
    name="TwinForge Factory"
)

machine = Machine(
    name="CNC Spindle",
    machine_type="Spindle"
)

factory.add_machine(machine)

print(factory)