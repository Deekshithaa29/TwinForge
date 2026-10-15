from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.core.container import application


def test_websocket_receives_telemetry():
    manager = application.websocket_manager

    with (
        patch.object(application, "start"),
        patch.object(application, "stop"),
        TestClient(app) as client,
    ):
        with client.websocket_connect("/ws/telemetry") as websocket:

            assert len(manager.connections) == 1

            message = {
                "machine_id": "CNC-spindle-001",
                "health": 85.0,
                "predicted_rul_hours": 120.0,
            }

            # Broadcast from a simulated background thread.
            import threading

            worker = threading.Thread(
                target=manager.broadcast,
                args=(message,),
            )

            worker.start()
            worker.join(timeout=2)

            assert not worker.is_alive()

            received = websocket.receive_json()

            assert received == message

        assert len(manager.connections) == 0