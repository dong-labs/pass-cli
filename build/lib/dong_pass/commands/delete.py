"""delete 命令"""
import typer
import sqlite3
from pathlib import Path

def delete(
    site: str = typer.Option(..., help="网站名称"),
):
    """删除账号"""
    db_path = Path.home() / ".dong" / "accounts.db"
    if not db_path.exists():
        typer.echo("❌ 数据库不存在，请先运行 dong-pass init")
        raise typer.Exit(1)

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("SELECT site FROM accounts WHERE site = ?", (site.lower(),))
    row = cur.fetchone()

    if not row:
        typer.echo(f"❌ 未找到网站：{site}")
        raise typer.Exit(1)

    if not typer.confirm(f"确定要删除网站 '{row[0]}' 吗？"):
        return

    cur.execute("DELETE FROM accounts WHERE site = ?", (site.lower(),))

    conn.commit()
    conn.close()

    typer.echo(f"✅ 已删除账号：{row[0]}")
