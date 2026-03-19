import typer
from rich.console import Console

console = Console()

app = typer.Typer(
    name="dong-pass",
    help="密码咚 - 账号密码管理 CLI",
    no_args_is_help=True,
    add_completion=False,
)

@app.command()
def init():
    """初始化数据库"""
    import sqlite3
    from pathlib import Path
    db_path = Path.home() / ".dong" / "accounts.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT NOT NULL UNIQUE, account TEXT NOT NULL, password TEXT NOT NULL, category TEXT)")
    conn.commit()
    conn.close()
    console.print("[green]✅ 数据库初始化成功[/green]")

@app.command()
def add(site: str = typer.Argument(...), account: str = typer.Option(..., "--account", "-a"), password: str = typer.Option(..., "--password", "-p"), category: str = typer.Option(None, "--category", "-c")):
    """添加账号密码"""
    import sqlite3
    from pathlib import Path
    db_path = Path.home() / ".dong" / "accounts.db"
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO accounts (site, account, password, category) VALUES (?, ?, ?, ?)", (site.lower(), account, password, category))
        conn.commit()
        console.print(f"[green]✅ 已添加账号：{site}[/green]")
    except sqlite3.IntegrityError:
        console.print(f"[red]❌ 网站 '{site}' 已存在[/red]")
        raise typer.Exit(1)
    finally:
        conn.close()

@app.command()
def get(site: str = typer.Argument(...)):
    """获取账号密码"""
    import sqlite3
    from pathlib import Path
    from rich.table import Table
    db_path = Path.home() / ".dong" / "accounts.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts WHERE site = ?", (site.lower(),))
    row = cur.fetchone()
    conn.close()
    if not row:
        console.print(f"[red]❌ 未找到网站：{site}[/red]")
        raise typer.Exit(1)
    table = Table(title=f"账号信息：{row['site']}")
    table.add_column("项目", style="cyan")
    table.add_column("内容", style="green")
    table.add_row("网站", row['site'])
    table.add_row("账号", row['account'])
    table.add_row("密码", row['password'])
    if row['category']:
        table.add_row("分类", row['category'])
    console.print(table)

@app.command(name="list")
def list_accounts(category: str = typer.Option(None, "--category", "-c")):
    """列出所有账号"""
    import sqlite3
    from pathlib import Path
    from rich.table import Table
    db_path = Path.home() / ".dong" / "accounts.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if category:
        cur.execute("SELECT * FROM accounts WHERE category = ?", (category,))
    else:
        cur.execute("SELECT * FROM accounts")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        console.print("暂无账号记录")
        return
    table = Table(title=f"账号列表 {f'（分类：{category}）' if category else ''}")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("网站", style="green")
    table.add_column("账号", style="yellow")
    table.add_column("分类", style="magenta")
    for row in rows:
        table.add_row(str(row['id']), row['site'], row['account'], row['category'] or "-")
    console.print(table)

@app.command()
def delete(site: str = typer.Option(...)):
    """删除账号"""
    import sqlite3
    from pathlib import Path
    db_path = Path.home() / ".dong" / "accounts.db"
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT site FROM accounts WHERE site = ?", (site.lower(),))
    row = cur.fetchone()
    if not row:
        console.print(f"[red]❌ 未找到网站：{site}[/red]")
        raise typer.Exit(1)
    if not typer.confirm(f"确定要删除网站 '{row[0]}' 吗？"):
        return
    cur.execute("DELETE FROM accounts WHERE site = ?", (site.lower(),))
    conn.commit()
    conn.close()
    console.print(f"[green]✅ 已删除账号：{row[0]}[/green]")

@app.command()
def stats():
    """统计信息"""
    import sqlite3
    from pathlib import Path
    from rich.table import Table
    db_path = Path.home() / ".dong" / "accounts.db"
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM accounts")
    total = cur.fetchone()[0]
    cur.execute("SELECT category, COUNT(*) as count FROM accounts GROUP BY category")
    category_stats = cur.fetchall()
    conn.close()
    if total == 0:
        console.print("暂无账号记录")
        return
    table = Table(title="账号统计")
    table.add_column("分类", style="blue")
    table.add_column("数量", justify="right", style="cyan")
    for category, count in category_stats:
        table.add_row(category or "未分类", str(count))
    table.add_row("总计", str(total))
    console.print(table)

@app.callback()
def main(version: bool = typer.Option(False, "--version", "-v")):
    """密码咚 - 账号密码管理 CLI"""
    if version:
        console.print(f"dong-pass 0.1.0")
        raise typer.Exit()

if __name__ == "__main__":
    app()
