"""get 命令"""
import typer
import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def get(
    site: str = typer.Argument(..., help="网站名称"),
):
    """获取账号密码"""
    db_path = Path.home() / ".dong" / "accounts.db"
    if not db_path.exists():
        typer.echo("❌ 数据库不存在，请先运行 dong-pass init")
        raise typer.Exit(1)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM accounts WHERE site = ?", (site.lower(),))
    row = cur.fetchone()
    conn.close()

    if not row:
        typer.echo(f"❌ 未找到网站：{site}")
        raise typer.Exit(1)

    # 渲染表格
    table = Table(title=f"账号信息：{row['site']}")
    table.add_column("项目", style="cyan")
    table.add_column("内容", style="green")

    table.add_row("网站", row['site'])
    table.add_row("账号", row['account'])
    table.add_row("密码", row['password'])
    if row['category']:
        table.add_row("分类", row['category'])

    console.print(table)

    # 更新最后使用时间
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET last_used_at = CURRENT_TIMESTAMP WHERE site = ?", (site.lower(),))
    conn.commit()
    conn.close()
