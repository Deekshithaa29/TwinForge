import csv
from dataclasses import asdict
from pathlib import Path

from app.degradation.lifecycle_record import LifecycleRecord


class RULDatasetExporter:
    """
    Exports lifecycle records into CSV format.
    """

    @staticmethod
    def export_csv(
        records: list[LifecycleRecord],
        output_path: str | Path,
    ) -> None:
        if not records:
            raise ValueError("Cannot export an empty dataset.")

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=asdict(records[0]).keys(),
            )

            writer.writeheader()

            for record in records:
                writer.writerow(asdict(record))