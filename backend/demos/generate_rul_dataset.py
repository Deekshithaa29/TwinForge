from app.degradation.dataset_exporter import RULDatasetExporter
from app.degradation.dataset_generator import RULDatasetGenerator


generator = RULDatasetGenerator(
    number_of_runs=100,
    physics_dt=10.0,
    sample_interval=3600.0,
)

records = generator.generate()

RULDatasetExporter.export_csv(
    records,
    "data/rul_dataset.csv",
)

print(f"Generated {len(records)} lifecycle records.")