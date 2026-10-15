from unittest.mock import Mock

from app.twin.telemetry.telemetry_manager import TelemetryManager


def test_mqtt_failure_does_not_block_websocket():
    factory = Mock()
    factory.machines = [Mock()]

    repository = Mock()
    publisher = Mock()
    websocket_manager = Mock()

    publisher.publish.side_effect = ConnectionError(
        "MQTT broker unavailable"
    )

    manager = TelemetryManager(
        factory=factory,
        telemetry_repository=repository,
        publisher=publisher,
        websocket_manager=websocket_manager,
    )

    from unittest.mock import patch

    with patch(
        "app.twin.telemetry.telemetry_manager.TelemetryService.create_snapshot"
    ) as create_snapshot:
        snapshot = Mock()
        snapshot.machine_id = "M1"
        snapshot.to_dict.return_value = {"machine_id": "M1"}
        create_snapshot.return_value = snapshot

        manager.collect()

    repository.save.assert_called_once_with(snapshot)
    publisher.publish.assert_called_once_with(snapshot)
    websocket_manager.broadcast.assert_called_once_with(
        {"machine_id": "M1"}
    )


def test_websocket_failure_does_not_crash_collection():
    factory = Mock()
    factory.machines = [Mock()]

    websocket_manager = Mock()
    websocket_manager.broadcast.side_effect = RuntimeError(
        "WebSocket disconnected"
    )

    manager = TelemetryManager(
        factory=factory,
        websocket_manager=websocket_manager,
    )

    from unittest.mock import patch

    with patch(
        "app.twin.telemetry.telemetry_manager.TelemetryService.create_snapshot"
    ) as create_snapshot:
        create_snapshot.return_value = Mock(
            machine_id="M1"
        )

        manager.collect()

    websocket_manager.broadcast.assert_called_once()


def test_database_failure_is_not_silenced():
    factory = Mock()
    factory.machines = [Mock()]

    repository = Mock()
    publisher = Mock()

    repository.save.side_effect = RuntimeError(
        "Database write failed"
    )

    manager = TelemetryManager(
        factory=factory,
        telemetry_repository=repository,
        publisher=publisher,
    )

    from unittest.mock import patch
    import pytest

    with patch(
        "app.twin.telemetry.telemetry_manager.TelemetryService.create_snapshot"
    ) as create_snapshot:
        create_snapshot.return_value = Mock(machine_id="M1")

        with pytest.raises(
            RuntimeError,
            match="Database write failed",
        ):
            manager.collect()

    publisher.publish.assert_not_called()