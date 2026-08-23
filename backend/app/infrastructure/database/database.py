from pathlib import Path
import sqlite3


class SQLiteDatabase:
    """
    Manages the SQLite connection for TwinForge.
    """

    def __init__(self, database_name: str = "twinforge.db"):

        self.database_path = Path(database_name)

        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False,
        )

        self.connection.row_factory = sqlite3.Row

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()