import time
from collections.abc import Callable

from app.twin.factory.factory import Factory
from app.twin.simulation.simulation_context import SimulationContext


class SimulationEngine:

    def __init__(self, factory: Factory):

        self.factory = factory

        self.tick = 0

        self.running = False

        self.tick_rate = 1.0

        self.tick_listeners: list[Callable[[SimulationContext], None]] = []

    def add_tick_listener(
    self,
    listener: Callable[[SimulationContext], None],
    ) -> None:
        """
        Register a callback that is invoked after every simulation tick.
        """
        self.tick_listeners.append(listener)

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

            context = SimulationContext(
                tick=self.tick,
                dt=self.tick_rate,
                simulation_time=self.tick * self.tick_rate,
            )

            for listener in self.tick_listeners:
                listener(context)

            time.sleep(self.tick_rate)

    def stop(self):

        self.running = False
