
from app.infrastructure.database.database import SQLiteDatabase
from app.infrastructure.repository.telemetry_repository import TelemetryRepository
from app.twin.telemetry.telemetry import Telemetry
from datetime import datetime
from typing import override


class SQLiteTelemetryRepository(TelemetryRepository):

    INSERT_TELEMETRY = """
        INSERT INTO telemetry (
            timestamp,
            machine_id,
            machine_name,
            machine_type,
            status,
            temperature,
            vibration,
            current_rpm,
            load,
            health,
            runtime_hours
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    def __init__(self, database: SQLiteDatabase):
        self.database = database

    @staticmethod
    def _row_to_telemetry(row) -> Telemetry:
        return Telemetry(
            timestamp=datetime.fromisoformat(row["timestamp"]),
            machine_id=row["machine_id"],
            machine_name=row["machine_name"],
            machine_type=row["machine_type"],
            status=row["status"],
            temperature=row["temperature"],
            vibration=row["vibration"],
            current_rpm=row["current_rpm"],
            load=row["load"],
            health=row["health"],
            runtime_hours=row["runtime_hours"]
        )

    @override
    def get_latest(self) -> dict[str, Telemetry]:

        cursor = self.database.cursor()

        cursor = cursor.execute(
            "SELECT COUNT(*) AS count FROM telemetry"
        )

        count = cursor.fetchone()["count"]

        print(f"Telemetry rows in database: {count}")

        cursor.execute(
            """
            SELECT *
            FROM telemetry
            ORDER BY timestamp DESC
            """
        )

        rows = cursor.fetchall()

        latest: dict[str, Telemetry] = {}

        for row in rows:

            machine_id = row["machine_id"]

            if machine_id in latest:
                continue

            latest[machine_id] = self._row_to_telemetry(row)

        return latest   

    @override
    def get_all_history(self) -> dict[str, list[Telemetry]]:

        """Return the complete telemetry history for all machines."""

        cursor = self.database.cursor()

        cursor.execute(
            """
            SELECT *
            FROM telemetry
            ORDER BY timestamp DESC
            """
        )

        rows = cursor.fetchall()

        history: dict[str, list[Telemetry]] = {}

        for row in rows:

            machine_id = row["machine_id"]

            if machine_id not in history:
                history[machine_id] = []

            history[machine_id].append(self._row_to_telemetry(row))

        return history

    @override
    def get_history_for_machine(self, machine_id: str) -> list[Telemetry]:

        """Return the complete telemetry history for a specific machine."""

        cursor = self.database.cursor()

        cursor.execute(
            """
            SELECT *
            FROM telemetry
            WHERE machine_id = ?
            ORDER BY timestamp ASC
            """,
            (machine_id,)
        )

        rows = cursor.fetchall()

        history: list[Telemetry] = []

        return [self._row_to_telemetry(row) for row in rows]

    @override
    def save(self, telemetry: Telemetry) -> None:
        """
        Save telemetry data to the SQLite database.
        """
        cursor = self.database.cursor()
        cursor.execute(self.INSERT_TELEMETRY, telemetry.to_database())
        self.database.commit()