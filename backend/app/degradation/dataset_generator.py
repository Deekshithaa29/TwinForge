import random

from app.degradation.run_to_failure import RunToFailureSimulator
from app.degradation.spindle_degradation import SpindleDegradationModel
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.enums import SensorType
from app.twin.sensor.sensor import Sensor


class RULDatasetGenerator:
    """
    Generates multiple run-to-failure lifecycles
    for RUL model training.
    """

    def __init__(
        self,
        number_of_runs: int = 10,
        physics_dt: float = 10.0,
        sample_interval: float = 3600.0
    ):
        self.number_of_runs = number_of_runs
        self.physics_dt = physics_dt
        self.sample_interval = sample_interval

    def generate(self):
        all_records = []

        for run_id in range(1, self.number_of_runs + 1):

            spindle = CNCSpindle(
                name=f"Training Spindle {run_id}",
                machine_id=f"TRAIN-SPINDLE-{run_id:03d}",
            )

            temperature = Sensor(
                name="Temperature",
                sensor_type=SensorType.TEMPERATURE,
                unit="°C",
                min_value=0,
                max_value=150,
            )

            vibration = Sensor(
                name="Vibration",
                sensor_type=SensorType.VIBRATION,
                unit="mm/s",
                min_value=0,
                max_value=50,
            )

            temperature.update(25.0)
            vibration.update(0.5)

            spindle.add_sensor(temperature)
            spindle.add_sensor(vibration)

            spindle.degradation_model = SpindleDegradationModel(
                base_degradation_rate=random.uniform(
                    0.3,
                    0.8,
                )
            )

            spindle.physics_model.heating_rate = random.uniform( 0.12, 0.18,)
            spindle.physics_model.cooling_rate = random.uniform( 0.018, 0.025)
            
            simulator = RunToFailureSimulator(
                run_id=run_id,
                machine=spindle,
                physics_dt=self.physics_dt,
                sample_interval=self.sample_interval,
            )

            records = simulator.run()

            all_records.extend(records)

        return all_records