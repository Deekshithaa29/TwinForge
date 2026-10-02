from app.infrastructure.database.database import SQLiteDatabase


def create_schema(database: SQLiteDatabase) -> None:

    cursor = database.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            machine_id TEXT NOT NULL,
            machine_name TEXT NOT NULL,
            machine_type TEXT NOT NULL,
            status TEXT NOT NULL,
            temperature REAL,
            vibration REAL,
            current_rpm REAL NOT NULL,
            load REAL NOT NULL,
            health REAL NOT NULL,
            runtime_hours REAL NOT NULL,
            predicted_rul_hours REAL
        )
        """
    )

    cursor.execute(
        "PRAGMA table_info(telemetry)"
    )

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if "predicted_rul_hours" not in columns:
        cursor.execute(
            "ALTER TABLE telemetry "
            "ADD COLUMN predicted_rul_hours REAL"
        )

    database.commit()