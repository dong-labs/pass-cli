"""add 命令"""
import typer
import sqlite3
from pathlib import Path

def add(
    site: str = typer.Argument(..., help="网站名称"),
    account: str = typer.Option(..., "--account", "-a", help="账号"),
    password: str = typer.Option(..., "--password", "-p", help="密码"),
    category: str = typer.Option(None, "--category", "-c", help="分类"),
):
    """添加账号密码"""
    db_path = Path.home() / ".dong" / "accounts.db"
    if not db_path.exists():
        typer.echo("❌ 数据库不存在，请先运行 dong-pass init")
        raise typer.Exit(1)

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO accounts (site, account, password, category)
            VALUES (?, ?, ?, ?)
        """, (site.lower(), account, password, category))

        conn.commit()
        typer.echo(f"✅ 已添加账号：{site}")
    except sqlite3.IntegrityError:
        typer.echo(f"❌ 网站 '{site}' 已存在")
        raise typer.Exit(1)
    finally:
        conn.close()
