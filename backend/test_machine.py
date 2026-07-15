from app.domains.machine.machine import Machine

machine = Machine (
    name = "CNC Spindle",
    machine_type = "Spindle"
)

print(machine)

machine.start()

machine.update(10)  

print(f"Machine status: {machine.status}, Runtime hours: {machine.runtime_hours}")