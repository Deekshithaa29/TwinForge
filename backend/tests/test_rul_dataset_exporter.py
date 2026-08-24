import csv

import pytest

from app.degradation.dataset_exporter import RULDatasetExporter
from app.degradation.lifecycle_record import LifecycleRecord


def create_record() -> LifecycleRecord:
    return LifecycleRecord(
        run_id=1,
        cycle=1,
        machine_id="TRAIN-SPINDLE-001",
        runtime_hours=1.0,
        temperature=45.0,
        vibration=2.0,
        rpm=3000.0,
        load=0.5,
        health=99.5,
        health_state="HEALTHY",
        rul_hours=100.0,
    )


def test_export_csv_creates_file(tmp_path):
    output_file = tmp_path / "rul_dataset.csv"

    RULDatasetExporter.export_csv(
        [create_record()],
        output_file,
    )

    assert output_file.exists()


def test_export_csv_contains_record(tmp_path):
    output_file = tmp_path / "rul_dataset.csv"

    RULDatasetExporter.export_csv(
        [create_record()],
        output_file,
    )

    with output_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["machine_id"] == "TRAIN-SPINDLE-001"
    assert float(rows[0]["rul_hours"]) == 100.0


def test_export_csv_rejects_empty_dataset(tmp_path):
    output_file = tmp_path / "rul_dataset.csv"

    with pytest.raises(
        ValueError,
        match="Cannot export an empty dataset",
    ):
        RULDatasetExporter.export_csv(
            [],
            output_file,
        )