from typing import Any
from dong.io import BaseImporter, ImporterRegistry
from .db.connection import ExpireDatabase

class ExpireImporter(BaseImporter):
    name = "expire"
    
    def validate(self, data: list[dict[str, Any]]) -> tuple[bool, str]:
        if not isinstance(data, list): return False, "数据必须是列表格式"
        for i, item in enumerate(data):
            if not isinstance(item, dict) or "name" not in item or "expire_date" not in item:
                return False, f"第 {i+1} 条数据缺少 name 或 expire_date 字段"
        return True, ""
    
    def import_data(self, data: list[dict[str, Any]], merge: bool = False) -> dict[str, Any]:
        with ExpireDatabase.get_cursor() as cur:
            if not merge: cur.execute("DELETE FROM expires")
            imported, skipped = 0, 0
            for item in data:
                if merge:
                    cur.execute("SELECT id FROM expires WHERE name = ?", (item["name"],))
                    if cur.fetchone(): skipped += 1; continue
                cur.execute("INSERT INTO expires (name, category, expire_date, cost, currency, repeat, remind_days, status, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (item["name"], item.get("category"), item["expire_date"], item.get("cost"), item.get("currency", "CNY"), item.get("repeat"), item.get("remind_days", "30,7,1"), item.get("status", "active"), item.get("note")))
                imported += 1
            return {"imported": imported, "skipped": skipped, "total": len(data)}

ImporterRegistry.register(ExpireImporter())
