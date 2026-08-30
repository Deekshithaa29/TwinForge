from app.degradation.lifecycle_record import LifecycleRecord
from app.twin.machine.health import HealthState
from app.twin.sensor.enums import SensorType


class RunToFailureSimulator:

    def __init__(
        self,
        machine,
        run_id: int,
        physics_dt: float = 10.0,
        sample_interval: float = 3600.0,
        max_samples: int = 100000,
    ):
        self.machine = machine
        self.run_id = run_id
        self.physics_dt = physics_dt
        self.sample_interval = sample_interval
        self.max_samples = max_samples

    def run(self) -> list[LifecycleRecord]:

        self.machine.start()

        records: list[LifecycleRecord] = []

        cycle = 1

        while (
            self.machine.health_state != HealthState.FAILED
            and cycle <= self.max_samples
        ):
            self._simulate_until_next_sample()

            temperature_sensor = self.machine.get_sensor_by_type(
                SensorType.TEMPERATURE
            )

            vibration_sensor = self.machine.get_sensor_by_type(
                SensorType.VIBRATION
            )

            record = LifecycleRecord(
                run_id=self.run_id,
                cycle=cycle,
                machine_id=self.machine.id,
                runtime_hours=self.machine.runtime_hours,
                temperature=(
                    temperature_sensor.value
                    if temperature_sensor
                    else None
                ),
                vibration=(
                    vibration_sensor.value
                    if vibration_sensor
                    else None
                ),
                rpm=self.machine.current_rpm,
                load=self.machine.load,
                health=self.machine.health,
                health_state=self.machine.health_state.value,
            )

            records.append(record)

            cycle += 1

        if self.machine.health_state != HealthState.FAILED:
            raise RuntimeError(
                "Run-to-failure simulation ended before machine failure."
            )

        self._assign_rul(records)

        return records

    def _simulate_until_next_sample(self) -> None:
        elapsed = 0.0

        while (
            elapsed < self.sample_interval
            and self.machine.health_state != HealthState.FAILED
        ):
            remaining_time = self.sample_interval - elapsed

            step = min(
                self.physics_dt,
                remaining_time,
            )

            self.machine.update(step)

            elapsed += step

    @staticmethod
    def _assign_rul(records: list[LifecycleRecord]) -> None:
        if not records:
            return

        failure_runtime = records[-1].runtime_hours

        for record in records:
            record.rul_hours = max(
                0.0,
                failure_runtime - record.runtime_hours,
            )