"""stats 命令 - 统计"""

import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from ..db import get_cursor, is_initialized
from dong import json_output, DongError

console = Console()


@json_output
def stats(
    project: str = typer.Option(None, "--project", "-p", help="按项目筛选"),
):
    """统计会员数据"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-member init")
    
    with get_cursor() as cur:
        # 按项目统计
        if project:
            cur.execute("""
                SELECT 
                    project,
                    member_type,
                    COUNT(*) as count,
                    SUM(price) as total_price
                FROM members
                WHERE project = ? AND status = 'active'
                GROUP BY project, member_type
                ORDER BY project, member_type
            """, (project,))
        else:
            cur.execute("""
                SELECT 
                    project,
                    member_type,
                    COUNT(*) as count,
                    SUM(price) as total_price
                FROM members
                WHERE status = 'active'
                GROUP BY project, member_type
                ORDER BY project, member_type
            """)
        
        project_stats = cur.fetchall()
        
        # 总收入
        cur.execute("""
            SELECT SUM(price) FROM members WHERE price IS NOT NULL AND status = 'active'
        """)
        total = cur.fetchone()[0] or 0
    
    if not project_stats:
        console.print("暂无会员数据")
        return {"projects": [], "total": 0}
    
    # 渲染表格
    table = Table(title="📊 会员统计")
    table.add_column("项目", style="cyan")
    table.add_column("类型", style="blue")
    table.add_column("人数", justify="right")
    table.add_column("总收入", justify="right", style="green")
    table.add_column("占比", justify="right")
    
    projects = []
    for row in project_stats:
        proj, member_type, count, total_price = row
        total_price = total_price or 0
        percentage = (total_price / total * 100) if total > 0 else 0
        
        type_str = "年费" if member_type == "yearly" else "永久"
        
        table.add_row(
            proj or "-",
            type_str,
            str(count),
            f"¥{total_price:.0f}",
            f"{percentage:.1f}%",
        )
        
        projects.append({
            "project": proj,
            "member_type": member_type,
            "count": count,
            "total_price": total_price,
            "percentage": round(percentage, 1),
        })
    
    # 总计行
    total_count = sum(p[2] for p in project_stats)
    table.add_row("总计", "-", str(total_count), f"¥{total:.0f}", "100%")
    
    console.print(table)
    
    return {"projects": projects, "total": total, "total_count": total_count}
