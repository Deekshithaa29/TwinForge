import pandas as pd

from app.rul.model_trainer import RULModelTrainer
from app.rul.predictor import RULPredictor


def test_rul_predictor_returns_float():

    X = pd.DataFrame(
        {
            "runtime_hours": [10, 20, 30, 40],
            "temperature": [27, 28, 29, 30],
            "vibration": [1, 2, 3, 4],
            "load": [0.3, 0.4, 0.5, 0.6],
            "health": [95, 85, 75, 65],
        }
    )

    y = pd.Series(
        [400, 300, 200, 100]
    )

    model = (
        RULModelTrainer.train_random_forest(
            X,
            y,
            n_estimators=10,
        )
    )

    predictor = RULPredictor(model)

    prediction = predictor.predict(
        runtime_hours=25,
        temperature=28.5,
        vibration=2.5,
        load=0.45,
        health=80,
    )

    assert isinstance(prediction, float)
    assert prediction >= 0

def test_model_can_be_saved_and_loaded(tmp_path):

    from app.rul.model_persistence import (
        RULModelPersistence,
    )

    X = pd.DataFrame(
        {
            "runtime_hours": [10, 20],
            "temperature": [27, 29],
            "vibration": [1, 3],
            "load": [0.3, 0.6],
            "health": [95, 70],
        }
    )

    y = pd.Series([300, 100])

    model = (
        RULModelTrainer.train_random_forest(
            X,
            y,
            n_estimators=10,
        )
    )

    path = tmp_path / "model.joblib"

    RULModelPersistence.save(
        model,
        path,
    )

    loaded_model = (
        RULModelPersistence.load(path)
    )

    assert loaded_model is not None