
from datetime import datetime, timedelta, timezone
import threading

import pytest

from app.infrastructure.database.database import SQLiteDatabase
from app.infrastructure.database.schema import create_schema
from app.infrastructure.repository.sqlite_repository import SQLiteTelemetryRepository
from app.twin.telemetry.telemetry import Telemetry


@pytest.fixture
def repository(tmp_path):
    database = SQLiteDatabase(str(tmp_path / "telemetry_test.db"))
    create_schema(database)

    repo = SQLiteTelemetryRepository(database)

    yield repo

    database.close()


def make_telemetry(
    machine_id: str,
    timestamp: datetime,
    runtime_hours: float,
) -> Telemetry:
    return Telemetry(
        timestamp=timestamp,
        machine_id=machine_id,
        machine_name=f"Machine {machine_id}",
        machine_type="CNC_SPINDLE",
        status="RUNNING",
        temperature=65.0,
        vibration=2.5,
        current_rpm=3000.0,
        load=0.75,
        health=85.0,
        health_state="HEALTHY",
        runtime_hours=runtime_hours,
        predicted_rul_hours=120.0,
        maintenance_status="NORMAL",
        maintenance_severity="INFO",
        maintenance_message="Machine operating normally",
        recommended_action="Continue monitoring",
    )


def test_latest_telemetry_for_multiple_machines(repository):
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)

    repository.save(make_telemetry("M1", base, 1.0))
    repository.save(make_telemetry("M2", base, 10.0))
    repository.save(
        make_telemetry("M1", base + timedelta(hours=1), 2.0)
    )
    repository.save(
        make_telemetry("M2", base + timedelta(hours=2), 12.0)
    )

    latest = repository.get_latest()

    assert set(latest.keys()) == {"M1", "M2"}
    assert latest["M1"].runtime_hours == 2.0
    assert latest["M2"].runtime_hours == 12.0


def test_history_ordering_with_identical_timestamps(repository):
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)

    for runtime in [1.0, 2.0, 3.0]:
        repository.save(
            make_telemetry("M1", timestamp, runtime)
        )

    machine_history = repository.get_history_for_machine("M1")

    assert [
        item.runtime_hours for item in machine_history
    ] == [1.0, 2.0, 3.0]

    all_history = repository.get_all_history()

    assert [
        item.runtime_hours for item in all_history["M1"]
    ] == [3.0, 2.0, 1.0]


def test_concurrent_reads_and_writes(repository):
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    errors = []
    start_event = threading.Event()

    def writer():
        try:
            start_event.wait()

            for i in range(100):
                repository.save(
                    make_telemetry(
                        "M1",
                        base + timedelta(seconds=i),
                        float(i),
                    )
                )
        except Exception as exc:
            errors.append(exc)

    def reader():
        try:
            start_event.wait()

            for _ in range(100):
                repository.get_latest()
                repository.get_history_for_machine("M1")
                repository.get_all_history()
        except Exception as exc:
            errors.append(exc)

    threads = [
        threading.Thread(target=writer),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
    ]

    for thread in threads:
        thread.start()

    start_event.set()

    for thread in threads:
        thread.join(timeout=10)

    assert all(not thread.is_alive() for thread in threads)
    assert not errors

    history = repository.get_history_for_machine("M1")

    assert len(history) == 100
    assert history[0].runtime_hours == 0.0
    assert history[-1].runtime_hours == 99.0

    latest = repository.get_latest()

    assert latest["M1"].runtime_hours == 99.0
