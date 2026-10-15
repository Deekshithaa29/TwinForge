
import asyncio
import logging
import threading
from concurrent.futures import Future

from fastapi import WebSocket


logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages dashboard WebSocket clients.

    WebSocket operations run on FastAPI's event loop.
    Telemetry can be submitted from the simulation thread.
    """

    def __init__(self):
        self.connections: list[WebSocket] = []
        self.loop: asyncio.AbstractEventLoop | None = None
        self._lock = threading.RLock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

        current_loop = asyncio.get_running_loop()

        with self._lock:
            if self.loop is not current_loop:
                if self.connections:
                    logger.warning(
                        "WebSocket event loop changed; "
                        "discarding stale connections"
                    )
                    self.connections.clear()

                self.loop = current_loop

            if websocket not in self.connections:
                self.connections.append(websocket)

        logger.info("Dashboard WebSocket client connected")

    def disconnect(self, websocket: WebSocket) -> None:
        with self._lock:
            if websocket in self.connections:
                self.connections.remove(websocket)

    async def _broadcast(self, message: dict) -> None:
        with self._lock:
            connections = list(self.connections)

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                logger.exception(
                    "Failed to send telemetry to WebSocket client"
                )
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(websocket)

    @staticmethod
    def _handle_broadcast_result(future: Future) -> None:
        try:
            future.result()
        except Exception:
            logger.exception("WebSocket broadcast task failed")

    def broadcast(self, message: dict) -> None:
        """
        Schedule telemetry delivery from a background thread.

        Does not block the simulation thread.
        """
        with self._lock:
            loop = self.loop
            has_connections = bool(self.connections)

        if not has_connections or loop is None:
            return

        if loop.is_closed() or not loop.is_running():
            logger.warning(
                "WebSocket event loop is unavailable"
            )
            return

        try:
            future = asyncio.run_coroutine_threadsafe(
                self._broadcast(message),
                loop,
            )
        except RuntimeError:
            logger.exception(
                "Failed to schedule WebSocket broadcast"
            )
            return

        future.add_done_callback(
            self._handle_broadcast_result
        )

    async def close_all(self) -> None:
        """
        Close all connected dashboard clients.

        Call this from the FastAPI event loop during shutdown.
        """
        with self._lock:
            connections = list(self.connections)
            self.connections.clear()
            self.loop = None

        for websocket in connections:
            try:
                await websocket.close()
            except Exception:
                logger.exception(
                    "Failed to close WebSocket connection"
                )
