from typing import Any
from dong.io import BaseExporter, ExporterRegistry
import sqlite3
from pathlib import Path

class PassExporter(BaseExporter):
    name = "pass"
    
    def fetch_all(self) -> list[dict[str, Any]]:
        db_path = Path.home() / ".dong" / "pass" / "pass.db"
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT id, site, account, password, category FROM accounts ORDER BY site")
            return [dict(row) for row in cur.fetchall()]

ExporterRegistry.register(PassExporter())
