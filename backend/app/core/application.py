from app.infrastructure.listeners.mqtt_listener import MQTTTelemetryListener
from app.infrastructure.listeners.console_listener import ConsoleTelemetryListener
from app.twin.factory.factory import Factory
from app.twin.simulation.simulation import SimulationEngine
from app.twin.machine.cnc_spindle import CNCSpindle
from app.twin.sensor.sensor import Sensor
from app.twin.sensor.enums import SensorType
from app.infrastructure.mqtt.mqtt_publisher import MQTTPublisher
from app.twin.telemetry.telemetry_manager import TelemetryManager
from app.infrastructure.websocket.manager import WebSocketManager
from app.infrastructure.database.database import SQLiteDatabase
from app.infrastructure.database.schema import create_schema
from app.rul.model_persistence import RULModelPersistence
from app.rul.predictor import RULPredictor
from app.maintenance.predictive_maintenance_service import PredictiveMaintenanceService
from app.configs.demo_config import DemoConfig

from app.infrastructure.repository.sqlite_repository import (
    SQLiteTelemetryRepository,
)
import threading
from pathlib import Path


class Application:

    def __init__(self):
        self.factory = Factory("TwinForge Factory")
        self.demo_config = DemoConfig(enabled=True, physics_step_seconds=10.0, simulated_seconds_per_tick=3600.0, degradation_rate=0.5)
        self.simulation = SimulationEngine(self.factory, self.demo_config)
        self.publisher = MQTTPublisher()
        self.websocket_manager = WebSocketManager()
        self.database = SQLiteDatabase()
        create_schema(self.database)
        self.telemetry_repository = SQLiteTelemetryRepository(self.database)

        self.lifecycle_lock = threading.RLock()
        self.started = False
        self.closed = False

        backend_root = Path(__file__).resolve().parents[2]

        model_path = (
            backend_root
            / "models"
            / "rul_random_forest.joblib"
        )
        
        self.rul_model = RULModelPersistence.load(
            model_path
        )      
        self.rul_predictor = RULPredictor(self.rul_model)
        self.maintenance_service = PredictiveMaintenanceService()

        self.telemetry_manager = TelemetryManager(
            factory=self.factory,
            telemetry_repository=self.telemetry_repository,
            publisher=self.publisher,
            websocket_manager=self.websocket_manager,
            rul_predictor=self.rul_predictor,
            maintenance_service=self.maintenance_service,
        )

        mqtt_listener = MQTTTelemetryListener(
            self.telemetry_manager,
        )

        console_listener = ConsoleTelemetryListener(
            self.factory,
        )

        print("Application:", id(self))
        print("WebSocketManager:", id(self.websocket_manager))
        print("TelemetryManager:", id(self.telemetry_manager))

        self.simulation.add_tick_listener(mqtt_listener)
        self.simulation.add_tick_listener(console_listener)

        self.simulation_thread: threading.Thread | None = None

        self._create_default_factory()

    def _create_default_factory(self):

        spindle = CNCSpindle("Main Spindle", machine_id="CNC-spindle-001")

        if self.demo_config.enabled:
            spindle.degradation_model.base_degradation_rate = self.demo_config.degradation_rate

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


        temperature.update(25)
        vibration.update(0.50)

        spindle.add_sensor(temperature)
        spindle.add_sensor(vibration)

        spindle.start()

        self.factory.add_machine(spindle)

    def _start_simulation(self) -> None:
        """
        Starts the simulation in a background thread.
        Prevent concurrent starts using a lock to ensure thread safety.
        """
        with self.lifecycle_lock:
            if self.closed:
                raise RuntimeError("Cannot start a closed application.")
            if( 
                self.simulation_thread is not None and self.simulation_thread.is_alive()
            ):
                return  # Simulation is already running
            self.simulation_thread = threading.Thread(
                target=self.simulation.start,
                kwargs={"max_ticks": None},
                daemon=True,
                name="TwinForgeSimulation",
            )

            self.simulation_thread.start()

    def _stop_simulation(self) -> None:
        """
        Stop the simulation and wait for its worker to exit.
        """
        with self.lifecycle_lock:
            self.simulation.stop()

            thread = self.simulation_thread

            if thread is not None and thread.is_alive():
                if thread is threading.current_thread():
                    # If the current thread is the simulation thread, we cannot join it.
                    raise RuntimeError("Simulation thread cannot join itself.")
                thread.join()  
            self.simulation_thread = None


    def start(self):
        with self.lifecycle_lock:
            if self.closed:
                raise RuntimeError("Cannot restart an application after shutdown.")
            if self.started:
                return  # Already started

            self.publisher.connect()

            try:
                self._start_simulation()
            except Exception as e:
                self.publisher.disconnect()
                raise e

            self.started = True
            print("TwinForge started.")

    def stop(self) -> None:
        with self.lifecycle_lock:
            if self.closed:
                return  # Already closed

            self._stop_simulation()

            try:
                self.publisher.disconnect()
            finally:
                self.database.close()
                self.closed = True
                self.started = False

            print("TwinForge stopped.")