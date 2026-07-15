import time

from app.twin.factory.factory import Factory
from app.twin.sensor.enums import SensorType

class SimulationEngine:

    def __init__(self, factory: Factory):

        self.factory = factory

        self.tick = 0

        self.running = False

        self.tick_rate = 1.0

    def start(self, max_ticks: int | None = None):

        self.running = True

        print("Simulation Started\n")

        while self.running:

            if max_ticks is not None and self.tick >= max_ticks:
                self.stop()
                break

            self.tick += 1

            self.factory.update(self.tick_rate)

            print(f"Tick : {self.tick}")

            for machine in self.factory.machines:

                temperature = machine.get_sensor_by_type(SensorType.TEMPERATURE)

                if temperature:

                    print(
                        f"{machine.name}"
                    )

                    print(
                        f"Temperature : {temperature.read():.2f} °C"
                    )

                    print(
                        f"Health : {machine.health:.4f}%"
                    )

                    print(
                        f"Runtime : {machine.runtime_hours:.6f} hrs"
                    )

                    print("--------------------------")

            time.sleep(self.tick_rate)

    def stop(self):

        self.running = False