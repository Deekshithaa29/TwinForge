from app.degradation.dataset_generator import RULDatasetGenerator
from app.twin.machine.health import HealthState


def test_dataset_generator_creates_multiple_runs():
    generator = RULDatasetGenerator(
        number_of_runs=3,
        dt=3600.0,
    )

    records = generator.generate()

    assert len(records) > 0

    run_ids = {record.run_id for record in records}

    assert run_ids == {1, 2, 3}


def test_each_run_ends_in_failed_state():
    generator = RULDatasetGenerator(
        number_of_runs=3,
        dt=3600.0,
    )

    records = generator.generate()

    runs: dict[int, list] = {}

    for record in records:
        runs.setdefault(record.run_id, []).append(record)

    assert len(runs) == 3

    for run_records in runs.values():
        assert run_records[-1].health_state == HealthState.FAILED.value
        assert run_records[-1].rul_hours == 0.0


def test_rul_decreases_over_lifecycle():
    generator = RULDatasetGenerator(
        number_of_runs=1,
        dt=3600.0,
    )

    records = generator.generate()

    assert len(records) > 1

    for previous, current in zip(records, records[1:]):
        assert previous.rul_hours is not None
        assert current.rul_hours is not None

        assert previous.rul_hours >= current.rul_hours


def test_rul_is_never_negative():
    generator = RULDatasetGenerator(
        number_of_runs=2,
        dt=3600.0,
    )

    records = generator.generate()

    for record in records:
        assert record.rul_hours is not None
        assert record.rul_hours >= 0.0


def test_each_run_has_unique_machine_id():
    generator = RULDatasetGenerator(
        number_of_runs=3,
        dt=3600.0,
    )

    records = generator.generate()

    machine_ids_by_run: dict[int, set[str]] = {}

    for record in records:
        machine_ids_by_run.setdefault(
            record.run_id,
            set(),
        ).add(record.machine_id)

    assert len(machine_ids_by_run) == 3

    for machine_ids in machine_ids_by_run.values():
        assert len(machine_ids) == 1

    all_machine_ids = {
        next(iter(machine_ids))
        for machine_ids in machine_ids_by_run.values()
    }

    assert len(all_machine_ids) == 3