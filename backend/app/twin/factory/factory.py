from __future__ import annotations

from dataclasses import dataclass, field

from app.twin.machine.machine import Machine


@dataclass
class Factory:
    """
    Represents a virtual factory.
    """

    name: str

    machines: list[Machine] = field(default_factory=list)

    def add_machine(self, machine: Machine):

        self.machines.append(machine)

    def remove_machine(self, machine_id: str):

        self.machines = [
            m for m in self.machines
            if m.id != machine_id
        ]

    def update(self, dt: float):

        for machine in self.machines:

            machine.update(dt)