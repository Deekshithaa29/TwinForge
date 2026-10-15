
import logging
import threading

import paho.mqtt.client as mqtt

from app.infrastructure.mqtt.publisher import Publisher
from app.infrastructure.mqtt.serializer import TelemetrySerializer
from app.infrastructure.mqtt.topics import MACHINE_TELEMETRY
from app.twin.telemetry.telemetry import Telemetry


logger = logging.getLogger(__name__)


class MQTTPublisher(Publisher):
    """
    MQTT publisher with asynchronous connection,
    automatic reconnection and connection-state tracking.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 1883,
    ):
        self.host = host
        self.port = port

        self._connected = threading.Event()
        self._lifecycle_lock = threading.RLock()
        self._started = False

        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.reconnect_delay_set(
            min_delay=1,
            max_delay=30,
        )

    @property
    def is_connected(self) -> bool:
        return self._connected.is_set()

    def on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):
        if reason_code == 0:
            self._connected.set()
            logger.info("Connected to MQTT broker")
        else:
            self._connected.clear()
            logger.warning(
                "MQTT connection rejected: %s",
                reason_code,
            )

    def on_disconnect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):
        self._connected.clear()

        logger.warning(
            "Disconnected from MQTT broker: %s",
            reason_code,
        )

    def connect(self) -> None:
        """
        Start MQTT connection in the background.

        The broker does not need to be online at startup.
        """
        with self._lifecycle_lock:
            if self._started:
                return

            self.client.connect_async(
                self.host,
                self.port,
                keepalive=60,
            )

            result = self.client.loop_start()

            if result != mqtt.MQTT_ERR_SUCCESS:
                raise ConnectionError(
                    f"Failed to start MQTT network loop: {result}"
                )

            self._started = True

    def disconnect(self) -> None:
        """
        Shut down MQTT networking safely.
        """
        with self._lifecycle_lock:
            if not self._started:
                return

            self._started = False
            self._connected.clear()

            try:
                self.client.disconnect()
            finally:
                self.client.loop_stop()

    def publish(self, telemetry: Telemetry) -> None:
        """
        Publish live telemetry only when connected.

        Raises ConnectionError if MQTT is unavailable.
        TelemetryManager handles this exception.
        """
        if not self.is_connected:
            raise ConnectionError(
                "MQTT broker is not connected"
            )

        payload = TelemetrySerializer.to_json(telemetry)

        result = self.client.publish(
            MACHINE_TELEMETRY,
            payload,
            qos=0,
        )

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise ConnectionError(
                f"MQTT publish failed: {result.rc}"
            )
