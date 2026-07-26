import paho.mqtt.client as mqtt

from app.infrastructure.mqtt.publisher import Publisher
from app.infrastructure.mqtt.serializer import TelemetrySerializer
from app.infrastructure.mqtt.topics import MACHINE_TELEMETRY
from app.twin.telemetry.telemetry import Telemetry


class MQTTPublisher(Publisher):
    """
    Publishes telemetry to an MQTT broker.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 1883,
    ):
        self.host = host
        self.port = port

        self.client = mqtt.Client()

    def connect(self) -> None:
        """
        Connect to the MQTT broker.
        """

        self.client.connect(
            self.host,
            self.port,
        )

    def disconnect(self) -> None:
        """
        Disconnect from the MQTT broker.
        """

        self.client.disconnect()

    def publish(
        self,
        telemetry: Telemetry,
    ) -> None:

        payload = TelemetrySerializer.to_json(
            telemetry
        )

        self.client.publish(
            MACHINE_TELEMETRY,
            payload,
        )