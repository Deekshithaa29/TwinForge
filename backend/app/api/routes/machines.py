from fastapi import APIRouter, Depends

from app.api.dependencies import get_application
from app.core.application import Application

router = APIRouter(
    prefix="/machines",
    tags=["Machines"],
)


@router.get("")
def get_machines(
    application: Application = Depends(get_application),
):
    return [
        {
            "id": machine.id,
            "name": machine.name,
            "type": machine.machine_type,
            "status": machine.status.name,
            "health": machine.health,
            "runtime_hours": machine.runtime_hours,
        }
        for machine in application.factory.machines
    ]