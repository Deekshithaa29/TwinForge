
import time
from collections.abc import Callable
import threading
from app.configs.demo_config import DemoConfig
from app.twin.factory.factory import Factory
from app.twin.simulation.simulation_context import SimulationContext
from app.twin.machine.health import HealthState


class SimulationEngine:

    def __init__(
        self,
        factory: Factory,
        demo_config: DemoConfig | None = None,
    ):
        self.factory = factory
        self.tick = 0
        self.running = False
        self._stop_event = threading.Event()
        self._lifecycle_lock = threading.Lock()
        self._active = False
        self._stop_requested = False
        self.tick_rate = 1.0

        self.demo_config = demo_config or DemoConfig()

        self.tick_listeners: list[
            Callable[[SimulationContext], None]
        ] = []

    def add_tick_listener(
        self,
        listener: Callable[[SimulationContext], None],
    ) -> None:
        self.tick_listeners.append(listener)

    def _advance_simulation(self) -> float:
        """
        Advance factory state and return elapsed
        simulated time in seconds.
        """

        if not self.demo_config.enabled:
            self.factory.update(self.tick_rate)
            return self.tick_rate

        remaining = self.demo_config.simulated_seconds_per_tick

        while remaining > 0 and self.running:

            if self.all_machines_failed():
                break

            dt = min(
                self.demo_config.physics_step_seconds,
                remaining,
            )

            self.factory.update(dt)
            remaining -= dt

        return (
            self.demo_config.simulated_seconds_per_tick
            - remaining
        )

    def start(self, max_ticks: int | None = None):
        with self._lifecycle_lock:
            if self._active or self._stop_requested:
                return

            self._active = True
            self.running = True
            self._stop_event.clear()

        simulation_time = 0.0

        print("Simulation started.")

        try:
            while not self._stop_event.is_set():
                if max_ticks is not None and self.tick >= max_ticks:
                    break

                elapsed = self._advance_simulation()

                if self._stop_event.is_set():
                    break

                self.tick += 1
                simulation_time += elapsed

                context = SimulationContext(
                    tick=self.tick,
                    dt=elapsed,
                    simulation_time=simulation_time,
                )

                for listener in self.tick_listeners:
                    listener(context)

                print(
                    f"Tick: {self.tick}, "
                    f"Simulation Time: {simulation_time / 3600:.2f} hours"
                )

                if self.demo_config.enabled and self.all_machines_failed():
                    print("All machines have failed. Stopping simulation.")
                    break

                if self._stop_event.wait(self.tick_rate):
                    break

        finally:
            with self._lifecycle_lock:
                self._active = False
                self.running = False

    def all_machines_failed(self) -> bool:
        """
        Return True if every machine in the factory
        has reached the FAILED health state.
        """
        machines = self.factory.machines

        if not machines:
            return False
        
        return all(machine.health_state == HealthState.FAILED for machine in machines)

    def stop(self):
        with self._lifecycle_lock:
            self._stop_requested = True
            self.running = False
            self._stop_event.set()

        print("Simulation stopping...")
