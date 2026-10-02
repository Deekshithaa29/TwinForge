from __future__ import annotations

import pandas as pd


class RULPredictor:
    FEATURE_COLUMNS = [
        "runtime_hours",
        "temperature",
        "vibration",
        "load",
        "health",
    ]

    def __init__(self, model):
        self.model = model

    def predict(
        self,
        runtime_hours: float,
        temperature: float,
        vibration: float,
        load: float,
        health: float,
    ) -> float:

        features = pd.DataFrame(
            [
                {
                    "runtime_hours": runtime_hours,
                    "temperature": temperature,
                    "vibration": vibration,
                    "load": load,
                    "health": health,
                }
            ],
            columns=self.FEATURE_COLUMNS,
        )

        prediction = self.model.predict(
            features
        )[0]

        return max(
            0.0,
            float(prediction),
        )