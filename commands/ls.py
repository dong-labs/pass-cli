"""ls 命令"""
import typer
import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

@typer.command()
def list_accounts(
    category: str = typer.Option(None, "--category", "-c", help="按分类筛选"),
):
    """列出所有账号"""
    db_path = Path.home() / ".dong" / "accounts.db"
    if not db_path.exists():
        typer.echo("❌ 数据库不存在，请先运行 dong-pass init")
        raise typer.Exit(1)
    
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
        console.print("暂无账号记录")
        return
    
    table = Table(title=f"账号列表 {f'（分类：{category}）' if category else ''}")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("网站", style="green")
    table.add_column("账号", style="yellow")
    table.add_column("分类", style="magenta")
    table.add_column("最后使用")
    
    for row in rows:
        last_used = row['last_used_at'][:10] if row['last_used_at'] else "-"
        table.add_row(
            str(row['id']),
            row['site'],
            row['account'],
            row['category'] or "-",
            last_used,
        )
    
    console.print(table)
