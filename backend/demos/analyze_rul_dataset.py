from pathlib import Path

import pandas as pd


DATASET_PATH = Path("data/rul_dataset.csv")


def main():
    df = pd.read_csv(DATASET_PATH)

    print("\n=== Dataset Shape ===")
    print(df.shape)

    print("\n=== Columns ===")
    print(df.columns.tolist())

    print("\n=== Number of Runs ===")
    print(df["run_id"].nunique())

    print("\n=== Records Per Run ===")
    print(
        df.groupby("run_id")
        .size()
        .describe()
    )

    print("\n=== Feature Summary ===")
    feature_columns = [
        "runtime_hours",
        "temperature",
        "vibration",
        "rpm",
        "load",
        "health",
        "rul_hours",
    ]

    print(df[feature_columns].describe())

    print("\n=== Final RUL Per Run ===")
    final_rows = (
        df.sort_values(["run_id", "cycle"])
        .groupby("run_id")
        .tail(1)
    )

    print(
        final_rows[
            [
                "run_id",
                "health",
                "health_state",
                "rul_hours",
            ]
        ]
    )

    print("\n=== Runs Ending At RUL = 0 ===")
    print(
        (
            final_rows["rul_hours"] == 0
        ).value_counts()
    )

    print("\n=== Health State Distribution ===")
    print(df["health_state"].value_counts())

    print("\n=== Missing Values ===")
    print(df.isnull().sum())

    print("\n=== Numeric Correlation With RUL ===")

    numeric_columns = [
        "runtime_hours",
        "temperature",
        "vibration",
        "rpm",
        "load",
        "health",
        "rul_hours",
    ]

    correlation = (
        df[numeric_columns]
        .corr()["rul_hours"]
        .sort_values(ascending=False)
    )

    print(correlation)


if __name__ == "__main__":
    main()