from app.twin.factory.factory import Factory
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType
from app.twin.simulation.simulation import SimulationEngine
from app.twin.machine.enums import MachineStatus


def create_spindle():
    spindle = CNCSpindle("Main Spindle")

    temperature = Sensor(
        name="Temperature",
        sensor_type=SensorType.TEMPERATURE,
        unit="°C",
        min_value=0,
        max_value=150,
    )

    temperature.update(25)

    spindle.add_sensor(temperature)

    spindle.start()

    return spindle


def test_simulation_creation():
    factory = Factory("TwinForge Factory")

    spindle = create_spindle()

    factory.add_machine(spindle)

    simulation = SimulationEngine(factory)

    assert simulation.factory == factory


def test_factory_contains_machine():
    factory = Factory("TwinForge Factory")

    spindle = create_spindle()

    factory.add_machine(spindle)

    assert len(factory.machines) == 1
    assert factory.machines[0].name == "Main Spindle"


def test_machine_is_running():
    spindle = create_spindle()

    assert spindle.status == MachineStatus.RUNNING


def test_temperature_sensor_exists():
    spindle = create_spindle()

    sensor = spindle.get_sensor_by_type(SensorType.TEMPERATURE)

    assert sensor is not None
    assert sensor.read() == 25