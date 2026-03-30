from typing import Any
from dong.io import BaseExporter, ExporterRegistry
from .db.connection import ExpireDatabase

class ExpireExporter(BaseExporter):
    name = "expire"
    
    def fetch_all(self) -> list[dict[str, Any]]:
        with ExpireDatabase.get_cursor() as cur:
            cur.execute("SELECT id, name, category, expire_date, cost, currency, repeat, remind_days, status, note, created_at FROM expires ORDER BY expire_date")
            return [dict(row) for row in cur.fetchall()]

ExporterRegistry.register(ExpireExporter())
