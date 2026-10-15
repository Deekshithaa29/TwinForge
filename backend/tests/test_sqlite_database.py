import sqlite3
import threading

import pytest

from app.infrastructure.database.database import SQLiteDatabase


@pytest.fixture
def database(tmp_path):
    db = SQLiteDatabase(str(tmp_path / "test.db"))

    yield db

    db.close()


def test_transaction_commits_successfully(database):
    with database.transaction() as cursor:
        cursor.execute(
            "CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)"
        )
        cursor.execute(
            "INSERT INTO test (value) VALUES (?)",
            ("TwinForge",),
        )

    with database.transaction() as cursor:
        cursor.execute("SELECT value FROM test")
        row = cursor.fetchone()

    assert row["value"] == "TwinForge"


def test_transaction_rolls_back_on_error(database):
    with database.transaction() as cursor:
        cursor.execute(
            "CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)"
        )

    with pytest.raises(sqlite3.IntegrityError):
        with database.transaction() as cursor:
            cursor.execute(
                "INSERT INTO test (id, value) VALUES (?, ?)",
                (1, "First"),
            )
            cursor.execute(
                "INSERT INTO test (id, value) VALUES (?, ?)",
                (1, "Duplicate"),
            )

    with database.transaction() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM test")
        count = cursor.fetchone()["count"]

    assert count == 0


def test_close_is_idempotent(database):
    database.close()
    database.close()


def test_transaction_after_close_raises(database):
    database.close()

    with pytest.raises(RuntimeError):
        with database.transaction():
            pass


def test_concurrent_writes(database):
    with database.transaction() as cursor:
        cursor.execute(
            "CREATE TABLE test (id INTEGER PRIMARY KEY, value INTEGER)"
        )

    def writer(value):
        with database.transaction() as cursor:
            cursor.execute(
                "INSERT INTO test (value) VALUES (?)",
                (value,),
            )

    threads = [
        threading.Thread(target=writer, args=(i,))
        for i in range(20)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with database.transaction() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM test")
        count = cursor.fetchone()["count"]

    assert count == 20