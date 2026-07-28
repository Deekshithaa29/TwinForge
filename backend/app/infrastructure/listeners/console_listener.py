from app.twin.factory.factory import Factory
from app.twin.sensor.enums import SensorType
from app.twin.simulation.simulation_context import SimulationContext


class ConsoleTelemetryListener:
    """
    Prints machine telemetry after every simulation tick.
    """

    def __init__(self, factory: Factory):
        self.factory = factory

    def __call__(self, context: SimulationContext) -> None:

        print(f"\nTick : {context.tick}")

        for machine in self.factory.machines:

            temperature = machine.get_sensor_by_type(
                SensorType.TEMPERATURE
            )

            print(machine.name)

            if temperature:
                print(f"Temperature : {temperature.read():.2f} °C")

            print(f"Health : {machine.health:.4f}%")
            print(f"Runtime : {machine.runtime_hours:.6f} hrs")
            print("--------------------------")