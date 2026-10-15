
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
            runtime_hours,
            predicted_rul_hours,
            maintenance_status,
            maintenance_severity,
            maintenance_message,
            recommended_action
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    def __init__(self, database: SQLiteDatabase):
        self.database = database

    @staticmethod
    def _health_state_from_health(health: float) -> str:
        if health >= 80.0:
            return "HEALTHY"
        elif health >= 50.0:
            return "DEGRADED"
        elif health >= 20.0:
            return "CRITICAL"
        else:
            return "FAILED"

    @classmethod
    def _row_to_telemetry(cls, row) -> Telemetry:
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
            health_state=cls._health_state_from_health(row["health"]),
            runtime_hours=row["runtime_hours"],
            predicted_rul_hours=row["predicted_rul_hours"],
            maintenance_status=row["maintenance_status"],
            maintenance_severity=row["maintenance_severity"],
            maintenance_message=row["maintenance_message"],
            recommended_action=row["recommended_action"]
        )

    @override
    def get_latest(self) -> dict[str, Telemetry]:
        """
        Return the latest telemetry record for each machine.
        """
        with self.database.transaction() as cursor:
            cursor.execute(
                """
                SELECT t.*
                FROM telemetry AS t
                WHERE t.id = (
                    SELECT t2.id
                    FROM telemetry AS t2
                    WHERE t2.machine_id = t.machine_id
                    ORDER BY t2.timestamp DESC, t2.id DESC
                    LIMIT 1
                )
                """
            )
            rows = cursor.fetchall()

        return {
            row["machine_id"]: self._row_to_telemetry(row)
            for row in rows
        }   

    @override
    def get_all_history(self) -> dict[str, list[Telemetry]]:

        """Return the complete telemetry history for all machines."""

        with self.database.transaction() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM telemetry
                ORDER BY timestamp DESC, id DESC
                """
            )

            rows = cursor.fetchall()

        history: dict[str, list[Telemetry]] = {}

        for row in rows:
            machine_id = row["machine_id"]

            history.setdefault(machine_id, []).append(self._row_to_telemetry(row))

        return history

    @override
    def get_history_for_machine(self, machine_id: str) -> list[Telemetry]:

        """Return the complete telemetry history for a specific machine."""

        with self.database.transaction() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM telemetry
                WHERE machine_id = ?
                ORDER BY timestamp ASC, id ASC
                """,
                (machine_id,),
            )

            rows = cursor.fetchall()
        return [self._row_to_telemetry(row) for row in rows]

    @override
    def save(self, telemetry: Telemetry) -> None:
        """
        Save telemetry data to the SQLite database.
        """
        with self.database.transaction() as cursor:
            cursor.execute(
                self.INSERT_TELEMETRY,
                telemetry.to_database(),
            )