import pandas as pd

from app.rul.dataset_splitter import RULDatasetSplitter
from app.rul.feature_engineering import (
    get_health_assisted_feature,
    get_target_feature ,
)
from app.rul.model_evaluator import RULModelEvaluator
from app.rul.model_trainer import RULModelTrainer
from app.rul.model_persistence import RULModelPersistence


def main():
    dataframe = pd.read_csv(
        "data/rul_dataset.csv"
    )

    splitter = RULDatasetSplitter(seed=42)

    train_df, validation_df, test_df = (
        splitter.split(dataframe)
    )

    # Model selection is finished.
    # Retrain the selected model using train + validation data.
    final_training_df = pd.concat(
        [train_df, validation_df],
        ignore_index=True,
    )

    X_train = get_health_assisted_feature(
        final_training_df
    )
    y_train = get_target_feature(
        final_training_df
    )

    X_test = get_health_assisted_feature(
        test_df
    )
    y_test = get_target_feature(
        test_df
    )

    model = RULModelTrainer.train_random_forest(
        X_train,
        y_train,
    )

    RULModelPersistence.save(
        model,
        "models/rul_random_forest.joblib"
    )

    print("\nModel saved to "
    "models/rul_random_forest.joblib")

    metrics = RULModelEvaluator.evaluate(
        model,
        X_test,
        y_test,
    )

    print("Final RUL Model - Unseen Test Set")
    print("---------------------------------")
    print(
        f"Test machines: "
        f"{test_df['run_id'].nunique()}"
    )
    print(f"MAE:  {metrics['mae']:.2f} hours")
    print(f"RMSE: {metrics['rmse']:.2f} hours")
    print(f"R²:   {metrics['r2']:.4f}")

    per_run = RULModelEvaluator.evaluate_per_run(
        model,
        X_test,
        y_test,
        test_df["run_id"],
    )

    print("\nPer-Machine Test Results")
    print("------------------------")
    print(
        per_run.to_string(
            index=False
        )
    )

    print("\nPer-Machine Summary")
    print("-------------------")
    print(
        per_run[
            ["mae", "rmse"]
        ].describe()
    )


if __name__ == "__main__":
    main()