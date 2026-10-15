
import asyncio
from unittest.mock import AsyncMock, Mock

import pytest

from app.infrastructure.websocket.manager import WebSocketManager

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_connection_registration():
    manager = WebSocketManager()
    websocket = Mock()
    websocket.accept = AsyncMock()

    await manager.connect(websocket)
    await manager.connect(websocket)

    assert len(manager.connections) == 1
    websocket.accept.assert_awaited()
    manager.disconnect(websocket)

    assert manager.connections == []


@pytest.mark.anyio
async def test_failed_client_is_removed():
    manager = WebSocketManager()

    good_client = Mock()
    good_client.accept = AsyncMock()
    good_client.send_json = AsyncMock()

    bad_client = Mock()
    bad_client.accept = AsyncMock()
    bad_client.send_json = AsyncMock(
        side_effect=RuntimeError("Disconnected")
    )

    await manager.connect(good_client)
    await manager.connect(bad_client)

    await manager._broadcast({"health": 85})

    good_client.send_json.assert_awaited_once_with(
        {"health": 85}
    )

    assert good_client in manager.connections
    assert bad_client not in manager.connections


@pytest.mark.anyio
async def test_close_all_removes_connections():
    manager = WebSocketManager()

    websocket = Mock()
    websocket.accept = AsyncMock()
    websocket.close = AsyncMock()

    await manager.connect(websocket)
    await manager.close_all()

    websocket.close.assert_awaited_once()
    assert manager.connections == []
    assert manager.loop is None


def test_broadcast_without_clients_is_safe():
    manager = WebSocketManager()

    manager.broadcast({"health": 85})

    assert manager.connections == []
