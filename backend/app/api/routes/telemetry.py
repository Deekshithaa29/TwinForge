from fastapi import APIRouter, Depends

from app.api.dependencies import get_application
from app.core.application import Application

router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"],
)


@router.get("/latest")
def get_latest_telemetry(
    application: Application = Depends(get_application),
):
    print(id(application.telemetry_manager))
    print(application.telemetry_manager.get_latest())
    latest = application.telemetry_manager.get_latest()

    return [
        snapshot.to_dict()
        for snapshot in latest.values()
    ]