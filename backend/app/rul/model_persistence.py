from __future__ import annotations

from pathlib import Path

import joblib


class RULModelPersistence:
    @staticmethod
    def save(model, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(model, path)

    @staticmethod
    def load(path: str | Path):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"RUL model not found: {path}"
            )

        return joblib.load(path)