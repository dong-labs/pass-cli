"""ls 命令"""
import typer
import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table
from dong import json_output

console = Console()


@json_output
def ls(
    category: str = typer.Option(None, "--category", "-c", help="按分类筛选"),
):
    """列出所有账号"""
    db_path = Path.home() / ".dong" / "accounts.db"
    if not db_path.exists():
        return {"error": "数据库不存在，请先运行 dong-pass init"}

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if category:
        cur.execute("""
            SELECT * FROM accounts WHERE category = ?
            ORDER BY last_used_at DESC
        """, (category,))
    else:
        cur.execute("""
            SELECT * FROM accounts
            ORDER BY last_used_at DESC
        """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {"accounts": [], "total": 0}

    accounts = [dict(row) for row in rows]
    return {"accounts": accounts, "total": len(accounts)}
