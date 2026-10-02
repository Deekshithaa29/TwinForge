from __future__ import annotations

import pandas as pd

SENSOR_FEATURES = [
    "runtime_hours",
    "temperature",
    "vibration",
    "load",
]

HEALTH_ASSISTED_FEATURE = [
    "runtime_hours",
    "temperature",
    "vibration",
    "load",
    "health",
]
TARGET_COLUMN = "rul_hours"

def get_sensor_feature(
        dataframe: pd.DataFrame,
) -> pd.DataFrame:
    return dataframe[SENSOR_FEATURES].copy()

def get_health_assisted_feature(
        dataframe: pd.DataFrame,
) -> pd.DataFrame:
    return dataframe[HEALTH_ASSISTED_FEATURE].copy()

def get_target_feature(
        dataframe: pd.DataFrame,
) -> pd.DataFrame:
    return dataframe[TARGET_COLUMN].copy()