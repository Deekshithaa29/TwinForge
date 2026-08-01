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

        for machine in self.factory.machines:

            temperature = machine.get_sensor_by_type(
                SensorType.TEMPERATURE
            )

            vibration = machine.get_sensor_by_type(
                SensorType.VIBRATION
            )

            print(machine.name)

            if temperature:
                print(f"Temperature : {temperature.read():.2f} °C")

            if vibration:
                print(f"Vibration : {vibration.read():.2f} units")

            print(f"Health : {machine.health:.4f}%")
            print(f"Runtime : {machine.runtime_hours:.6f} hrs")
            print(f"Load : {machine.load:.4f}")
            print(f"Current RPM : {machine.current_rpm:.2f} RPM")
            print("--------------------------")