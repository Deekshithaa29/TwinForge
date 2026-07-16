from enum import Enum


class MachineStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    MAINTENANCE = "maintenance"
    FAULT = "fault"
    STOPPED = "stopped"
