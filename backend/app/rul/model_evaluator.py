from __future__ import annotations

from math import sqrt

import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


class RULModelEvaluator:
    @staticmethod
    def evaluate(model, X, y) -> dict[str, float]:
        predictions = model.predict(X)

        mae = mean_absolute_error(y, predictions)
        rmse = sqrt(mean_squared_error(y, predictions))
        r2 = r2_score(y, predictions)

        return {
            "mae": float(mae),
            "rmse": float(rmse),
            "r2": float(r2),
        }

    @staticmethod
    def evaluate_per_run(
        model,
        X: pd.DataFrame,
        y: pd.Series,
        run_ids: pd.Series,
    ) -> pd.DataFrame:
        predictions = model.predict(X)

        results = pd.DataFrame(
            {
                "run_id": run_ids.to_numpy(),
                "actual": y.to_numpy(),
                "predicted": predictions,
            }
        )

        rows = []

        for run_id, group in results.groupby("run_id"):
            mae = mean_absolute_error(
                group["actual"],
                group["predicted"],
            )

            rmse = sqrt(
                mean_squared_error(
                    group["actual"],
                    group["predicted"],
                )
            )

            rows.append(
                {
                    "run_id": run_id,
                    "mae": float(mae),
                    "rmse": float(rmse),
                }
            )

        return pd.DataFrame(rows)