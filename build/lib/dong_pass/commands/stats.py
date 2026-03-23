"""stats 命令"""
import typer
import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def stats():
    """统计信息"""
    db_path = Path.home() / ".dong" / "accounts.db"
    if not db_path.exists():
        typer.echo("❌ 数据库不存在，请先运行 dong-pass init")
        raise typer.Exit(1)

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM accounts")
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT category, COUNT(*) as count
        FROM accounts
        GROUP BY category
    """)
    category_stats = cur.fetchall()
    conn.close()

    if total == 0:
        console.print("暂无账号记录")
        return

    table = Table(title="账号统计")
    table.add_column("分类", style="blue")
    table.add_column("数量", justify="right", style="cyan")
    table.add_column("占比", justify="right", style="green")

    for category, count in category_stats:
        category = category or "未分类"
        percentage = (count / total * 100)
        table.add_row(category, str(count), f"{percentage:.1f}%")

    table.add_row("总计", str(total), "100%")
    console.print(table)
