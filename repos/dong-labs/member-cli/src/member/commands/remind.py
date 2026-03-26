"""remind 命令 - 查看即将到期会员"""

import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime, date
from ..db import get_cursor, is_initialized
from dong import json_output, DongError

console = Console()


@json_output
def remind(
    days: int = typer.Option(7, "--days", "-d", help="提前多少天提醒"),
    project: str = typer.Option(None, "--project", "-p", help="按项目筛选"),
):
    """查看即将到期的会员"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-member init")
    
    today = date.today()
    
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM members WHERE status = 'active' ORDER BY expire_date ASC"
        )
        rows = cur.fetchall()
    
    # 筛选即将到期的（永久会员除外）
    expiring = []
    for row in rows:
        (member_id, name, wechat, phone, email, account_id, member_type, proj,
         join_date_str, expire_date_str, price, currency, status, source,
         notes, created_at, updated_at) = row
        
        # 永久会员跳过
        if member_type == "lifetime":
            continue
        
        # 按项目筛选
        if project and proj != project:
            continue
        
        if not expire_date_str:
            continue
        
        expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d").date()
        days_left = (expire_date - today).days
        
        if 0 <= days_left <= days:
            expiring.append({
                "id": member_id,
                "name": name,
                "wechat": wechat,
                "project": proj,
                "join_date": join_date_str,
                "expire_date": expire_date_str,
                "days_left": days_left,
                "price": price,
            })
    
    if not expiring:
        console.print(f"[green]✅ 未来 {days} 天内无到期会员[/green]")
        return {"members": [], "total": 0}
    
    # 渲染表格
    table = Table(title=f"⏰ 即将到期会员（{days}天内）")
    table.add_column("ID", justify="right", style="cyan", width=4)
    table.add_column("姓名", style="yellow", width=8)
    table.add_column("微信", style="blue", width=12)
    table.add_column("项目", width=10)
    table.add_column("加入日期", width=10)
    table.add_column("到期日期", style="red", width=10)
    table.add_column("剩余", justify="right", style="red", width=6)
    
    for item in expiring:
        table.add_row(
            str(item["id"]),
            item["name"],
            item["wechat"] or "-",
            item["project"] or "-",
            item["join_date"],
            item["expire_date"],
            f"{item['days_left']}天",
        )
    
    console.print(table)
    
    return {"members": expiring, "total": len(expiring)}
