import asyncio

from fastapi import WebSocket


class WebSocketManager:
    """
    Manages all connected dashboard clients.
    """

    def __init__(self):
        self.connections: list[WebSocket] = []
        self.loop: asyncio.AbstractEventLoop | None = None

    async def connect(self, websocket: WebSocket):

        print(f"CONNECT Manager: {id(self)}")
        await websocket.accept()

        current_loop = asyncio.get_running_loop()
        print(f"Current event loop: {current_loop}")
        # Remember FastAPI's event loop
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        self.connections.append(websocket)
        print(f"New client connected. Total clients: {len(self.connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def _broadcast(self, message: dict):
        disconnected = []

        print(f"Connected clients: {len(self.connections)}")
        for websocket in self.connections:
            try:
                print(f"Sending message to client {websocket.client}: {message}")
                await websocket.send_json(message)
            except Exception as e:
                print(f"Failed to send message to client {websocket.client}: {e}")
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(websocket)

    def broadcast(self, message: dict):
        """
        Thread-safe broadcast.
        Can be called from the simulation thread.
        """
        print("Broadcasting message to dashboard clients:", message)
        print("BROADCAST MANAGER:", id(self))
        print("Connections:", len(self.connections))
        print(f"Stored loop: {self.loop}")
        if self.loop is None:
            return

        future = asyncio.run_coroutine_threadsafe(
            self._broadcast(message),
            self.loop,
        )

        print("Broadcast future:", future)