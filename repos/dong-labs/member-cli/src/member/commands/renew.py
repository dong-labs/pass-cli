"""renew 命令 - 续费"""

import typer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ..db import get_cursor, is_initialized
from dong import json_output, DongError


@json_output
def renew(
    member_id: int = typer.Argument(..., help="会员 ID"),
    months: int = typer.Option(12, "--months", "-m", help="续费月数，默认 12 个月"),
    price: float = typer.Option(None, "--price", help="续费金额"),
    notes: str = typer.Option(None, "--notes", "-n", help="备注"),
):
    """续费会员"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-member init")
    
    with get_cursor() as cur:
        # 获取原记录
        cur.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        row = cur.fetchone()
        
        if not row:
            raise DongError("NOT_FOUND", f"未找到 ID={member_id} 的会员")
        
        old_date = row[8]  # expire_date
        member_type = row[6]  # member_type
        
        # 永久会员不能续费
        if member_type == "lifetime":
            raise DongError("LIFETIME_MEMBER", "永久会员无需续费")
        
        # 计算新日期
        if old_date:
            old_dt = datetime.strptime(old_date, "%Y-%m-%d")
        else:
            old_dt = datetime.now()
        
        new_dt = old_dt + relativedelta(months=months)
        new_date = new_dt.strftime("%Y-%m-%d")
        
        # 更新到期日期
        cur.execute(
            "UPDATE members SET expire_date = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_date, member_id)
        )
        
        # 记录续费历史
        cur.execute("""
            INSERT INTO renewals (member_id, old_date, new_date, price, months, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (member_id, old_date, new_date, price, months, notes))
        
        renewal_id = cur.lastrowid
    
    return {
        "id": member_id,
        "old_date": old_date,
        "new_date": new_date,
        "months": months,
        "price": price,
        "renewal_id": renewal_id,
    }
