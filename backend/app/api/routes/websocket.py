import logging

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)

from app.api.dependencies import get_application
from app.core.application import Application


logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/telemetry")
async def telemetry_socket(
    websocket: WebSocket,
    application: Application = Depends(get_application),
):
    manager = application.websocket_manager

    try:
        await manager.connect(websocket)

        logger.info("Dashboard WebSocket connected")

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        logger.info("Dashboard WebSocket disconnected")

    finally:
        manager.disconnect(websocket)
        logger.info("Dashboard WebSocket cleaned up")