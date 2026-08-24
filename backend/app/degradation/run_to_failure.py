from app.degradation.lifecycle_record import LifecycleRecord
from app.twin.machine.health import HealthState
from app.twin.sensor.enums import SensorType


class RunToFailureSimulator:

    def __init__(
        self,
        machine,
        run_id:int,
        dt: float = 60.0,
        max_steps: int = 100000,
    ):
        self.machine = machine
        self.run_id = run_id
        self.dt = dt
        self.max_steps = max_steps

    def run(self) -> list[LifecycleRecord]:

        self.machine.start()

        records: list[LifecycleRecord] = []

        cycle = 1

        while (
            self.machine.health_state != HealthState.FAILED
            and cycle < self.max_steps
        ):
            self.machine.update(self.dt)

            temperature_sensor = self.machine.get_sensor_by_type(
                SensorType.TEMPERATURE
            )

            vibration_sensor = self.machine.get_sensor_by_type(
                SensorType.VIBRATION
            )

            record = LifecycleRecord(
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
                run_id=self.run_id,
            )

            records.append(record)

            cycle += 1

        if self.machine.health_state != HealthState.FAILED:
            raise RuntimeError(
                "Run-to-failure simulation ended before machine failure."
            )
        
        self._assign_rul(records)

        return records

    @staticmethod
    def _assign_rul(records: list[LifecycleRecord]) -> None:
        if not records:
            return

        failure_runtime = records[-1].runtime_hours

        for record in records:
            record.rul_hours = max(0.0, failure_runtime - record.runtime_hours)