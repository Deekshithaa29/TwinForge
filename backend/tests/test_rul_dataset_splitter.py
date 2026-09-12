import pandas as pd

from app.rul.dataset_splitter import RULDatasetSplitter


def create_test_dataframe():
    rows = []

    for run_id in range(1, 101):
        for cycle in range(3):
            rows.append(
                {
                    "run_id": run_id,
                    "cycle": cycle,
                    "rul_hours": 10 - cycle,
                }
            )

    return pd.DataFrame(rows)


def test_split_keeps_runs_separate():

    dataframe = create_test_dataframe()

    splitter = RULDatasetSplitter(
        seed=42
    )

    train_df, validation_df, test_df = (
        splitter.split(dataframe)
    )

    train_runs = set(train_df["run_id"])
    validation_runs = set(validation_df["run_id"])
    test_runs = set(test_df["run_id"])

    assert train_runs.isdisjoint(validation_runs)
    assert train_runs.isdisjoint(test_runs)
    assert validation_runs.isdisjoint(test_runs)


def test_split_contains_all_runs():

    dataframe = create_test_dataframe()

    splitter = RULDatasetSplitter(
        seed=42
    )

    train_df, validation_df, test_df = (
        splitter.split(dataframe)
    )

    all_runs = (
        set(train_df["run_id"])
        | set(validation_df["run_id"])
        | set(test_df["run_id"])
    )

    assert all_runs == set(range(1, 101))


def test_split_uses_expected_run_counts():

    dataframe = create_test_dataframe()

    splitter = RULDatasetSplitter(
        seed=42
    )

    train_df, validation_df, test_df = (
        splitter.split(dataframe)
    )

    assert train_df["run_id"].nunique() == 80
    assert validation_df["run_id"].nunique() == 10
    assert test_df["run_id"].nunique() == 10