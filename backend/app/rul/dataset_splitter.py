from __future__ import annotations

import random

import pandas as pd


class RULDatasetSplitter:
    def __init__(
        self,
        train_ratio: float = 0.8,
        validation_ratio: float = 0.1,
        seed: int = 42,
    ):
        self.train_ratio = train_ratio
        self.validation_ratio = validation_ratio
        self.seed = seed

    def split(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

        run_ids = dataframe["run_id"].unique().tolist()

        random_generator = random.Random(self.seed)
        random_generator.shuffle(run_ids)

        total_runs = len(run_ids)

        train_count = int(
            total_runs * self.train_ratio
        )

        validation_count = int(
            total_runs * self.validation_ratio
        )

        train_run_ids = set(
            run_ids[:train_count]
        )

        validation_run_ids = set(
            run_ids[
                train_count:
                train_count + validation_count
            ]
        )

        test_run_ids = set(
            run_ids[
                train_count + validation_count:
            ]
        )

        train_df = dataframe[
            dataframe["run_id"].isin(train_run_ids)
        ].copy()

        validation_df = dataframe[
            dataframe["run_id"].isin(validation_run_ids)
        ].copy()

        test_df = dataframe[
            dataframe["run_id"].isin(test_run_ids)
        ].copy()

        return (
            train_df,
            validation_df,
            test_df,
        )