from enum import Enum


class MaintenanceStatus(str, Enum):
    NORMAL = "NORMAL"
    DUE_SOON = "DUE_SOON"
    REQUIRED = "REQUIRED"
    CRITICAL = "CRITICAL"