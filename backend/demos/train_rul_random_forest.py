import pandas as pd

from app.rul.dataset_splitter import RULDatasetSplitter
from app.rul.feature_engineering import (
    get_sensor_feature,
    get_target_feature,
)
from app.rul.model_evaluator import RULModelEvaluator
from app.rul.model_trainer import RULModelTrainer


def main():
    dataframe = pd.read_csv(
        "data/rul_dataset.csv"
    )

    splitter = RULDatasetSplitter(
        seed=42
    )

    train_df, validation_df, test_df = (
        splitter.split(dataframe)
    )

    X_train = get_sensor_feature(
        train_df
    )
    y_train = get_target_feature(
        train_df
    )

    X_validation = get_sensor_feature(
        validation_df
    )
    y_validation = get_target_feature(
        validation_df
    )

    model = RULModelTrainer.train_random_forest(
        X_train,
        y_train,
    )

    metrics = RULModelEvaluator.evaluate(
        model,
        X_validation,
        y_validation,
    )

    print("Random Forest RUL Model")
    print("-----------------------")
    print(f"MAE:  {metrics['mae']:.2f} hours")
    print(f"RMSE: {metrics['rmse']:.2f} hours")
    print(f"R²:   {metrics['r2']:.4f}")


if __name__ == "__main__":
    main()