from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.core.container import application


def test_fastapi_starts_and_stops_shared_application():
    with (
        patch.object(application, "start") as mock_start,
        patch.object(application, "stop") as mock_stop,
        patch.object(
            application.websocket_manager,
            "close_all",
            new_callable=AsyncMock,
        ) as mock_close_all,
    ):
        with TestClient(app):
            mock_start.assert_called_once()

        mock_stop.assert_called_once()
        mock_close_all.assert_awaited_once()