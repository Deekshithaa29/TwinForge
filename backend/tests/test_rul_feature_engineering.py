import pandas as pd

from app.rul.feature_engineering import (
    get_health_assisted_feature,
    get_sensor_feature,
    get_target_feature,
)


def test_sensor_features():

    dataframe = pd.DataFrame(
        {
            "runtime_hours": [1.0],
            "temperature": [29.0],
            "vibration": [3.0],
            "load": [0.5],
            "health": [95.0],
            "rul_hours": [300.0],
        }
    )

    features = get_sensor_feature(dataframe)

    assert list(features.columns) == [
        "runtime_hours",
        "temperature",
        "vibration",
        "load",
    ]


def test_health_assisted_features():

    dataframe = pd.DataFrame(
        {
            "runtime_hours": [1.0],
            "temperature": [29.0],
            "vibration": [3.0],
            "load": [0.5],
            "health": [95.0],
            "rul_hours": [300.0],
        }
    )

    features = get_health_assisted_feature(
        dataframe
    )

    assert "health" in features.columns


def test_target():

    dataframe = pd.DataFrame(
        {
            "rul_hours": [100.0, 50.0],
        }
    )

    target = get_target_feature(dataframe)

    assert target.tolist() == [
        100.0,
        50.0,
    ]