from app.domains.factory.factory import Factory
from app.domains.machine.machine import Machine
from app.domains.simulation.simulation import SimulationEngine

factory = Factory(
    name="TwinForge Factory"
)

machine = Machine(
    name="CNC Spindle",
    machine_type="Spindle"
)

machine.start()

factory.add_machine(machine)

simulation = SimulationEngine(factory)

simulation.start()