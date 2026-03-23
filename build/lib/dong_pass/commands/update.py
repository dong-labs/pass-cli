"""update 命令"""
import typer
import sqlite3
from pathlib import Path

def update(
    site: str = typer.Argument(..., help="网站名称"),
    account: str = typer.Option(None, "--account", help="账号"),
    password: str = typer.Option(None, "--password", help="密码"),
    category: str = typer.Option(None, "--category", help="分类"),
):
    """更新账号"""
    db_path = Path.home() / ".dong" / "accounts.db"
    if not db_path.exists():
        typer.echo("❌ 数据库不存在，请先运行 dong-pass init")
        raise typer.Exit(1)

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # 构建更新语句
    updates = []
    params = []

    if account:
        updates.append("account = ?")
        params.append(account)
    if password:
        updates.append("password = ?")
        params.append(password)
    if category:
        updates.append("category = ?")
        params.append(category)

    if not updates:
        typer.echo("❌ 没有指定要更新的字段")
        raise typer.Exit(1)

    params.append(site.lower())

    cur.execute(
        f"UPDATE accounts SET {', '.join(updates)} WHERE site = ?",
        params
    )

    if cur.rowcount == 0:
        typer.echo(f"❌ 未找到网站：{site}")
        raise typer.Exit(1)

    conn.commit()
    conn.close()

    typer.echo(f"✅ 已更新账号：{site}")
