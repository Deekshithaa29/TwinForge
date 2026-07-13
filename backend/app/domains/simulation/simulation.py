import time

from app.domains.factory.factory import Factory


class SimulationEngine:

    def __init__(
        self,
        factory: Factory,
        tick_rate: float = 1.0
    ):
        self.factory = factory
        self.tick_rate = tick_rate
        self.current_tick = 0
        self.running = False

    def start(self):

        self.running = True

        while self.running:

            self.current_tick += 1

            print(f"\nTick {self.current_tick}")

            self.factory.update(self.tick_rate)

            time.sleep(self.tick_rate)

    def stop(self):

        self.running = False