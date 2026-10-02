import pandas as pd

from app.rul.dataset_splitter import RULDatasetSplitter
from app.rul.feature_engineering import (
    get_health_assisted_feature,
    get_sensor_feature,
    get_target_feature,
)
from app.rul.model_evaluator import RULModelEvaluator
from app.rul.model_trainer import RULModelTrainer


def print_metrics(name, metrics):
    print(f"\n{name}")
    print("-" * len(name))
    print(f"MAE:  {metrics['mae']:.2f} hours")
    print(f"RMSE: {metrics['rmse']:.2f} hours")
    print(f"R²:   {metrics['r2']:.4f}")


def main():
    dataframe = pd.read_csv("data/rul_dataset.csv")

    splitter = RULDatasetSplitter(seed=42)

    train_df, validation_df, _ = splitter.split(dataframe)

    y_train = get_target_feature(train_df)
    y_validation = get_target_feature(validation_df)

    # Sensor-only features
    X_train_sensor = get_sensor_feature(train_df)
    X_validation_sensor = get_sensor_feature(validation_df)

    # Health-assisted features
    X_train_health = get_health_assisted_feature(train_df)
    X_validation_health = get_health_assisted_feature(validation_df)

    # Baseline
    baseline = RULModelTrainer.train_baseline(
        X_train_sensor,
        y_train,
    )

    print_metrics(
        "Baseline",
        RULModelEvaluator.evaluate(
            baseline,
            X_validation_sensor,
            y_validation,
        ),
    )

    # Random Forest - Sensor only
    rf_sensor = RULModelTrainer.train_random_forest(
        X_train_sensor,
        y_train,
    )

    print_metrics(
        "Random Forest - Sensor Only",
        RULModelEvaluator.evaluate(
            rf_sensor,
            X_validation_sensor,
            y_validation,
        ),
    )

    # Random Forest - Health assisted
    rf_health = RULModelTrainer.train_random_forest(
        X_train_health,
        y_train,
    )

    print_metrics(
        "Random Forest - Health Assisted",
        RULModelEvaluator.evaluate(
            rf_health,
            X_validation_health,
            y_validation,
        ),
    )

    # Gradient Boosting - Sensor only
    gb_sensor = RULModelTrainer.train_gradient_boosting(
        X_train_sensor,
        y_train,
    )

    print_metrics(
        "Gradient Boosting - Sensor Only",
        RULModelEvaluator.evaluate(
            gb_sensor,
            X_validation_sensor,
            y_validation,
        ),
    )

    # Gradient Boosting - Health assisted
    gb_health = RULModelTrainer.train_gradient_boosting(
        X_train_health,
        y_train,
    )

    print_metrics(
        "Gradient Boosting - Health Assisted",
        RULModelEvaluator.evaluate(
            gb_health,
            X_validation_health,
            y_validation,
        ),
    )

    per_run = RULModelEvaluator.evaluate_per_run(
        rf_health,
        X_validation_health,
        y_validation,
        validation_df["run_id"],
    )

    print("\nHealth-Assisted Random Forest - Per Run")
    print("---------------------------------------")
    print(per_run.to_string(index=False))

    print("\nPer-Run Summary")
    print("----------------")
    print(per_run[["mae", "rmse"]].describe())


if __name__ == "__main__":
    main()