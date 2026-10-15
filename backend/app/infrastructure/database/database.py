from pathlib import Path
import sqlite3
import threading
from contextlib import contextmanager
from collections.abc import Iterator


class SQLiteDatabase:
    """
    Manages a thread-safe SQLite connection for TwinForge.
    """

    def __init__(self, database_name: str = "twinforge.db"):
        self.database_path = Path(database_name)

        self._lock = threading.RLock()
        self._closed = False

        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False,
            timeout=10.0,
        )

        self.connection.row_factory = sqlite3.Row

        # Improves concurrent access from separate connections.
        self.connection.execute("PRAGMA journal_mode=WAL")

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Cursor]:
        """
        Execute database operations under one lock.

        Commits successful operations and rolls back on failure.
        """
        with self._lock:
            if self._closed:
                raise RuntimeError("Database connection is closed.")

            cursor = self.connection.cursor()

            try:
                yield cursor
                self.connection.commit()
            except Exception:
                self.connection.rollback()
                raise
            finally:
                cursor.close()

    def cursor(self):
        """
        Legacy cursor access.

        Prefer transaction() for new database operations.
        """
        if self._closed:
            raise RuntimeError("Database connection is closed.")

        return self.connection.cursor()

    def commit(self):
        with self._lock:
            if self._closed:
                raise RuntimeError("Database connection is closed.")

            self.connection.commit()

    def close(self):
        with self._lock:
            if self._closed:
                return

            self.connection.close()
            self._closed = True