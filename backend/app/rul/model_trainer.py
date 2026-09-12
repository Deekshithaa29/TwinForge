from __future__ import annotations

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
)


class RULModelTrainer:
    @staticmethod
    def train_baseline(X_train, y_train):
        model = DummyRegressor(strategy="mean")
        model.fit(X_train, y_train)
        return model

    @staticmethod
    def train_random_forest(
        X_train,
        y_train,
        n_estimators: int = 200,
        random_state: int = 42,
    ):
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
        )

        model.fit(X_train, y_train)

        return model


    def train_gradient_boosting(
        X_train,
        y_train,
        n_estimators: int = 200,
        learning_rate: float = 0.05,
        max_depth: int = 3,
        random_state: int = 42,
    ):
        model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
        )

        model.fit(X_train, y_train)

        return model