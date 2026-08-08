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
from app.infrastructure.repository.memory_repository import InMemoryTelemetryRepository
from app.infrastructure.database.database import SQLiteDatabase
from app.infrastructure.database.schema import create_schema

from app.infrastructure.repository.sqlite_repository import (
    SQLiteTelemetryRepository,
)
import threading


class Application:

    def __init__(self):
        self.factory = Factory("TwinForge Factory")
        self.simulation = SimulationEngine(self.factory)
        self.publisher = MQTTPublisher()
        self.websocket_manager = WebSocketManager()
        self.database = SQLiteDatabase()
        create_schema(self.database)
        self.telemetry_repository = SQLiteTelemetryRepository(self.database)
        self.telemetry_manager = TelemetryManager(
            self.factory,
            self.telemetry_repository,
            self.publisher,
            self.websocket_manager,
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

        spindle = CNCSpindle("Main Spindle")

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
        """

        self.simulation_thread = threading.Thread(
            target=self.simulation.start,
            kwargs={"max_ticks": None},
            daemon=True,
        )

        self.simulation_thread.start()

    def _stop_simulation(self) -> None:
        """
        Stops the simulation thread gracefully.
        """

        self.simulation.stop()

        if self.simulation_thread is not None:
            self.simulation_thread.join(timeout=2)  

    def start(self):
        self.publisher.connect()

        self._start_simulation()

        print("TwinForge started.")

    def stop(self):
        self._stop_simulation()
        
        self.publisher.disconnect()

        self.database.close()

        print("TwinForge stopped.")