from app.infrastructure.mqtt.publisher import Publisher
from app.twin.telemetry.telemetry import Telemetry


class ConsolePublisher(Publisher):

    def publish(self, telemetry: Telemetry):

        print()

        print("=" * 60)
        print("Publishing Telemetry")
        print("=" * 60)

        print(telemetry.to_dict())