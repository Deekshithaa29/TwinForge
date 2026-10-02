from app.rul.model_persistence import RULModelPersistence
from app.rul.predictor import RULPredictor


def main():
    model = RULModelPersistence.load(
        "models/rul_random_forest.joblib"
    )

    predictor = RULPredictor(model)

    predicted_rul = predictor.predict(
        runtime_hours=200.0,
        temperature=29.0,
        vibration=4.5,
        load=0.60,
        health=60.0,
    )

    print(
        f"Predicted RUL: "
        f"{predicted_rul:.2f} hours"
    )


if __name__ == "__main__":
    main()