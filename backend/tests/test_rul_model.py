import pandas as pd

from app.rul.model_evaluator import RULModelEvaluator
from app.rul.model_trainer import RULModelTrainer


def test_baseline_model_can_train_and_predict():

    X_train = pd.DataFrame(
        {
            "runtime_hours": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    y_train = pd.Series(
        [
            100.0,
            80.0,
            60.0,
        ]
    )

    model = (
        RULModelTrainer.train_baseline(
            X_train,
            y_train,
        )
    )

    predictions = model.predict(
        X_train
    )

    assert len(predictions) == 3


def test_model_evaluator_returns_metrics():

    X_train = pd.DataFrame(
        {
            "runtime_hours": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    y_train = pd.Series(
        [
            100.0,
            80.0,
            60.0,
        ]
    )

    model = (
        RULModelTrainer.train_baseline(
            X_train,
            y_train,
        )
    )

    metrics = RULModelEvaluator.evaluate(
        model,
        X_train,
        y_train,
    )

    assert "mae" in metrics
    assert "rmse" in metrics
    assert "r2" in metrics