"""init 命令"""
import typer
import sqlite3
from pathlib import Path

app = typer.Typer()

@typer.command()
def init():
    """初始化数据库"""
    db_path = Path.home() / ".dong" / "accounts.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL UNIQUE,
            account TEXT NOT NULL,
            password TEXT NOT NULL,
            nickname TEXT,
            category TEXT,
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_used_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    
    typer.echo("✅ 数据库初始化成功")
