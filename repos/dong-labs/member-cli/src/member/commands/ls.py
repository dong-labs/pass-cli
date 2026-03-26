"""list 命令"""

import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime, date
from ..db import get_cursor, is_initialized
from dong import json_output, DongError

console = Console()


@json_output
def list_members(
    status: str = typer.Option("active", "--status", "-s", help="按状态筛选"),
    member_type: str = typer.Option(None, "--type", "-t", help="按会员类型筛选: yearly/lifetime"),
    project: str = typer.Option(None, "--project", "-p", help="按项目筛选"),
    limit: int = typer.Option(50, "--limit", "-l", help="限制数量"),
    all: bool = typer.Option(False, "--all", "-a", help="显示所有（包括已过期）"),
):
    """列出所有会员"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-member init")
    
    today = date.today()
    
    with get_cursor() as cur:
        if all:
            cur.execute("SELECT * FROM members ORDER BY expire_date ASC")
        else:
            cur.execute(
                "SELECT * FROM members WHERE status = ? ORDER BY expire_date ASC",
                (status,)
            )
        
        rows = cur.fetchall()
    
    if not rows:
        console.print("暂无会员")
        return {"members": [], "total": 0}
    
    # 计算剩余天数
    items = []
    for row in rows:
        (member_id, name, wechat, phone, email, account_id, m_type, project_name, join_date_str,
         expire_date_str, price, currency, stat, source, notes, created_at, updated_at) = row
        
        # 按会员类型筛选
        if member_type and m_type != member_type:
            continue
        
        # 按项目筛选
        if project and project_name != project:
            continue
        
        # 永久会员
        if m_type == "lifetime":
            days_left = None
        elif expire_date_str:
            expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d").date()
            days_left = (expire_date - today).days
        else:
            days_left = None
        
        items.append({
            "id": member_id,
            "name": name,
            "wechat": wechat,
            "account_id": account_id,
            "member_type": m_type,
            "project": project_name,
            "join_date": join_date_str,
            "expire_date": expire_date_str,
            "days_left": days_left,
            "price": price,
            "status": stat,
        })
    
    # 渲染表格
    table = Table(title="会员列表")
    table.add_column("ID", justify="right", style="cyan", width=4)
    table.add_column("姓名", style="green", width=8)
    table.add_column("微信", style="blue", width=12)
    table.add_column("类型", width=6)
    table.add_column("项目", width=10)
    table.add_column("加入日期", width=10)
    table.add_column("到期日期", width=10)
    table.add_column("剩余", justify="right", width=8)
    table.add_column("金额", justify="right", style="magenta", width=8)
    
    for item in items[:limit]:
        # 会员类型
        m_type = "永久" if item["member_type"] == "lifetime" else "年费"
        
        # 剩余天数
        if item["member_type"] == "lifetime":
            days_str = "永久"
        elif item["days_left"] is None:
            days_str = "-"
        elif item["days_left"] < 0:
            days_str = f"已过期 {-item['days_left']}天"
        elif item["days_left"] == 0:
            days_str = "今天到期"
        else:
            days_str = f"{item['days_left']}天"
        
        # 到期日期
        expire_str = item["expire_date"] or "永久"
        
        price_str = f"¥{item['price']}" if item['price'] else "-"
        
        table.add_row(
            str(item["id"]),
            item["name"],
            item["wechat"] or "-",
            m_type,
            item["project"] or "-",
            item["join_date"],
            expire_str,
            days_str,
            price_str,
        )
    
    console.print(table)
    
    return {"members": items, "total": len(items)}
