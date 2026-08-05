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
    print("data is being printed from the get_latest_telemetry route telemetry.py")
    latest = application.telemetry_manager.get_latest()

    if not latest:
        return {}

    snapshot = next(iter(latest.values()))

    return snapshot.to_dict()