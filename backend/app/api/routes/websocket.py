from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import asyncio

from app.api.dependencies import get_application
from app.core.application import Application

router = APIRouter()

print("WEBSOCKET ROUTE FILE IMPORTED", flush=True)

@router.websocket("/ws/telemetry")
async def telemetry_socket(
    websocket: WebSocket,
    application: Application = Depends(get_application),
):
    print("Application:", id(application))
    print("WebSocketManager:", id(application.websocket_manager))
    manager = application.websocket_manager

    print("ROUTE MANAGER:", id(manager))
    
    await manager.connect(websocket)

    try:
        while True:
            # Keep the connection alive.
            await websocket.receive()

    except WebSocketDisconnect as e:
        print("WebSocket disconnected:", e)
        manager.disconnect(websocket)