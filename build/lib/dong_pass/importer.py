from typing import Any
from dong.io import BaseImporter, ImporterRegistry
import sqlite3
from pathlib import Path

class PassImporter(BaseImporter):
    name = "pass"

    def validate(self, data: list[dict[str, Any]]) -> tuple[bool, str]:
        if not isinstance(data, list): return False, "数据必须是列表格式"
        for i, item in enumerate(data):
            if not isinstance(item, dict) or "site" not in item or "account" not in item:
                return False, f"第 {i+1} 条数据缺少 site 或 account 字段"
        return True, ""

    def import_data(self, data: list[dict[str, Any]], merge: bool = False) -> dict[str, Any]:
        db_path = Path.home() / ".dong" / "pass" / "pass.db"
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            if not merge: cur.execute("DELETE FROM accounts")
            imported, skipped = 0, 0
            for item in data:
                if merge:
                    cur.execute("SELECT id FROM accounts WHERE site = ? AND account = ?", (item["site"], item["account"]))
                    if cur.fetchone(): skipped += 1; continue
                cur.execute("INSERT INTO accounts (site, account, password, category) VALUES (?, ?, ?, ?)",
                    (item["site"], item["account"], item.get("password", ""), item.get("category")))
                imported += 1
            return {"imported": imported, "skipped": skipped, "total": len(data)}

ImporterRegistry.register(PassImporter())
