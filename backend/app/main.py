from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.machines import router as machines_router
from app.api.routes.telemetry import router as telemetry_router
from app.api.routes.websocket import router as websocket_router
print("Websocket router:", websocket_router, flush=True)
from app.core.container import application


@asynccontextmanager
async def lifespan(app: FastAPI):
    application.start()

    yield

    application.stop()


app = FastAPI(
    title="TwinForge API",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(machines_router)
app.include_router(telemetry_router)
app.include_router(websocket_router)

